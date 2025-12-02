"""
03_visual_builder.py - Stage 3: Visual Prompt Engineering

Creates Runway/Pika prompts for each shot with camera, lighting, and style details.

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

from anthropic import Anthropic
import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class VisualPrompt:
    """Complete visual prompt for video generation"""
    shot_number: int
    duration: float
    runway_prompt: str
    style: str
    camera: Dict
    transition: str


class VisualBuilder:
    """
    Stage 3: Create video generation prompts

    Responsibilities:
    - Transform storyboard shots into Runway/Pika prompts
    - Define camera settings, lighting, movement
    - Ensure visual consistency across shots
    - Specify transitions between shots
    """

    def __init__(self, client: Optional[Anthropic] = None):
        self.client = client or Anthropic()
        self.model = "claude-haiku-20250305"  # Faster model for prompt generation

        # Style templates
        self.style_templates = {
            "energetic": {
                "lighting": "dynamic, high contrast, vibrant colors",
                "camera": "dynamic tracking, quick movements",
                "color_grade": "saturated, punchy",
                "mood": "exciting, active"
            },
            "calm": {
                "lighting": "soft, warm, natural",
                "camera": "slow, smooth, steady",
                "color_grade": "muted, warm tones",
                "mood": "peaceful, serene"
            },
            "dramatic": {
                "lighting": "low-key, rim lighting, shadows",
                "camera": "cinematic, slow reveal",
                "color_grade": "high contrast, cool tones",
                "mood": "intense, powerful"
            },
            "minimal": {
                "lighting": "clean, soft, neutral",
                "camera": "static, centered",
                "color_grade": "neutral, clean",
                "mood": "simple, elegant"
            },
            "cinematic": {
                "lighting": "golden hour, atmospheric",
                "camera": "smooth tracking, shallow depth",
                "color_grade": "filmic, natural",
                "mood": "storytelling, emotional"
            }
        }

        # Transition options
        self.transitions = {
            "energetic": ["quick-cut", "whip-pan", "jump-cut"],
            "calm": ["dissolve", "fade", "slow-cut"],
            "dramatic": ["hard-cut", "flash", "match-cut"],
            "minimal": ["cut", "fade"],
            "cinematic": ["cross-dissolve", "j-cut", "match-cut"]
        }

    async def create_prompts(self, concept: Dict, brief: Dict) -> List[Dict]:
        """
        Create visual prompts for all shots

        Args:
            concept: Storyboard from Stage 1
            brief: Original video brief

        Returns:
            List of visual prompt objects
        """

        shots = concept.get("shots", [])
        style_key = self._determine_style(brief.get("tom", "energetic"))
        style_template = self.style_templates.get(style_key, self.style_templates["energetic"])

        prompts = []

        for i, shot in enumerate(shots):
            # Generate prompt for this shot
            prompt_data = await self._generate_shot_prompt(
                shot=shot,
                brief=brief,
                style_template=style_template,
                is_first=(i == 0),
                is_last=(i == len(shots) - 1)
            )

            # Add transition (except for last shot)
            transition = "none"
            if i < len(shots) - 1:
                transition = self._select_transition(style_key, shot.get("narrative", ""))

            prompts.append({
                "shot_number": shot.get("number", i + 1),
                "duration": shot.get("duration", 5),
                "runway_prompt": prompt_data["prompt"],
                "style": f"{style_template['mood']}, {style_template['color_grade']}",
                "camera": prompt_data["camera"],
                "lighting": prompt_data["lighting"],
                "transition": transition
            })

        # Validate consistency
        self._validate_visual_consistency(prompts)

        return prompts

    def _determine_style(self, tone: str) -> str:
        """Determine style key from tone description"""

        tone_lower = tone.lower()

        if any(word in tone_lower for word in ["energético", "esportivo", "dinâmico"]):
            return "energetic"
        elif any(word in tone_lower for word in ["calmo", "relaxante", "suave"]):
            return "calm"
        elif any(word in tone_lower for word in ["dramático", "épico", "intenso"]):
            return "dramatic"
        elif any(word in tone_lower for word in ["minimalista", "clean", "simples"]):
            return "minimal"
        elif any(word in tone_lower for word in ["cinematográfico", "filmico"]):
            return "cinematic"
        else:
            return "energetic"  # Default

    async def _generate_shot_prompt(
        self,
        shot: Dict,
        brief: Dict,
        style_template: Dict,
        is_first: bool,
        is_last: bool
    ) -> Dict:
        """Generate detailed Runway prompt for a single shot"""

        prompt = f"""Você é um prompt engineer especializado em Runway Gen-3 para geração de vídeo.

