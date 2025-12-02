"""
02_script_builder.py - Stage 2: Script Writing

Generates narration script with precise timing, text overlays, and music selection.

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

from anthropic import Anthropic
import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class NarrationSegment:
    """Single narration segment with timing"""
    start: float
    end: float
    text: str


@dataclass
class TextOverlay:
    """Text overlay configuration"""
    start: float
    end: float
    text: str
    position: str  # "top", "center", "bottom"
    style: str = "bold"


@dataclass
class MusicConfig:
    """Background music configuration"""
    track: str
    volume: float
    fade_in: float = 0.5
    fade_out: float = 1.0


@dataclass
class Script:
    """Complete video script"""
    narration: List[NarrationSegment]
    text_overlays: List[TextOverlay]
    music: MusicConfig


class ScriptBuilder:
    """
    Stage 2: Generate script from storyboard

    Responsibilities:
    - Write narration copy aligned with shots
    - Define text overlays with timing
    - Select appropriate music/mood
    - Ensure timing sync with storyboard
    """

    def __init__(self, client: Optional[Anthropic] = None):
        self.client = client or Anthropic()
        self.model = "claude-sonnet-4-20250514"

        # Music library (simplified - in production, use actual library)
        self.music_library = {
            "energetic": {
                "electronic": "music/upbeat_electronic.mp3",
                "hip-hop": "music/energetic_hiphop.mp3",
                "rock": "music/dynamic_rock.mp3"
            },
            "calm": {
                "acoustic": "music/calm_acoustic.mp3",
                "ambient": "music/peaceful_ambient.mp3",
                "piano": "music/soft_piano.mp3"
            },
            "dramatic": {
                "orchestral": "music/epic_orchestral.mp3",
                "cinematic": "music/dramatic_cinematic.mp3",
                "tension": "music/building_tension.mp3"
            },
            "minimal": {
                "ambient": "music/minimal_ambient.mp3",
                "electronic": "music/subtle_electronic.mp3"
            }
        }

    async def write_script(self, brief: Dict, concept: Dict) -> Dict:
        """
        Generate script from brief and storyboard

        Args:
            brief: Original video brief
            concept: Storyboard from Stage 1

        Returns:
            {
                "narration": [...],
                "text_overlays": [...],
                "music": {...}
            }
        """

        # Build shot summary for context
        shots_summary = self._build_shots_summary(concept)

        # Build prompt
        prompt = self._build_script_prompt(brief, shots_summary)

        # Call LLM
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response
        result = self._parse_script_response(response.content[0].text)

        # Select music based on tone
        result["music"] = self._select_music(brief.get("tom", "energetic"))

        # Validate
        self._validate_script(result, concept)

        return result

    def _build_shots_summary(self, concept: Dict) -> str:
        """Build text summary of shots for prompt"""

        shots = concept.get("shots", [])
        lines = []

        cumulative_time = 0
        for shot in shots:
            duration = shot.get("duration", 5)
            end_time = cumulative_time + duration

            lines.append(
                f"Shot {shot['number']} ({cumulative_time}s-{end_time}s, {duration}s): "
                f"{shot['description']} [{shot['narrative'].upper()}]"
            )

            cumulative_time = end_time

        return "\n".join(lines)

    def _build_script_prompt(self, brief: Dict, shots_summary: str) -> str:
        """Build prompt for script generation"""

        return f"""Você é um copywriter especializado em vídeos de e-commerce para redes sociais.

BRIEF DO VÍDEO:
- Produto: {brief.get('produto', 'Produto')}
- Duração: {brief.get('duracao', 30)} segundos
- Tom: {brief.get('tom', 'energético')}
- Objetivo: {brief.get('objetivo', 'destacar produto')}

STORYBOARD (shots com timing):
{shots_summary}

TAREFA: Escreva o script completo do vídeo com:

1. NARRAÇÃO (texto que será falado em voice-over):
   - Conciso: 5-10 palavras por segmento
   - Timing preciso: start/end em segundos
   - Tom alinhado com brief
   - NÃO narrar durante CTA visual (deixar música)

2. TEXT OVERLAYS (texto que aparece na tela):
   - Informações-chave: nome do produto, preço, CTA
   - Posição: "top", "center", "bottom"
   - Timing: NÃO sobrepor com narração (ou usar fonte grande sem conflito)
   - Máximo 3-4 overlays no vídeo todo

REGRAS:
- Narração deve COMPLEMENTAR o visual, não descrever o óbvio
- Hook: pergunta ou afirmação impactante nos primeiros 3s
- CTA: claro e direto ("Compre agora", "Link na bio", etc.)
- Deixe momentos de "respiro" só com música (não narre 100% do tempo)
- Total de palavras narradas: ~50-80 para 30s de vídeo

