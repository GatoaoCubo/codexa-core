"""
01_concept_builder.py - Stage 1: Storyboard Generation

Generates 6-8 shot storyboard from video brief with narrative arc:
Hook → Build → Benefit → Proof → Transformation → CTA

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

from anthropic import Anthropic
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class NarrativeFunction(Enum):
    """Narrative function of each shot in the story arc"""
    HOOK = "hook"
    BUILD = "build"
    BENEFIT = "benefit"
    PROOF = "proof"
    TRANSFORMATION = "transformation"
    CTA = "cta"


@dataclass
class Shot:
    """Single shot in storyboard"""
    number: int
    duration: float
    description: str
    composition: str
    narrative: NarrativeFunction
    runway_prompt: Optional[str] = None


@dataclass
class Storyboard:
    """Complete storyboard with all shots"""
    shots: List[Shot]
    total_duration: float
    narrative_arc: str


class ConceptBuilder:
    """
    Stage 1: Generate storyboard from video brief

    Responsibilities:
    - Analyze product brief
    - Define narrative arc (6-phase story structure)
    - Generate 6-8 shots with timing
    - Output structured JSON for next stage
    """

    def __init__(self, client: Optional[Anthropic] = None):
        self.client = client or Anthropic()
        self.model = "claude-sonnet-4-20250514"

    async def generate_storyboard(self, brief: Dict) -> Dict:
        """
        Generate storyboard from video brief

        Args:
            brief: {
                "produto": "Tênis Nike Air Max",
                "duracao": 30,
                "formato": "9:16",
                "tom": "energético",
                "objetivo": "destacar amortecimento"
            }

        Returns:
            {
                "shots": [...],
                "total_duration": 30,
                "narrative_arc": "Hook → Build → CTA"
            }
        """

        # Calculate optimal shot count
        duration = brief.get("duracao", 30)
        shot_count = self._calculate_shot_count(duration)

        # Build prompt
        prompt = self._build_storyboard_prompt(brief, shot_count)

        # Call LLM
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response
        result = self._parse_storyboard_response(response.content[0].text)

        # Validate
        self._validate_storyboard(result, brief)

        return result

    def _calculate_shot_count(self, duration: int) -> int:
        """Calculate optimal number of shots based on duration"""
        if duration <= 15:
            return 3
        elif duration <= 30:
            return 6
        elif duration <= 45:
            return 7
        else:
            return 8

    def _build_storyboard_prompt(self, brief: Dict, shot_count: int) -> str:
        """Build prompt for storyboard generation"""

        return f"""Você é um diretor de vídeo especializado em e-commerce para redes sociais.

BRIEF DO VÍDEO:
- Produto: {brief.get('produto', 'Produto')}
- Duração total: {brief.get('duracao', 30)} segundos
- Formato: {brief.get('formato', '9:16')} (vertical para Reels/TikTok)
- Tom: {brief.get('tom', 'energético')}
- Objetivo: {brief.get('objetivo', 'destacar produto')}

TAREFA: Crie um storyboard profissional com {shot_count} shots.

ESTRUTURA NARRATIVA (siga este arco):
1. HOOK (shot 1): Captura atenção imediatamente - visual impactante ou pergunta provocadora
2. BUILD (shots 2-3): Constrói contexto e interesse - mostra problema ou situação
3. BENEFIT (shots 3-4): Apresenta benefícios do produto - features em ação
4. PROOF (shot 4-5): Demonstra credibilidade - uso real, detalhes, qualidade
5. TRANSFORMATION (shot 5-6): Mostra resultado final - antes/depois, satisfação
6. CTA (último shot): Call-to-action claro - preço, onde comprar, urgência

PARA CADA SHOT, DEFINA:
1. Duração (3-7 segundos, total deve somar ~{brief.get('duracao', 30)}s)
2. Descrição visual detalhada (o que vemos na tela)
3. Composição técnica (ângulo de câmera, movimento, iluminação)
4. Função narrativa (hook/build/benefit/proof/transformation/cta)

REGRAS IMPORTANTES:
- Total de shots deve somar aproximadamente {brief.get('duracao', 30)} segundos
- Primeiro shot SEMPRE é hook (captura atenção nos primeiros 3s)
- Último shot SEMPRE é CTA (call-to-action claro)
- Cada shot deve ter propósito narrativo claro
- Composições devem ser viáveis para geração por IA (Runway/Pika)
- Evite transições complexas demais (corte seco ou fade simples)

FORMATO DE RESPOSTA (JSON válido):
{{
  "shots": [
    {{
      "number": 1,
      "duration": 4,
      "description": "Close-up do tênis girando 360° em fundo branco, mostrando design aerodinâmico e cores vibrantes",
      "composition": "Product shot central, fundo branco infinito, iluminação de estúdio suave, rotação lenta e fluida",
      "narrative": "hook"
    }},
    {{
      "number": 2,
      "duration": 5,
      "description": "...",
      "composition": "...",
      "narrative": "build"
    }}
  ],
  "total_duration": {brief.get('duracao', 30)},
  "narrative_arc": "Hook visual impactante → Contexto de uso → Benefícios em ação → Prova de qualidade → Transformação → CTA com preço"
}}

Retorne APENAS o JSON, sem explicações adicionais."""

    def _parse_storyboard_response(self, response_text: str) -> Dict:
        """Parse LLM response into structured storyboard"""

        # Clean response (remove markdown code blocks if present)
        text = response_text.strip()
        if text.startswith("```"):
            # Remove ```json and ``` markers
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        try:
            result = json.loads(text)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError(f"Failed to parse storyboard JSON: {e}")

        return result

    def _validate_storyboard(self, storyboard: Dict, brief: Dict) -> None:
        """Validate storyboard meets requirements"""

        shots = storyboard.get("shots", [])
        target_duration = brief.get("duracao", 30)

        # Check shot count
        if len(shots) < 3:
            raise ValueError(f"Too few shots: {len(shots)}, minimum is 3")
        if len(shots) > 10:
            raise ValueError(f"Too many shots: {len(shots)}, maximum is 10")

        # Check total duration
        total = sum(shot.get("duration", 0) for shot in shots)
        tolerance = target_duration * 0.15  # 15% tolerance
        if abs(total - target_duration) > tolerance:
            raise ValueError(
                f"Duration mismatch: {total}s vs target {target_duration}s "
                f"(tolerance: {tolerance}s)"
            )

        # Check first shot is hook
        if shots[0].get("narrative") != "hook":
            raise ValueError("First shot must have narrative='hook'")

        # Check last shot is CTA
        if shots[-1].get("narrative") != "cta":
            raise ValueError("Last shot must have narrative='cta'")

        # Check all required fields
        required_fields = ["number", "duration", "description", "composition", "narrative"]
        for i, shot in enumerate(shots):
            for field in required_fields:
                if field not in shot:
                    raise ValueError(f"Shot {i+1} missing required field: {field}")


# ======================
# STANDALONE USAGE
# ======================

async def main():
    """Example usage of ConceptBuilder"""

    builder = ConceptBuilder()

    brief = {
        "produto": "Tênis Nike Air Max 2024",
        "duracao": 30,
        "formato": "9:16",
        "tom": "energético, esportivo",
        "objetivo": "destacar amortecimento Air e design moderno"
    }

    print("Generating storyboard...")
    storyboard = await builder.generate_storyboard(brief)

    print("\n" + "="*50)
    print("STORYBOARD GENERATED")
    print("="*50)
    print(json.dumps(storyboard, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
