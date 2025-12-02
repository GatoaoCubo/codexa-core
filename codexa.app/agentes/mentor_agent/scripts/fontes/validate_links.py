#!/usr/bin/env python3
"""
Validate all links in catalogo_fontes.json

This script validates:
1. URL accessibility (HTTP status codes)
2. Response times
3. SSL certificate validity
4. Broken links detection

Usage:
    python validate_links.py [--all] [--fonte FONTE_ID] [--priority PRIORITY]
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import argparse
import logging
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
MENTOR_ROOT = Path(__file__).parent.parent.parent
CATALOGO_PATH = MENTOR_ROOT / "FONTES" / "catalogo_fontes.json"
REPORTS_DIR = MENTOR_ROOT / "outputs" / "fontes_reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_catalogo() -> Dict:
    """Load catalogo_fontes.json"""
    with open(CATALOGO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_url(url: str) -> Dict:
    """Validate single URL"""
    result = {
        'url': url,
        'status': 'unknown',
        'status_code': None,
        'response_time': None,
        'error': None,
        'accessible': False
    }

    try:
        start_time = datetime.now()
        response = requests.head(url, timeout=10, allow_redirects=True)
        end_time = datetime.now()

        result['status_code'] = response.status_code
        result['response_time'] = (end_time - start_time).total_seconds()

        if 200 <= response.status_code < 300:
            result['status'] = 'ok'
            result['accessible'] = True
        elif 300 <= response.status_code < 400:
            result['status'] = 'redirect'
            result['accessible'] = True
            result['redirect_url'] = response.url
        elif 400 <= response.status_code < 500:
            result['status'] = 'client_error'
            result['error'] = f"Client error: {response.status_code}"
        elif 500 <= response.status_code < 600:
            result['status'] = 'server_error'
            result['error'] = f"Server error: {response.status_code}"

    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error'] = 'Request timeout'
    except requests.exceptions.SSLError as e:
        result['status'] = 'ssl_error'
        result['error'] = f'SSL error: {str(e)}'
    except requests.exceptions.ConnectionError:
        result['status'] = 'connection_error'
        result['error'] = 'Connection failed'
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)

    return result

def validate_fonte(fonte: Dict) -> Dict:
    """Validate all URLs for a fonte"""
    fonte_id = fonte['id']
    logger.info(f"🔗 Validating: {fonte_id}")

    results = {
        'fonte_id': fonte_id,
        'nome': fonte['nome'],
        'timestamp': datetime.now().isoformat(),
        'urls': [],
        'summary': {
            'total': 0,
            'accessible': 0,
            'broken': 0,
            'errors': 0
        }
    }

    # Validate main URL
    main_url = fonte['url_oficial']
    logger.info(f"  Checking main URL: {main_url}")
    main_result = validate_url(main_url)
    results['urls'].append({
        'type': 'main',
        'url': main_url,
        'result': main_result
    })

    # Validate specific URLs
    urls_especificas = fonte.get('urls_especificas', {})
    for topic, url in urls_especificas.items():
        logger.info(f"  Checking {topic}: {url}")
        url_result = validate_url(url)
        results['urls'].append({
            'type': 'specific',
            'topic': topic,
            'url': url,
            'result': url_result
        })

    # Calculate summary
    results['summary']['total'] = len(results['urls'])
    results['summary']['accessible'] = sum(1 for u in results['urls']
                                          if u['result']['accessible'])
    results['summary']['broken'] = sum(1 for u in results['urls']
                                      if u['result']['status'] in ['client_error', 'server_error'])
    results['summary']['errors'] = sum(1 for u in results['urls']
                                      if u['result']['status'] == 'error')

    # Log summary
    summary = results['summary']
    logger.info(f"  ✅ Accessible: {summary['accessible']}/{summary['total']}")
    if summary['broken'] > 0:
        logger.warning(f"  ⚠️  Broken links: {summary['broken']}")
    if summary['errors'] > 0:
        logger.error(f"  ❌ Errors: {summary['errors']}")

    return results

def generate_validation_report(all_results: List[Dict]) -> Path:
    """Generate validation report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"validation_report_{timestamp}.json"

    # Calculate overall summary
    total_fontes = len(all_results)
    total_urls = sum(r['summary']['total'] for r in all_results)
    total_accessible = sum(r['summary']['accessible'] for r in all_results)
    total_broken = sum(r['summary']['broken'] for r in all_results)
    total_errors = sum(r['summary']['errors'] for r in all_results)

    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_fontes': total_fontes,
            'total_urls': total_urls,
            'accessible': total_accessible,
            'broken': total_broken,
            'errors': total_errors,
            'success_rate': round(total_accessible / total_urls * 100, 2) if total_urls > 0 else 0
        },
        'results': all_results
    }

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Create markdown report
    md_report_file = REPORTS_DIR / f"validation_report_{timestamp}.md"
    md_content = f"""# FONTES Link Validation Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overall Summary

- 📊 Total fontes validated: {total_fontes}
- 🔗 Total URLs checked: {total_urls}
- ✅ Accessible: {total_accessible} ({report['summary']['success_rate']}%)
- ⚠️  Broken links: {total_broken}
- ❌ Errors: {total_errors}

## Fonte Details

"""

    for result in all_results:
        summary = result['summary']
        status_icon = "✅" if summary['broken'] == 0 and summary['errors'] == 0 else "⚠️"

        md_content += f"""### {status_icon} {result['nome']}

- **Fonte ID**: {result['fonte_id']}
- **URLs checked**: {summary['total']}
- **Accessible**: {summary['accessible']}
- **Broken**: {summary['broken']}
- **Errors**: {summary['errors']}

"""

        # Show broken links
        broken_urls = [u for u in result['urls']
                      if u['result']['status'] in ['client_error', 'server_error', 'error']]

        if broken_urls:
            md_content += "**Issues found**:\n\n"
            for u in broken_urls:
                md_content += f"- ❌ [{u.get('topic', 'main')}]({u['url']}): {u['result']['error']}\n"

            md_content += "\n"

    md_report_file.write_text(md_content, encoding='utf-8')

    logger.info(f"\n📄 Validation report: {report_file}")
    logger.info(f"📄 Markdown report: {md_report_file}")

    return report_file

