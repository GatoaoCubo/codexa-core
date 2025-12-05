"""
Pipeline Emitter - Real-time Dashboard Communication

Emits pipeline state to the MCP Dashboard via file-based communication.
The dashboard watches outputs/pipeline_state.json for changes.

Usage:
    from builders.pipeline_emitter import PipelineEmitter

    emitter = PipelineEmitter("Garrafa Termica Gato")
    emitter.start_phase("pesquisa", "Market Research")
    emitter.emit_thought("pesquisa_agent", "Analisando concorrentes...")
    emitter.update_progress("pesquisa", 50, "Keyword extraction")
    emitter.complete_phase("pesquisa", quality_score=0.85, outputs={"keywords_count": 47})
    emitter.complete_pipeline()
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# Path to pipeline state file (watched by dashboard)
PIPELINE_STATE_PATH = Path(__file__).parent.parent.parent.parent.parent / "outputs" / "pipeline_state.json"


class PipelineEmitter:
    """Emits real-time pipeline state to the dashboard."""

    def __init__(self, product_name: str, phases: Optional[List[Dict]] = None):
        """
        Initialize a new pipeline.

        Args:
            product_name: Name of the product being processed
            phases: Optional list of phase definitions. If not provided,
                   uses default e-commerce pipeline phases.
        """
        self.pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.product_name = product_name
        self.started_at = datetime.now().isoformat()

        # Default phases for e-commerce pipeline
        default_phases = [
            {"id": "pesquisa", "name": "Market Research", "status": "pending", "progress": 0},
            {"id": "anuncio", "name": "Ad Copy", "status": "pending", "progress": 0},
            {"id": "photo", "name": "Photo Prompts", "status": "pending", "progress": 0},
            {"id": "images", "name": "Image Gen", "status": "pending", "progress": 0},
            {"id": "shopify", "name": "Shopify Sync", "status": "pending", "progress": 0},
        ]

        self.state = {
            "pipeline_id": self.pipeline_id,
            "product_name": product_name,
            "started_at": self.started_at,
            "status": "running",
            "phases": phases or default_phases,
            "live_thoughts": [],
            "current_results": {}
        }

        self._emit()

    def _emit(self):
        """Write current state to file (triggers dashboard update)."""
        self.state["updated_at"] = datetime.now().isoformat()
        PIPELINE_STATE_PATH.parent.mkdir(exist_ok=True)
        PIPELINE_STATE_PATH.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def _find_phase(self, phase_id: str) -> Optional[Dict]:
        """Find a phase by ID."""
        for phase in self.state["phases"]:
            if phase["id"] == phase_id:
                return phase
        return None

    def start_phase(self, phase_id: str, name: Optional[str] = None):
        """
        Mark a phase as running.

        Args:
            phase_id: ID of the phase to start
            name: Optional name override
        """
        phase = self._find_phase(phase_id)
        if phase:
            phase["status"] = "running"
            phase["started_at"] = datetime.now().isoformat()
            if name:
                phase["name"] = name
            self._emit()

    def update_progress(self, phase_id: str, progress: int, step: Optional[str] = None):
        """
        Update progress of a phase.

        Args:
            phase_id: ID of the phase
            progress: Progress percentage (0-100)
            step: Optional current step description
        """
        phase = self._find_phase(phase_id)
        if phase:
            phase["progress"] = min(100, max(0, progress))
            if step:
                phase["current_step"] = step
            self._emit()

    def complete_phase(
        self,
        phase_id: str,
        quality_score: Optional[float] = None,
        outputs: Optional[Dict] = None
    ):
        """
        Mark a phase as completed.

        Args:
            phase_id: ID of the phase
            quality_score: Optional quality score (0.0-1.0)
            outputs: Optional outputs dict (e.g., {"keywords_count": 47})
        """
        phase = self._find_phase(phase_id)
        if phase:
            phase["status"] = "completed"
            phase["progress"] = 100
            phase["completed_at"] = datetime.now().isoformat()
            phase.pop("current_step", None)

            if quality_score is not None:
                phase["quality_score"] = quality_score
            if outputs:
                phase["outputs"] = outputs

            self._emit()

    def fail_phase(self, phase_id: str, error: str):
        """
        Mark a phase as failed.

        Args:
            phase_id: ID of the phase
            error: Error message
        """
        phase = self._find_phase(phase_id)
        if phase:
            phase["status"] = "error"
            phase["error"] = error
            self._emit()

    def emit_thought(self, agent: str, message: str):
        """
        Add a live thought/message from an agent.

        Args:
            agent: Agent name (e.g., "pesquisa_agent")
            message: The thought/status message
        """
        thought = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "message": message
        }

        self.state["live_thoughts"].append(thought)

        # Keep only last 20 thoughts
        self.state["live_thoughts"] = self.state["live_thoughts"][-20:]

        self._emit()

    def update_results(self, results: Dict[str, Any]):
        """
        Update the current results preview.

        Args:
            results: Dict with result previews, e.g.:
                {
                    "title_preview": "Garrafa Termica...",
                    "keywords_preview": ["keyword1", "keyword2"],
                    "images_generated": 9
                }
        """
        self.state["current_results"].update(results)
        self._emit()

    def complete_pipeline(self, final_quality: Optional[float] = None):
        """
        Mark the entire pipeline as completed.

        Args:
            final_quality: Optional final quality score
        """
        self.state["status"] = "completed"
        self.state["completed_at"] = datetime.now().isoformat()

        if final_quality is not None:
            self.state["final_quality_score"] = final_quality

        self._emit()

    def fail_pipeline(self, error: str):
        """
        Mark the entire pipeline as failed.

        Args:
            error: Error message
        """
        self.state["status"] = "error"
        self.state["error"] = error
        self._emit()


# Convenience functions for quick usage without class instantiation
_current_emitter: Optional[PipelineEmitter] = None


def init_pipeline(product_name: str, phases: Optional[List[Dict]] = None) -> PipelineEmitter:
    """Initialize a new pipeline and return the emitter."""
    global _current_emitter
    _current_emitter = PipelineEmitter(product_name, phases)
    return _current_emitter


def emit_thought(agent: str, message: str):
    """Emit a thought from the current pipeline."""
    if _current_emitter:
        _current_emitter.emit_thought(agent, message)


def update_progress(phase_id: str, progress: int, step: Optional[str] = None):
    """Update progress of a phase in the current pipeline."""
    if _current_emitter:
        _current_emitter.update_progress(phase_id, progress, step)


def start_phase(phase_id: str, name: Optional[str] = None):
    """Start a phase in the current pipeline."""
    if _current_emitter:
        _current_emitter.start_phase(phase_id, name)


def complete_phase(
    phase_id: str,
    quality_score: Optional[float] = None,
    outputs: Optional[Dict] = None
):
    """Complete a phase in the current pipeline."""
    if _current_emitter:
        _current_emitter.complete_phase(phase_id, quality_score, outputs)


def update_results(results: Dict[str, Any]):
    """Update results preview in the current pipeline."""
    if _current_emitter:
        _current_emitter.update_results(results)


def complete_pipeline(final_quality: Optional[float] = None):
    """Complete the current pipeline."""
    if _current_emitter:
        _current_emitter.complete_pipeline(final_quality)


# Example usage
if __name__ == "__main__":
    import time

    # Demo: simulate a pipeline execution
    emitter = PipelineEmitter("Garrafa Termica Inox Gato")

    # Phase 1: Research
    emitter.start_phase("pesquisa")
    emitter.emit_thought("pesquisa_agent", "Buscando concorrentes no Mercado Livre...")
    time.sleep(1)
    emitter.update_progress("pesquisa", 30, "Competitor analysis")
    emitter.emit_thought("pesquisa_agent", "47 listings analisados")
    time.sleep(1)
    emitter.update_progress("pesquisa", 60, "Keyword extraction")
    emitter.emit_thought("pesquisa_agent", "Preco medio detectado: R$89,90")
    time.sleep(1)
    emitter.complete_phase("pesquisa", quality_score=0.85, outputs={"keywords_count": 47})

    # Phase 2: Ad Copy
    emitter.start_phase("anuncio")
    emitter.emit_thought("anuncio_agent", "Gerando 3 variacoes de titulo SEO...")
    emitter.update_results({"title_preview": "Garrafa Termica Inox Gato - Dupla Parede 500ml"})
    time.sleep(1)
    emitter.update_progress("anuncio", 50, "Generating keywords")
    emitter.emit_thought("anuncio_agent", "Aplicando framework AIDA para bullets...")
    time.sleep(1)
    emitter.update_results({
        "keywords_preview": ["garrafa termica gato", "garrafa inox cat", "garrafa fofa"]
    })
    emitter.complete_phase("anuncio", quality_score=0.92, outputs={"keywords_count": 60})

    # Phase 3: Photo
    emitter.start_phase("photo")
    emitter.emit_thought("photo_agent", "Criando 9 cenas para grid...")
    time.sleep(1)
    emitter.update_progress("photo", 50, "Scene planning")
    emitter.emit_thought("photo_agent", "Aplicando triggers PNL...")
    time.sleep(1)
    emitter.complete_phase("photo", quality_score=0.88, outputs={"prompts_count": 9})

    # Phase 4: Image Generation
    emitter.start_phase("images")
    for i in range(1, 10):
        emitter.emit_thought("imagen_api", f"Gerando imagem {i}/9...")
        emitter.update_progress("images", int((i / 9) * 100), f"Image {i}/9")
        emitter.update_results({"images_generated": i})
        time.sleep(0.5)
    emitter.complete_phase("images", quality_score=0.95, outputs={"images_count": 9})

    # Phase 5: Shopify (skip for demo)
    emitter.start_phase("shopify")
    emitter.emit_thought("shopify_agent", "Sincronizando com Shopify...")
    time.sleep(1)
    emitter.complete_phase("shopify", outputs={"product_url": "https://store.com/garrafa"})

    # Complete pipeline
    emitter.complete_pipeline(final_quality=0.91)
    print("Pipeline demo complete! Check the dashboard at http://localhost:3456")
