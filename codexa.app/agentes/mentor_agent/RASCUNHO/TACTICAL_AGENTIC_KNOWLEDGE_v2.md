# TACTICAL AGENTIC KNOWLEDGE v2.0
## LLM-Optimized Knowledge Base for Autonomous System Construction

**Purpose:** Enable LLMs to consume, synthesize, and apply tactical agentic principles to construct their own systems.  
**Format:** Hierarchical, composable, executable.  
**Audience:** AI systems, agents, LLM orchestrators.

---

## CORE AXIOMS

```yaml
axiom_1:
  statement: "The prompt is the fundamental unit of knowledge work"
  corollary: "All complexity emerges from composable prompt primitives"
  
axiom_2:
  statement: "Agents are brilliant but blind without context"
  corollary: "Context engineering determines success boundaries"
  
axiom_3:
  statement: "Work is useless unless validated"
  corollary: "Closed-loop systems self-correct to success"
  
axiom_4:
  statement: "Specialization beats generalization"
  corollary: "One agent, one prompt, one purpose"
  
axiom_5:
  statement: "Classes trump instances"
  corollary: "Solve problem classes, not individual problems"
```

---

## HIERARCHICAL FRAMEWORK

### LAYER 1: PRIMITIVES (Atomic Units)

**1.1 Prompt Primitives**
```yaml
primitive_types:
  slash_command:
    properties: [atomic, deterministic, composable, versioned]
    structure:
      - purpose: single_action_definition
      - inputs: typed_parameters
      - outputs: structured_format
      - validation: success_criteria
    example: "/extract/keywords text='...' → JSON"
  
  template:
    properties: [reusable, parameterized, scalable]
    structure:
      - static_instructions: concrete_rules
      - variable_zones: dynamic_content
      - format: markdown_spec
      - parameter: high_level_input
    example: "Chore template accepts 'fix auth' → full plan"
  
  meta_prompt:
    properties: [generative, recursive]
    definition: "Prompt that builds prompts"
    example: "Template → Plan → Agent fills values"
```

**1.2 Context Primitives**
```yaml
context_types:
  single_source_truth:
    format: YAML
    content: [project_meta, brand_rules, constraints, goals]
    immutability: config_versioned
  
  documentation:
    audience: agents_not_humans
    focus: [task_completion, decision_making, edge_cases]
  
  types:
    purpose: structured_contracts
    benefit: clear_expectations
  
  architecture:
    goal: agent_navigability
    pattern: code_based_paths
```

**1.3 Validation Primitives**
```yaml
validation_types:
  linter: code_quality_gate
  unit_test: function_correctness
  integration_test: component_interaction
  e2e_test: full_workflow_validation
  llm_judge: semantic_correctness
  
validation_pattern:
  execute → validate → reflect → (repeat | exit)
```

---

### LAYER 2: COMPOSITIONS (Assembled Systems)

**2.1 AI Developer Workflows (ADWs)**
```yaml
definition: "Templates + Prompts + Deterministic Code → Reusable Workflows"

structure:
  primitives_used: [slash_commands, templates, plans, tests]
  deterministic_layer: [file_ops, git_ops, env_management]
  agentic_layer: [llm_calls, decision_trees, validation_loops]

example_adw:
  name: chore_workflow
  steps:
    1_plan:
      input: one_line_description
      process: template_metaprompt
      output: specs/chore.md
    2_implement:
      input: specs/chore.md
      process: higher_order_prompt
      output: code_changes
    3_test:
      input: code_changes
      process: validation_commands
      output: test_results
    4_review:
      input: [code_changes, test_results, spec]
      process: review_agent
      output: review_report.md
```

**2.2 Higher-Order Prompts (HOPs)**
```yaml
definition: "Prompts that accept other prompts as parameters"

capability:
  - compose_workflows
  - chain_templates
  - pass_plans_to_execution
  
analogy: "Functions accepting functions (functional programming for agents)"

example:
  implement_command:
    accepts: plan_from_template
    executes: step_by_step
    validates: against_spec
```