def main():
    parser = argparse.ArgumentParser(description='Validate documentation links')
    parser.add_argument('--fonte', help='Validate specific fonte by ID')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                       help='Validate fontes by priority')
    parser.add_argument('--all', action='store_true', help='Validate all fontes')

    args = parser.parse_args()

    catalogo = load_catalogo()
    fontes_to_validate = []

    if args.fonte:
        fonte = next((f for f in catalogo['fontes'] if f['id'] == args.fonte), None)
        if fonte:
            fontes_to_validate = [fonte]
        else:
            logger.error(f"Fonte '{args.fonte}' not found")
            return

    elif args.priority:
        fontes_to_validate = [f for f in catalogo['fontes']
                             if f['priority'] == args.priority]

    elif args.all:
        fontes_to_validate = catalogo['fontes']

    else:
        logger.error("Please specify --fonte, --priority, or --all")
        return

    logger.info(f"🚀 Validating {len(fontes_to_validate)} fontes...\n")

    all_results = []
    for fonte in fontes_to_validate:
        result = validate_fonte(fonte)
        all_results.append(result)
        print()  # Empty line between fontes

    # Generate report
    report_file = generate_validation_report(all_results)

    # Print summary
    logger.info("\n" + "="*60)
    logger.info("VALIDATION COMPLETE")
    logger.info("="*60)

    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
        summary = report['summary']

    logger.info(f"✅ Success rate: {summary['success_rate']}%")
    logger.info(f"📊 {summary['accessible']}/{summary['total_urls']} URLs accessible")

    if summary['broken'] > 0:
        logger.warning(f"⚠️  {summary['broken']} broken links found")
    if summary['errors'] > 0:
        logger.error(f"❌ {summary['errors']} errors encountered")

    logger.info(f"\n📄 Full report: {report_file}")

if __name__ == '__main__':
    main()