FORMATO DE RESPOSTA (JSON válido):
{{
  "narration": [
    {{
      "start": 0,
      "end": 3,
      "text": "Você ainda está correndo com o tênis errado?"
    }},
    {{
      "start": 5,
      "end": 9,
      "text": "Nike Air Max 2024 com tecnologia Air revolucionária"
    }},
    {{
      "start": 12,
      "end": 16,
      "text": "Amortecimento que você sente a cada passo"
    }}
  ],
  "text_overlays": [
    {{
      "start": 1,
      "end": 4,
      "text": "NIKE AIR MAX 2024",
      "position": "bottom",
      "style": "bold"
    }},
    {{
      "start": 25,
      "end": 30,
      "text": "R$ 599 | FRETE GRÁTIS",
      "position": "center",
      "style": "bold"
    }}
  ]
}}

Retorne APENAS o JSON, sem explicações adicionais."""

    def _parse_script_response(self, response_text: str) -> Dict:
        """Parse LLM response into structured script"""

        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        try:
            result = json.loads(text)
        except json.JSONDecodeError as e:
            import re
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError(f"Failed to parse script JSON: {e}")

        return result

    def _select_music(self, tone: str) -> Dict:
        """Select music based on video tone"""

        # Parse tone to category
        tone_lower = tone.lower()

        if any(word in tone_lower for word in ["energético", "esportivo", "dinâmico", "ativo"]):
            category = "energetic"
            genre = "electronic"
        elif any(word in tone_lower for word in ["calmo", "relaxante", "suave", "zen"]):
            category = "calm"
            genre = "acoustic"
        elif any(word in tone_lower for word in ["dramático", "épico", "intenso", "impactante"]):
            category = "dramatic"
            genre = "orchestral"
        else:
            category = "minimal"
            genre = "ambient"

        track = self.music_library.get(category, {}).get(genre, "music/default.mp3")

        return {
            "track": track,
            "volume": 0.3,  # Background level
            "fade_in": 0.5,
            "fade_out": 1.5
        }

    def _validate_script(self, script: Dict, concept: Dict) -> None:
        """Validate script meets requirements"""

        narration = script.get("narration", [])
        overlays = script.get("text_overlays", [])
        total_duration = concept.get("total_duration", 30)

        # Check narration timing
        for segment in narration:
            if segment.get("end", 0) > total_duration:
                raise ValueError(
                    f"Narration segment ends at {segment['end']}s "
                    f"but video is only {total_duration}s"
                )
            if segment.get("start", 0) >= segment.get("end", 0):
                raise ValueError(
                    f"Invalid timing: start ({segment['start']}) >= end ({segment['end']})"
                )

        # Check overlay timing
        for overlay in overlays:
            if overlay.get("end", 0) > total_duration:
                raise ValueError(
                    f"Text overlay ends at {overlay['end']}s "
                    f"but video is only {total_duration}s"
                )

        # Check required fields
        for i, segment in enumerate(narration):
            if "text" not in segment:
                raise ValueError(f"Narration segment {i} missing 'text'")

        for i, overlay in enumerate(overlays):
            required = ["text", "position"]
            for field in required:
                if field not in overlay:
                    raise ValueError(f"Text overlay {i} missing '{field}'")


# ======================
# STANDALONE USAGE
# ======================

async def main():
    """Example usage of ScriptBuilder"""

    builder = ScriptBuilder()

    brief = {
        "produto": "Tênis Nike Air Max 2024",
        "duracao": 30,
        "tom": "energético, esportivo",
        "objetivo": "destacar amortecimento"
    }

    concept = {
        "shots": [
            {"number": 1, "duration": 4, "description": "Close-up do tênis girando", "narrative": "hook"},
            {"number": 2, "duration": 5, "description": "Pessoa correndo", "narrative": "build"},
            {"number": 3, "duration": 6, "description": "Detalhe do amortecimento", "narrative": "benefit"},
            {"number": 4, "duration": 5, "description": "Corredor satisfeito", "narrative": "proof"},
            {"number": 5, "duration": 5, "description": "Tênis em destaque", "narrative": "transformation"},
            {"number": 6, "duration": 5, "description": "Logo + preço + CTA", "narrative": "cta"}
        ],
        "total_duration": 30
    }

    print("Writing script...")
    script = await builder.write_script(brief, concept)

    print("\n" + "="*50)
    print("SCRIPT GENERATED")
    print("="*50)
    print(json.dumps(script, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