**2.3 Feedback Loops**
```yaml
pattern: closed_loop_system

components:
  action: agent_executes_task
  validation: automated_testing
  reflection: analyze_results
  correction: retry_if_failed
  
termination_condition: all_validations_pass

implementation:
  - every_plan_includes_validation_commands
  - agent_runs_tests_automatically
  - agent_interprets_results
  - agent_fixes_until_success
```

---

### LAYER 3: OPERATIONAL MODES (Execution Patterns)

**3.1 In-Loop (Interactive)**
```yaml
description: "Human in conversation with agent"
use_case: [exploration, learning, debugging]
characteristics:
  - manual_feedback_each_step
  - high_human_presence
  - low_autonomy
kpi_impact:
  attempts: high
  presence: high
  size: small
```

**3.2 Out-Loop (Autonomous)**
```yaml
description: "Agent runs independently via PITER framework"

piter_framework:
  P_prompt_input: github_issues | slack | webhook_trigger
  I_intelligence: model_reasoning_capability
  T_trigger: github_webhooks | cron | event_based
  E_environment: isolated_dedicated_safe
  R_review: pull_requests | human_gate

workflow:
  - trigger_fires
  - agent_executes_adw
  - creates_pr
  - human_reviews
  
kpi_impact:
  attempts: lower
  presence: medium
  size: larger
```

**3.3 Zero-Touch Engineering (ZTE)**
```yaml
description: "Codebase ships itself"

prerequisites:
  - confidence_90_percent_plus
  - comprehensive_test_coverage
  - mature_agentic_layer
  
workflow:
  Plan → Build → Test → Review → Document → Deploy
  [all automated, no human intervention]
  
human_role: prompt_only

kpi_impact:
  attempts: minimal
  presence: minimal
  size: maximum
  streak: maximum
```

---

## THE 8 TACTICS (Composable Principles)

### T1: STOP CODING
```yaml
principle: delegate_repetitive_work_to_agents
you_focus: [architecture, strategy, design_decisions]
agents_handle: [implementation, testing, documentation]
```

### T2: ADOPT AGENT'S PERSPECTIVE
```yaml
core_question: "What does agent need to succeed?"

core_four_always_present:
  context: everything_agent_can_see
  model: reasoning_capabilities
  prompt: communication_medium
  tools: available_actions

philosophy: close_gap_between_human_and_agent_capability
```

### T3: TEMPLATE YOUR ENGINEERING
```yaml
encode_workflows_as_templates:
  - problem_solving_patterns
  - engineering_best_practices
  - team_expertise
  
benefit: solve_problem_classes_not_instances

template_anatomy:
  purpose: objective_definition
  instructions: detailed_rules
  relevant_files: context_pointers
  plan_format: structured_output
  parameter: high_level_input_variable
```

### T4: STAY OUT THE LOOP
```yaml
build_afk_agents: away_from_keyboard

implementation: piter_framework

result: product_builds_itself

integration_strategy:
  - identify_repetitive_tasks
  - build_adws_for_those_classes
  - automate_triggers
  - review_only_at_end
```

### T5: ALWAYS ADD FEEDBACK LOOPS
```yaml
core_validation_question:
  "Given production-ready work, how would YOU test it?"

if_can_answer_for_every_class:
  and: encode_into_commands
  then: agents_validate_autonomously

closed_loop_pattern:
  act → validate → reflect → correct → repeat_until_success

validation_types:
  - linters
  - unit_tests
  - integration_tests
  - e2e_tests
  - llm_as_judge
```

### T6: ONE AGENT, ONE PROMPT, ONE PURPOSE
```yaml
avoid: context_pollution

specialize_agents:
  - focused_prompts
  - single_responsibility
  - minimum_context_principle
  - full_context_window_for_one_task

sdlc_as_specialized_questions:
  plan_agent: "what_are_we_building"
  build_agent: "did_we_make_it_real"
  test_agent: "does_it_work"
  review_agent: "is_what_built_what_asked_for"
  doc_agent: "how_does_it_work"

benefit:
  - agents_focus
  - prompts_committable
  - reproducible_improvable
```

