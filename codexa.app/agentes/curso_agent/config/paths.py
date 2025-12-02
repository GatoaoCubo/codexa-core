"""
Central path configuration for curso_agent
Single source of truth for all file system paths
"""

from pathlib import Path

# Project hierarchy
# __file__ = .../curso_agent/config/paths.py
# parent = .../curso_agent/config
# parent.parent = .../curso_agent
# parent.parent.parent = .../agentes
# parent.parent.parent.parent = .../codexa.app
# parent.parent.parent.parent.parent = .../lm.codexa (PROJECT_ROOT)
CURSO_AGENT_DIR = Path(__file__).parent.parent  # .../curso_agent
AGENTS_ROOT = CURSO_AGENT_DIR.parent  # .../agentes
CODEXA_APP = AGENTS_ROOT.parent  # .../codexa.app
PROJECT_ROOT = CODEXA_APP.parent  # .../lm.codexa

# curso_agent directories
PATH_CONFIG = CURSO_AGENT_DIR / "config"
PATH_CONTEXT = CURSO_AGENT_DIR / "context"
PATH_ISO_VECTORSTORE = CURSO_AGENT_DIR / "iso_vectorstore"
PATH_ARTIFACTS = CURSO_AGENT_DIR / "artifacts"
PATH_TEMPLATES = CURSO_AGENT_DIR / "templates"
PATH_BUILDERS = CURSO_AGENT_DIR / "builders"
PATH_VALIDATORS = CURSO_AGENT_DIR / "validators"
PATH_COMMANDS = CURSO_AGENT_DIR / "commands"
PATH_WORKFLOWS = CURSO_AGENT_DIR / "workflows"
PATH_PROMPTS = CURSO_AGENT_DIR / "prompts"
PATH_OUTPUTS = CURSO_AGENT_DIR / "outputs"

# Key files
PATH_PRIME = CURSO_AGENT_DIR / "PRIME.md"
PATH_README = CURSO_AGENT_DIR / "README.md"
PATH_INSTRUCTIONS = CURSO_AGENT_DIR / "INSTRUCTIONS.md"
PATH_SETUP = CURSO_AGENT_DIR / "SETUP.md"
PATH_VALIDATION_CHECKLIST = CURSO_AGENT_DIR / "VALIDATION_CHECKLIST.md"
PATH_TESTING_COMMANDS = CURSO_AGENT_DIR / "TESTING_COMMANDS.md"

# Registry
PATH_REGISTRY = AGENTS_ROOT / "51_AGENT_REGISTRY.json"

# Context files (curso modules)
CONTEXT_FILES = {
    "index": PATH_CONTEXT / "00_INDICE_CURSO_CODEXA.md",
    "module_01": PATH_CONTEXT / "01_MODULO_INTRODUCAO.md",
    "module_02": PATH_CONTEXT / "02_MODULO_ANUNCIOS.md",
    "module_03": PATH_CONTEXT / "03_MODULO_PESQUISA.md",
    "module_04": PATH_CONTEXT / "04_MODULO_MARCA.md",
    "module_05": PATH_CONTEXT / "05_MODULO_FOTOS.md",
    "module_06": PATH_CONTEXT / "06_MODULO_META_CONSTRUCAO.md",
    "faq": PATH_CONTEXT / "FAQ.md",
    "glossario": PATH_CONTEXT / "GLOSSARIO.md",
    "recursos": PATH_CONTEXT / "RECURSOS_EXTRAS.md",
}

# Hotmart integration HOPs
HOTMART_HOPS = {
    "integration_guide": PATH_ISO_VECTORSTORE / "21_hotmart_integration_guide.md",
    "video_upload": PATH_ISO_VECTORSTORE / "22_HOP_hotmart_video_upload.md",
    "checkout_config": PATH_ISO_VECTORSTORE / "23_HOP_hotmart_checkout_config.md",
    "club_structure": PATH_ISO_VECTORSTORE / "24_HOP_hotmart_club_structure.md",
}

# Artifacts
ARTIFACTS = {
    "master_instructions": PATH_ARTIFACTS / "MASTER_INSTRUCTIONS.md",
    "config_json": PATH_ARTIFACTS / "AGENT_CONFIGURATION.json",
    "deployment": PATH_ARTIFACTS / "DEPLOYMENT_GUIDE.md",
    "sales_strategy": PATH_ARTIFACTS / "ESTRATEGIA_VENDA_CURSO.md",
    "handoff": PATH_ARTIFACTS / "HANDOFF_TO_CURSO_AGENT.md",
    "readme": PATH_ARTIFACTS / "README.md",
}

# Validation
def validate_paths():
    """Validate that key paths exist"""
    missing = []

    # Check directories
    for path in [CURSO_AGENT_DIR, PATH_CONTEXT, PATH_ISO_VECTORSTORE, PATH_ARTIFACTS]:
        if not path.exists():
            missing.append(str(path))

    # Check key files
    for path in [PATH_PRIME, PATH_README, PATH_REGISTRY]:
        if not path.exists():
            missing.append(str(path))

    if missing:
        print(f"[WARN] Missing paths: {len(missing)}")
        for p in missing:
            print(f"  - {p}")
        return False

    print(f"[OK] All key paths validated")
    return True

if __name__ == "__main__":
    # Test path configuration
    print("=== CURSO AGENT PATH CONFIGURATION ===")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Curso Agent Dir: {CURSO_AGENT_DIR}")
    print(f"Context Files: {len(CONTEXT_FILES)}")
    print(f"Hotmart HOPs: {len(HOTMART_HOPS)}")
    print(f"Artifacts: {len(ARTIFACTS)}")
    print()
    validate_paths()
