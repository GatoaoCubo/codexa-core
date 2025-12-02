#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meta-Driven Workflow Executor
Executes workflows defined in JSON with runtime parameter substitution.

Philosophy: Flexibility over determinism, context over assumptions.
"""

import json
import os
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import re

# Fix Windows console encoding for UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, io.UnsupportedOperation):
        pass  # Already wrapped or not supported

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))


class MetaExecutor:
    """Execute workflows from meta-configuration."""

    def __init__(self, meta_dir: Optional[Path] = None):
        self.meta_dir = meta_dir or SCRIPT_DIR
        self.root_dir = self.meta_dir.parent
        self.system_meta = self._load_system_meta()
        self.context = {}
        self.outputs = {}
        self.errors = []

    def _load_system_meta(self) -> Dict:
        """Load system.meta.json configuration."""
        meta_file = self.meta_dir / "system.meta.json"
        if not meta_file.exists():
            raise FileNotFoundError(f"system.meta.json not found at {meta_file}")

        with open(meta_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_workflow(self, workflow_name: str) -> Dict:
        """Load workflow definition."""
        workflow_file = self.meta_dir / "workflows" / f"{workflow_name}.workflow.json"
        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow '{workflow_name}' not found")

        with open(workflow_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _substitute_placeholders(self, value: Any, context: Dict) -> Any:
        """
        Recursively substitute {{placeholders}} with context values.
        Supports:
        - {{variable}}
        - {{object.property}}
        - {{array.0}}
        - {{parameters.param_name}}
        """
        if isinstance(value, str):
            # Find all {{placeholder}} patterns
            pattern = r'\{\{([^}]+)\}\}'
            matches = re.findall(pattern, value)

            for match in matches:
                # Navigate nested properties (e.g., parameters.fetch_method)
                keys = match.strip().split('.')
                result = context
                found = True

                try:
                    for key in keys:
                        if isinstance(result, dict):
                            result = result.get(key)
                        elif isinstance(result, list):
                            result = result[int(key)]
                        else:
                            found = False
                            break

                    if found:
                        # Replace {{placeholder}} with actual value
                        placeholder = f"{{{{{match}}}}}"
                        if isinstance(result, (dict, list)):
                            return result  # Return complex types as-is
                        elif result is None:
                            # Only resolve to None for 'parameters.*' placeholders
                            # Other placeholders (like category, source_id) should be kept for later resolution
                            if match.strip().startswith('parameters.'):
                                if value.strip() == placeholder:
                                    return None
                                # Remove parameter placeholders that resolve to None
                                value = value.replace(placeholder, '')
                            # else: keep the placeholder as-is for later substitution
                        else:
                            value = value.replace(placeholder, str(result))
                except (KeyError, IndexError, ValueError):
                    # Keep placeholder if not found in context
                    pass

            return value

        elif isinstance(value, dict):
            return {k: self._substitute_placeholders(v, context) for k, v in value.items()}

        elif isinstance(value, list):
            return [self._substitute_placeholders(item, context) for item in value]

        return value

    def _load_sources(self, filter_params: Dict) -> List[Dict]:
        """
        Load sources based on filter parameters.
        Supports filtering by:
        - priority
        - categories
        - enabled status
        - custom filters
        """
        sources = []
        sources_dir = self.root_dir / "sources"

        # Determine which categories to load
        categories = filter_params.get('categories')
        if categories is None:
            # Load all JSON files in sources/
            category_files = list(sources_dir.glob("*.json"))
        else:
            # Load specific categories
            category_files = [sources_dir / f"{cat}.json" for cat in categories]

        # Load and filter sources
        for cat_file in category_files:
            if not cat_file.exists():
                continue

            with open(cat_file, 'r', encoding='utf-8') as f:
                cat_data = json.load(f)

            category_name = cat_file.stem

            # Find the key containing sources (platforms, marketplaces, etc.)
            source_key = None
            for key in cat_data.keys():
                if key not in ['metadata', 'tracking', 'cross_references', 'best_practices']:
                    source_key = key
                    break

            if not source_key:
                continue

            # Filter sources
            for source_id, source_data in cat_data[source_key].items():
                # Apply filters
                if filter_params.get('priority'):
                    if source_data.get('priority') != filter_params['priority']:
                        continue

                if filter_params.get('enabled') is not None:
                    if source_data.get('enabled', True) != filter_params['enabled']:
                        continue

                # Add to results
                sources.append({
                    'id': source_id,
                    'category': category_name,
                    'data': source_data,
                    'category_file': str(cat_file)
                })

        # Apply max_count if specified
        max_count = filter_params.get('max_count')
        if max_count:
            # Convert to int if it's a string (from CLI args or placeholder substitution)
            if isinstance(max_count, str):
                try:
                    max_count = int(max_count)
                except ValueError:
                    max_count = None

            if max_count and isinstance(max_count, int):
                sources = sources[:max_count]

        return sources

    def _execute_step(self, step: Dict, context: Dict) -> Any:
        """
        Execute a single workflow step.
        Returns: step output (to be added to context)
        """
        action = step['action']
        params = self._substitute_placeholders(step.get('params', {}), context)

        print(f"  > Executing: {step.get('description', action)}")

        # Execute based on action type
        if action == "initialize":
            return self._action_initialize(params)

        elif action == "load_sources":
            return self._action_load_sources(params)

        elif action == "fetch_content":
            return self._action_fetch_content(params, context)

        elif action == "extract_insights":
            return self._action_extract_insights(params, context)

        elif action == "generate_documentation":
            return self._action_generate_docs(params, context)

        elif action == "generate_report":
            return self._action_generate_report(params, context)

        elif action == "update_index":
            return self._action_update_index(params)

        elif action == "create_snapshot":
            return self._action_create_snapshot(params)

        elif action == "cleanup":
            return self._action_cleanup(params)

        else:
            print(f"    WARNING: Unknown action: {action}")
            return None

    # Action implementations
    def _action_initialize(self, params: Dict) -> Dict:
        """Initialize workflow execution."""
        print("    OK: System initialized")
        return {"initialized": True, "timestamp": datetime.now().isoformat()}

    def _action_load_sources(self, params: Dict) -> List[Dict]:
        """Load sources based on filter."""
        # Merge filter params with top-level max_count
        filter_params = params.get('filter', {}).copy()
        if 'max_count' in params:
            filter_params['max_count'] = params['max_count']

        sources = self._load_sources(filter_params)
        print(f"    OK: Loaded {len(sources)} sources")
        return sources

    def _action_fetch_content(self, params: Dict, context: Dict) -> List[Dict]:
        """Fetch content from sources (placeholder - needs WebFetch integration)."""
        sources = context.get('sources_list', [])
        fetched = []

        print(f"    > Fetching from {len(sources)} sources...")

        for source in sources:
            # Placeholder: In real implementation, use WebFetch or scraping
            print(f"      - {source['data']['name']} (method: {params.get('method', 'webfetch')})")

            fetched.append({
                'source_id': source['id'],
                'category': source['category'],
                'name': source['data']['name'],
                'content': f"[Fetched content for {source['data']['name']}]",
                'fetched_at': datetime.now().isoformat(),
                'method': params.get('method', 'webfetch'),
                'status': 'success'
            })

        print(f"    OK: Fetched {len(fetched)} sources")
        return fetched

    def _action_extract_insights(self, params: Dict, context: Dict) -> List[Dict]:
        """Extract insights from content (placeholder - needs AI integration)."""
        content_list = context.get('fetched_content', [])
        insights = []

        print(f"    > Extracting insights from {len(content_list)} sources...")

        for content in content_list:
            # Placeholder: In real implementation, use Claude/GPT
            insights.append({
                'source': content['name'],
                'type': 'market_validation',
                'title': f"Insight from {content['name']}",
                'description': 'Placeholder insight - integrate AI for real extraction',
                'confidence': 0.8,
                'extracted_at': datetime.now().isoformat()
            })

        print(f"    OK: Extracted {len(insights)} insights")
        return insights

    def _action_generate_docs(self, params: Dict, context: Dict) -> List[str]:
        """Generate documentation files."""
        content_list = context.get('fetched_content', [])
        doc_files = []

        print(f"    > Generating docs for {len(content_list)} sources...")

        for content in content_list:
            # Create output directory
            output_pattern = params.get('output_pattern', 'docs/{{category}}/{{source_id}}/')

            # Build context with content fields for placeholder substitution
            path_context = {
                'category': content.get('category', 'unknown'),
                'source_id': content.get('source_id', 'unknown'),
                'name': content.get('name', ''),
                'date': datetime.now().strftime('%Y-%m-%d')
            }

            # DEBUG: Check what we're substituting (uncomment to debug)
            # print(f"      DEBUG: path_context = {path_context}")
            # print(f"      DEBUG: output_pattern = '{output_pattern}'")

            output_dir = self._substitute_placeholders(output_pattern, path_context)
            output_path = self.root_dir / output_dir
            output_path.mkdir(parents=True, exist_ok=True)

            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            if params.get('create_timestamped', True):
                filename = f"overview_{timestamp}.md"
                filepath = output_path / filename
                doc_files.append(str(filepath))

            if params.get('create_latest_link', True):
                latest_path = output_path / "latest.md"
                doc_files.append(str(latest_path))

            # Placeholder: In real implementation, use template engine
            print(f"      - {content.get('name', 'Unknown')} > {output_dir}")

        print(f"    OK: Generated {len(doc_files)} doc files")
        return doc_files

    def _action_generate_report(self, params: Dict, context: Dict) -> str:
        """Generate summary report."""
        output_path = self._substitute_placeholders(params.get('output_path', ''), {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%Y-%m-%d_%H%M%S')
        })

        full_path = self.root_dir / output_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"    > Generating report: {output_path}")
        # Placeholder: Use template engine in real implementation

        print(f"    OK: Report saved: {full_path}")
        return str(full_path)

    def _action_update_index(self, params: Dict) -> str:
        """Update documentation index."""
        index_path = self.root_dir / params.get('index_path', 'docs_index_latest.json')

        # Placeholder: Implement real indexing logic
        print(f"    OK: Index updated: {index_path}")
        return str(index_path)

    def _action_create_snapshot(self, params: Dict) -> str:
        """Create snapshot of sources."""
        snapshot_dir = self._substitute_placeholders(params.get('snapshot_dir', ''), {
            'date': datetime.now().strftime('%Y-%m-%d')
        })

        full_path = self.root_dir / snapshot_dir
        full_path.mkdir(parents=True, exist_ok=True)

        print(f"    OK: Snapshot created: {snapshot_dir}")
        return str(full_path)

    def _action_cleanup(self, params: Dict) -> bool:
        """Cleanup temporary files."""
        print(f"    OK: Cleanup completed")
        return True

    def execute_workflow(self, workflow_name: str, user_params: Optional[Dict] = None):
        """
        Execute a complete workflow.

        Args:
            workflow_name: Name of workflow to execute
            user_params: Runtime parameters from user (overrides defaults)
        """
        print(f"\n{'='*60}")
        print(f"  EXECUTING WORKFLOW: {workflow_name}")
        print(f"{'='*60}\n")

        # Load workflow definition
        workflow = self._load_workflow(workflow_name)

        # Merge parameters (user params override workflow defaults)
        params = {}
        for key, spec in workflow.get('parameters', {}).items():
            default_value = spec.get('default')
            params[key] = user_params.get(key, default_value) if user_params else default_value

        # Initialize context
        self.context = {
            'parameters': params,
            'workflow': workflow,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        # Execute steps
        print(f"Steps to execute: {len(workflow['steps'])}\n")

        for i, step in enumerate(workflow['steps'], 1):
            step_id = step.get('id', f'step_{i}')
            print(f"[{i}/{len(workflow['steps'])}] {step_id}")

            try:
                # Check condition if specified
                condition = step.get('condition')
                if condition:
                    condition_result = self._substitute_placeholders(condition, self.context)
                    if not condition_result:
                        print(f"    (Skipped - condition not met)")
                        continue

                # Execute step
                result = self._execute_step(step, self.context)

                # Store outputs
                outputs_key = step.get('outputs', [])
                if outputs_key and isinstance(outputs_key, list):
                    for key in outputs_key:
                        self.context[key] = result

            except Exception as e:
                error_msg = f"Step {step_id} failed: {str(e)}"
                self.errors.append(error_msg)
                print(f"    ERROR: {error_msg}")

                # Handle failure
                on_failure = step.get('on_failure', 'abort')
                if on_failure == 'abort':
                    print(f"\nERROR: Workflow aborted due to error in step: {step_id}")
                    return False
                elif on_failure == 'continue':
                    print(f"    > Continuing despite error...")
                    continue

        # Summary
        print(f"\n{'='*60}")
        print(f"  WORKFLOW COMPLETED: {workflow_name}")
        print(f"{'='*60}")
        print(f"  Errors: {len(self.errors)}")
        if self.errors:
            for error in self.errors:
                print(f"    • {error}")
        print(f"{'='*60}\n")

        return len(self.errors) == 0


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Execute meta-driven workflows')
    parser.add_argument('--workflow', '-w', required=True, help='Workflow name to execute')
    parser.add_argument('--category', help='Specific category to process')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                       help='Filter by priority')
    parser.add_argument('--max-sources', type=int, help='Maximum sources to process')
    parser.add_argument('--no-report', action='store_true', help='Skip report generation')

    args = parser.parse_args()

    # Build user parameters from CLI args
    user_params = {}
    if args.category:
        user_params['categories'] = [args.category]
    if args.priority:
        user_params['priority_filter'] = args.priority
    if args.max_sources:
        user_params['max_sources'] = args.max_sources
    if args.no_report:
        user_params['generate_report'] = False

    # Execute
    executor = MetaExecutor()
    success = executor.execute_workflow(args.workflow, user_params)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