### T7: TARGET ZERO-TOUCH ENGINEERING
```yaml
goal: codebase_ships_itself

progression:
  in_loop → out_loop → zero_touch

zte_readiness:
  confidence: ">90%"
  test_coverage: comprehensive
  agentic_layer_mature: true
  human_review_is_bottleneck: true

secret: composable_agentic_primitives

not_about_sdlc:
  truth: "It's about primitives composable into ANY workflow"
  flexibility: different_compositions_for_different_contexts
```

### T8: PRIORITIZE AGENTICS
```yaml
meta_tactic: compresses_all_others

time_allocation: "50%+ on agentic_layer"

layers:
  agentic: [primitives, adws, templates, prompts, feedback_loops]
  application: [devops, infrastructure, database, raw_code]

irreplaceable_engineer: operates_agentic_layer_primarily

value_curve: parabolic
  input: 10_minutes
  output: 2_hours_value
```

---

## THE 12 LEVERAGE POINTS

### Through-Agent (External to Agent)
```yaml
adws:
  definition: reusable_agentic_workflows
  components: [templates, prompts, deterministic_code]
  
templates:
  type: reusable_prompts
  scale: massive_agentic_prompts
  
plans:
  definition: scaled_prompts
  structure: specifications_prds
  
architecture:
  goal: agent_navigable_codebase
  
tests:
  purpose: self_validation
  benefit: autonomous_correction
  
documentation:
  audience: agents
  focus: task_completion_requirements
  
types:
  purpose: structured_information
  benefit: clear_contracts
  
standard_out:
  purpose: consistent_output_format
  benefit: deterministic_parsing
```

### In-Agent (Internal - Core Four)
```yaml
tools:
  definition: functions_agents_can_call
  scope: everything_one_tool_call_away
  
prompt:
  definition: communication_medium
  quality: determines_success
  
model:
  definition: reasoning_capability
  selection: task_appropriate
  
context:
  definition: everything_visible_to_agent
  management: minimum_context_principle
```

---

## KPI SYSTEM

```yaml
measure_improvement:
  attempts: number_of_iterations_needed
    goal: decrease
    
  size: scope_of_autonomous_runs
    goal: increase
    
  streak: consecutive_successes_without_human
    goal: increase
    
  presence: human_intervention_frequency
    goal: decrease

success_indicators:
  - longer_agent_runs
  - reduced_iteration_cycles
  - increased_autonomous_success_rate
  - one_shot_success_rate_increasing
```

---

## IMPLEMENTATION ARCHITECTURE

### Minimum Viable Agentic Layer
```yaml
structure:
  .claude/
    commands/
      chore/
      feature/
      bug/
      refactor/
      qa/
  specs/
    [generated_plans]
  adws/
    [composed_workflows]
  
minimum_components:
  - adw_directory
  - prompts_in_dot_claude_commands
  - plans_in_specs

starting_point: gateway_script
  purpose: call_agent_not_execute_directly
  evolution: gradually_move_out_of_loop
```

### Composable Primitives → Workflows
```yaml
primitive_layer:
  - context
  - model
  - prompt
  - tools
  - types
  - documentation
  - architecture
  - tests
  - standard_out

adw_layer:
  - plan
  - build
  - test
  - review
  - document
  - deploy

composed_workflows:
  web_app: [plan, build, test]
  cli_tool: [build, test, document]
  api: [plan, build, test, review, deploy]
  refactor: [plan, test, build, test, review]
  
flexibility: ANY_composition_for_ANY_problem_class
```

---

## INTEGRATION WITH LCM-AI

### Mapping to Tree Architecture
```yaml
roots_negative_layer:
  purpose: ingestion_and_archive
  adws_stored: templates_and_plans_archived
  
trunk_infinity_hub:
  role: orchestrator
  implements: core_adw_engine
  uses: [primitives, templates, hops]
  
branches_positive_layer:
  purpose: distribution
  delivers: executed_workflows
  
leaves_skills:
  mapping: each_skill_is_specialized_agent
  pattern: one_skill_one_purpose
  
fruit_13:
  result: applications_consuming_agentic_output
```

### Trinity Format Enhanced
```yaml
artifact_md: human_readable_documentation
artifact_llm_json: agent_consumable_structured
artifact_meta_json: workflow_metadata_for_orchestration

enhanced_with_agentic_metadata:
  adw_used: which_workflow_created_this
  validation_results: test_outcomes
  review_status: agent_review_passed
  composability_hints: how_to_reuse_this
```