SHOT DETAILS:
- Descrição: {shot.get('description', '')}
- Composição: {shot.get('composition', '')}
- Duração: {shot.get('duration', 5)} segundos
- Função narrativa: {shot.get('narrative', 'build')}
- Produto: {brief.get('produto', '')}

ESTILO DESEJADO:
- Iluminação: {style_template['lighting']}
- Câmera: {style_template['camera']}
- Color grade: {style_template['color_grade']}
- Mood: {style_template['mood']}

{'NOTA: Este é o PRIMEIRO shot (HOOK) - deve ser visualmente impactante!' if is_first else ''}
{'NOTA: Este é o ÚLTIMO shot (CTA) - deve ter espaço para texto overlay!' if is_last else ''}

TAREFA: Crie um prompt detalhado para Runway Gen-3 que gere este shot.

O prompt deve incluir:
1. Descrição visual clara e específica
2. Movimento/ação clara (se houver)
3. Estilo e qualidade (cinematic, 4k, professional, etc.)
4. Iluminação e mood
5. Composição de câmera (ângulo, movimento)

FORMATO DE RESPOSTA (JSON):
{{
  "prompt": "Detailed English prompt for Runway...",
  "camera": {{
    "angle": "low-angle | eye-level | high-angle | bird's-eye",
    "movement": "static | pan | tilt | tracking | zoom",
    "speed": "slow | normal | fast"
  }},
  "lighting": "description of lighting setup"
}}

IMPORTANTE:
- Prompt deve ser em INGLÊS (Runway funciona melhor com inglês)
- Máximo 100 palavras no prompt
- Seja específico mas não verboso
- Evite descrições abstratas

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return self._parse_prompt_response(response.content[0].text)

    def _parse_prompt_response(self, response_text: str) -> Dict:
        """Parse LLM response into prompt data"""

        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback: create basic structure
                result = {
                    "prompt": text[:200],
                    "camera": {"angle": "eye-level", "movement": "static", "speed": "normal"},
                    "lighting": "professional studio lighting"
                }

        return result

    def _select_transition(self, style_key: str, narrative: str) -> str:
        """Select appropriate transition based on style and narrative"""

        options = self.transitions.get(style_key, ["cut"])

        # Special cases based on narrative
        if narrative == "hook":
            return "cut"  # Quick entry
        elif narrative == "cta":
            return "fade"  # Clean exit
        elif narrative == "transformation":
            return "dissolve" if style_key != "energetic" else "cut"

        # Default: first option for style
        return options[0]

    def _validate_visual_consistency(self, prompts: List[Dict]) -> None:
        """Validate visual consistency across all prompts"""

        if len(prompts) < 2:
            return

        # Check all prompts have required fields
        required = ["shot_number", "duration", "runway_prompt"]
        for i, prompt in enumerate(prompts):
            for field in required:
                if field not in prompt:
                    raise ValueError(f"Prompt {i+1} missing required field: {field}")

            # Check prompt length
            runway_prompt = prompt.get("runway_prompt", "")
            if len(runway_prompt) < 20:
                raise ValueError(f"Prompt {i+1} too short: {len(runway_prompt)} chars")
            if len(runway_prompt) > 500:
                raise ValueError(f"Prompt {i+1} too long: {len(runway_prompt)} chars")


# ======================
# STANDALONE USAGE
# ======================

async def main():
    """Example usage of VisualBuilder"""

    builder = VisualBuilder()

    brief = {
        "produto": "Tênis Nike Air Max 2024",
        "duracao": 30,
        "tom": "energético, esportivo"
    }

    concept = {
        "shots": [
            {"number": 1, "duration": 4, "description": "Close-up do tênis girando 360°", "composition": "Product shot, white background", "narrative": "hook"},
            {"number": 2, "duration": 5, "description": "Pessoa correndo em slow-motion", "composition": "Side angle, urban environment", "narrative": "build"},
            {"number": 3, "duration": 5, "description": "Detalhe do amortecimento Air", "composition": "Macro shot, soft lighting", "narrative": "benefit"}
        ],
        "total_duration": 14
    }

    print("Creating visual prompts...")
    prompts = await builder.create_prompts(concept, brief)

    print("\n" + "="*50)
    print("VISUAL PROMPTS GENERATED")
    print("="*50)
    for prompt in prompts:
        print(f"\nShot {prompt['shot_number']}:")
        print(f"  Runway: {prompt['runway_prompt'][:100]}...")
        print(f"  Camera: {prompt['camera']}")
        print(f"  Transition: {prompt['transition']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