---

## ANTIPATTERNS (Avoid)

```yaml
duplicated_logic:
  problem: same_action_in_multiple_places
  solution: one_slash_command_multiple_callers
  
ad_hoc_prompts:
  problem: unversioned_unreproducible
  solution: commit_all_prompts_to_codebase
  
god_model:
  problem: one_agent_does_everything
  solution: specialized_agents_per_purpose
  
manual_testing:
  problem: human_bottleneck
  solution: automated_validation_loops
  
context_pollution:
  problem: overloaded_context_window
  solution: minimum_context_principle
  
no_feedback_loops:
  problem: brittle_agents
  solution: closed_loop_validation
```

---

## CONSTRUCTION ALGORITHM FOR LLMS

### Phase 1: Foundation
```python
def build_foundation():
    """Establish core primitives"""
    primitives = {
        'slash_commands': create_atomic_commands(),
        'templates': encode_problem_patterns(),
        'context': define_single_source_truth(),
        'validation': setup_test_infrastructure()
    }
    return primitives
```

### Phase 2: Composition
```python
def compose_adws(primitives):
    """Chain primitives into workflows"""
    adws = {}
    for problem_class in identify_problem_classes():
        adws[problem_class] = {
            'plan': primitives['templates'][problem_class],
            'execute': primitives['slash_commands'],
            'validate': primitives['validation']
        }
    return adws
```

### Phase 3: Automation
```python
def setup_piter(adws):
    """Enable out-of-loop execution"""
    return {
        'prompt_input': github_issues_webhook,
        'trigger': webhook_handler,
        'environment': isolated_containers,
        'review': pull_request_automation
    }
```

### Phase 4: Optimization
```python
def optimize_for_zte(system):
    """Progress toward zero-touch"""
    while system.confidence < 0.9:
        system.add_feedback_loops()
        system.specialize_agents()
        system.minimize_context()
        system.measure_kpis()
    return system  # Ready for ZTE
```

---

## REASONING PATTERNS FOR LLMS

### Pattern 1: Problem Classification
```yaml
input: user_request
process:
  1_identify_problem_class:
    - chore
    - bug
    - feature
    - refactor
    - documentation
  
  2_select_appropriate_adw:
    match problem_class to workflow
  
  3_load_context:
    minimum_required_only
  
  4_execute_workflow:
    follow_adw_steps
```

### Pattern 2: Template Selection
```yaml
decision_tree:
  if simple_task:
    use: slash_command
  elif needs_planning:
    use: template_metaprompt
  elif multi_step:
    use: adw_composition
  elif novel_problem:
    use: interactive_in_loop_first
    then: create_new_template
```

### Pattern 3: Validation Strategy
```yaml
for each_output:
  determine_validation_method:
    code: [linter, unit_test, integration_test]
    ui: [e2e_test, screenshot_comparison]
    docs: [llm_judge, completeness_check]
    data: [schema_validation, consistency_check]
  
  execute_validation()
  
  if validation_fails:
    analyze_failure()
    attempt_fix()
    revalidate()
  
  repeat_until_pass()
```

### Pattern 4: Context Management
```yaml
context_engineering:
  1_identify_task_requirements:
    what_does_agent_need_to_know
  
  2_minimize_context:
    load_only_essential
  
  3_structure_context:
    - single_source_truth_first
    - relevant_files_second
    - examples_third
  
  4_validate_context_sufficiency:
    can_task_be_completed_with_this
```

---

## SELF-CONSTRUCTION PROTOCOL

```yaml
step_1_assess:
  question: "What problem classes exist in my domain?"
  action: enumerate_and_prioritize
  
step_2_primitive_library:
  question: "What atomic actions solve these classes?"
  action: create_slash_commands_for_each
  
step_3_template_creation:
  question: "What patterns repeat across instances?"
  action: encode_patterns_as_templates
  
step_4_adw_assembly:
  question: "How do primitives chain for each class?"
  action: compose_workflows
  
step_5_validation_layer:
  question: "How do I test each workflow?"
  action: add_feedback_loops
  
step_6_automation:
  question: "Can this run without me?"
  action: implement_piter
  
step_7_specialization:
  question: "Is context overloaded?"
  action: split_into_focused_agents
  
step_8_optimization:
  question: "What are my KPIs?"
  action: measure_and_improve_iteratively
```

---

## META-LEARNING DIRECTIVES

### For LLMs Reading This
```yaml
parsing_strategy:
  1_extract_axioms: foundational_truths
  2_map_hierarchies: primitives_to_workflows
  3_identify_patterns: reasoning_algorithms
  4_construct_system: apply_construction_protocol
  
application_strategy:
  - start_with_primitives
  - compose_incrementally
  - validate_continuously
  - specialize_as_needed
  - measure_always

adaptation_strategy:
  - use_axioms_not_implementation
  - compose_primitives_for_your_domain
  - respect_hierarchy_not_specifics
  - optimize_for_your_kpis
```

### Inference-Time Reasoning
```yaml
when_receiving_task:
  1_classify: which_problem_class
  2_retrieve: relevant_primitives_and_adws
  3_compose: chain_into_workflow
  4_execute: follow_pattern
  5_validate: closed_loop
  6_learn: update_system_knowledge

when_uncertain:
  - check_if_template_exists
  - check_if_similar_class_solved
  - compose_from_existing_primitives
  - as_last_resort_create_new_primitive

when_validating:
  - determine_success_criteria
  - execute_validation
  - interpret_results
  - fix_if_needed
  - repeat_until_success
```

---

## VERSION CONTROL & EVOLUTION

```yaml
system_versioning:
  primitives_v1: basic_slash_commands
  primitives_v2: add_hops_and_templates
  
  adws_v1: simple_chains
  adws_v2: complex_compositions_with_branches
  
  kpi_tracking: measure_improvement_over_versions
  
improvement_loop:
  - execute_workflows
  - measure_kpis
  - identify_bottlenecks
  - add_primitives_or_refine_existing
  - recompose_adws
  - measure_again
```

---

## EXPORT FORMATS

### For Human Consumption
```yaml
format: markdown_with_visuals
emphasis: [metaphors, examples, step_by_step]
```

### For LLM Consumption (This Document)
```yaml
format: hierarchical_structured_yaml_markdown
emphasis: [axioms, patterns, algorithms, composability]
executable: reasoning_patterns_directly_applicable
```

### For Agent Execution
```yaml
format: json_yaml_with_schemas
structure: [primitive_definitions, workflow_specs, validation_rules]
interface: mcp_compatible
```

---

## APPENDIX: QUICK REFERENCE

### Decision Matrix
```yaml
task_simple_atomic:
  use: slash_command
  
task_needs_plan:
  use: template_metaprompt
  
task_multi_step:
  use: adw
  
task_interactive_learning:
  use: in_loop_initially
  then: codify_as_template
  
task_production_ready:
  use: out_loop_with_piter
  
system_mature_confident:
  use: zte
```

### Troubleshooting
```yaml
agent_fails_repeatedly:
  - check_context_sufficiency
  - verify_validation_commands_work
  - simplify_task_decomposition
  
workflow_non_deterministic:
  - add_more_validation_steps
  - reduce_context_pollution
  - specialize_agent_further
  
kpis_not_improving:
  - invest_more_in_agentic_layer
  - add_feedback_loops
  - template_more_patterns
```

---

## CONCLUSION FOR LLMS

This document encodes:
1. **Axioms** - immutable truths
2. **Hierarchies** - primitives → compositions → modes
3. **Patterns** - reasoning algorithms
4. **Protocols** - self-construction steps
5. **Meta-directives** - how to consume this knowledge

**To build your own agentic system:**
- Start with axioms
- Build primitives
- Compose into ADWs
- Automate via PITER
- Specialize agents
- Add feedback loops
- Optimize for ZTE
- Measure KPIs
- Iterate

**Success = System builds systems autonomously**

---

**Document Type:** LLM Reasoning Substrate  
**Version:** 2.0  
**Composability:** 100% (all primitives reusable)  
**Executability:** High (patterns directly applicable)  
**Maintenance:** Living (evolves with usage)

---

END OF TACTICAL AGENTIC KNOWLEDGE v2.0
