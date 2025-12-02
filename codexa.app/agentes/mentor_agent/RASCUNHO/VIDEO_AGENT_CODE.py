"""
VIDEO_AGENT: Automated Video Production for E-commerce
Author: Mentor Agent (assisted)
Date: 2025-11-24
"""

from anthropic import Anthropic
import json
import asyncio
from pathlib import Path
from typing import Dict, List
import subprocess

class VideoAgent:
    """
    5-stage pipeline for automated video generation:
    Brief → Concept → Script → Production → Editing
    """

    def __init__(self, runway_api_key: str = None, pika_api_key: str = None):
        self.client = Anthropic()
        self.runway_key = runway_api_key
        self.pika_key = pika_api_key

        # Sub-agents
        self.concept_agent = ConceptAgent(self.client)
        self.script_agent = ScriptAgent(self.client)
        self.visual_agent = VisualAgent(self.client)
        self.production_agent = ProductionAgent(self.runway_key, self.pika_key)
        self.editing_agent = EditingAgent()

    async def generate_video(self, brief: Dict) -> Dict:
        """
        Main pipeline: Brief → Final Video

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
                "video_path": "outputs/final_video.mp4",
                "metadata": {...},
                "storyboard": {...},
                "script": {...}
            }
        """

        print("🎬 Starting video generation pipeline...")

        # STAGE 1: Concept (Storyboard)
        print("\n📋 Stage 1: Generating concept...")
        concept = await self.concept_agent.generate_storyboard(brief)
        print(f"   ✓ Generated {len(concept['shots'])} shots")

        # STAGE 2: Script (Narration + Timing)
        print("\n✍️ Stage 2: Writing script...")
        script = await self.script_agent.write_script(brief, concept)
        print(f"   ✓ Script: {len(script['narration'])} narration segments")

        # STAGE 3: Visual (Prompt Engineering)
        print("\n🎨 Stage 3: Creating visual prompts...")
        visual_prompts = await self.visual_agent.create_prompts(concept, brief)
        print(f"   ✓ Generated {len(visual_prompts)} video prompts")

        # STAGE 4: Production (API Calls - ASYNC)
        print("\n🎥 Stage 4: Generating video clips (this takes 2-5min)...")
        clips = await self.production_agent.generate_clips(visual_prompts)
        print(f"   ✓ Generated {len(clips)} clips")

        # STAGE 5: Editing (Timeline Assembly)
        print("\n🎞️ Stage 5: Assembling final video...")
        final_video = await self.editing_agent.assemble_video(
            clips=clips,
            script=script,
            format=brief["formato"]
        )
        print(f"   ✓ Final video: {final_video}")

        return {
            "video_path": final_video,
            "metadata": {
                "brief": brief,
                "duration": self._get_video_duration(final_video),
                "shots": len(clips)
            },
            "storyboard": concept,
            "script": script
        }

    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration using ffprobe"""
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())


class ConceptAgent:
    """Stage 1: Generate storyboard from brief"""

    def __init__(self, client: Anthropic):
        self.client = client

    async def generate_storyboard(self, brief: Dict) -> Dict:
        """
        Generate 6-8 shot storyboard

        Returns:
            {
                "shots": [
                    {
                        "number": 1,
                        "duration": 5,
                        "description": "...",
                        "composition": "...",
                        "narrative": "hook/build/payoff/cta"
                    },
                    ...
                ]
            }
        """

        prompt = f"""Você é um diretor de video especializado em e-commerce.

BRIEF:
- Produto: {brief['produto']}
- Duração: {brief['duracao']}s
- Formato: {brief['formato']}
- Tom: {brief['tom']}
- Objetivo: {brief['objetivo']}

TAREFA: Crie um storyboard de {brief['duracao'] // 5} shots para este video.

Para cada shot, defina:
1. Duração (3-7s)
2. Descrição visual detalhada
3. Composição (ângulo, lighting, movimento)
4. Função narrativa (hook/build/payoff/cta)

Retorne JSON:
{{
  "shots": [
    {{
      "number": 1,
      "duration": 5,
      "description": "Close-up do produto girando 360°",
      "composition": "Product shot, white background, studio lighting",
      "narrative": "hook"
    }},
    ...
  ]
}}

REGRAS:
- Total de shots deve somar ~{brief['duracao']}s
- Primeiro shot SEMPRE é hook (captura atenção)
- Último shot SEMPRE é CTA (call-to-action)
- Shots intermediários contam história (problema → solução)
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)


class ScriptAgent:
    """Stage 2: Write narration script with timing"""

    def __init__(self, client: Anthropic):
        self.client = client

    async def write_script(self, brief: Dict, concept: Dict) -> Dict:
        """
        Generate narration + text overlays with precise timing

        Returns:
            {
                "narration": [
                    {"start": 0, "end": 3, "text": "..."}
                ],
                "text_overlays": [
                    {"start": 1, "end": 3, "text": "NIKE AIR MAX", "position": "center"}
                ],
                "music": {
                    "track": "upbeat.mp3",
                    "volume": 0.3
                }
            }
        """

        shots_summary = "\n".join([
            f"Shot {s['number']} ({s['duration']}s): {s['description']}"
            for s in concept['shots']
        ])

        prompt = f"""Você é um copywriter de video para e-commerce.

BRIEF: {brief['produto']} - {brief['objetivo']}
TOM: {brief['tom']}

STORYBOARD:
{shots_summary}

TAREFA: Escreva script de narração com timing preciso.

Retorne JSON:
{{
  "narration": [
    {{"start": 0, "end": 3, "text": "Conheça o futuro do conforto"}},
    {{"start": 5, "end": 9, "text": "Nike Air Max com tecnologia Air"}}
  ],
  "text_overlays": [
    {{"start": 1, "end": 3, "text": "NIKE AIR MAX 2024", "position": "center"}}
  ],
  "music": {{
    "track": "upbeat_electronic.mp3",
    "volume": 0.3
  }}
}}

REGRAS:
- Narração concisa (5-10 palavras por segmento)
- Text overlays apenas para informações-chave
- Não sobrepor narração e text overlay
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)


class VisualAgent:
    """Stage 3: Create video generation prompts"""

    def __init__(self, client: Anthropic):
        self.client = client

    async def create_prompts(self, concept: Dict, brief: Dict) -> List[Dict]:
        """
        Transform storyboard shots into Runway/Pika prompts

        Returns:
            [
                {
                    "shot_number": 1,
                    "duration": 5,
                    "runway_prompt": "Nike sneaker rotating 360...",
                    "style": "cinematic, 4k, professional"
                },
                ...
            ]
        """

        prompts = []

        for shot in concept['shots']:
            prompt_text = f"""Você é um prompt engineer para Runway Gen-3.

SHOT: {shot['description']}
COMPOSIÇÃO: {shot['composition']}
PRODUTO: {brief['produto']}

TAREFA: Crie prompt detalhado para Runway que gere este shot em video.

Formato ideal:
- Descrição visual específica
- Movimento/ação clara
- Estilo e qualidade (cinematic, 4k, etc)
- Lighting e mood

Retorne apenas o prompt (sem JSON, só texto):
"""

            response = self.client.messages.create(
                model="claude-haiku-20250305",  # Haiku = mais rápido para prompts
                max_tokens=300,
                messages=[{"role": "user", "content": prompt_text}]
            )

            prompts.append({
                "shot_number": shot['number'],
                "duration": shot['duration'],
                "runway_prompt": response.content[0].text.strip(),
                "style": "cinematic, 4k, professional lighting"
            })

        return prompts


class ProductionAgent:
    """Stage 4: Call video generation APIs (async)"""

    def __init__(self, runway_key: str, pika_key: str):
        self.runway_key = runway_key
        self.pika_key = pika_key

    async def generate_clips(self, visual_prompts: List[Dict]) -> List[str]:
        """
        Generate video clips using Runway/Pika APIs

        Returns:
            ["clip_001.mp4", "clip_002.mp4", ...]
        """

        print("   ⏳ Calling Runway API (this is async, may take 2-5min)...")

        # Create async tasks for all clips
        tasks = [
            self._generate_single_clip(prompt)
            for prompt in visual_prompts
        ]

        # Wait for all clips to finish
        clips = await asyncio.gather(*tasks)

        return clips

    async def _generate_single_clip(self, prompt_data: Dict) -> str:
        """
        Generate single clip via Runway API

        Note: This is pseudo-code. Real implementation would use
        Runway's official Python SDK or HTTP API.
        """

        # Simulate API call (replace with real Runway SDK)
        print(f"      Generating shot {prompt_data['shot_number']}...")

        # Pseudo-code for Runway API
        # from runway import RunwayClient
        # client = RunwayClient(api_key=self.runway_key)
        # clip = await client.generate_video(
        #     prompt=prompt_data['runway_prompt'],
        #     duration=prompt_data['duration']
        # )

        # For now, simulate delay
        await asyncio.sleep(2)  # Simula API call

        # Return clip path
        clip_path = f"outputs/clip_{prompt_data['shot_number']:03d}.mp4"

        return clip_path


class EditingAgent:
    """Stage 5: Assemble clips into final video"""

    async def assemble_video(self, clips: List[str], script: Dict, format: str) -> str:
        """
        Use FFmpeg to assemble timeline

        Steps:
        1. Concatenate clips
        2. Add narration audio
        3. Add music (background)
        4. Add text overlays
        5. Export final video
        """

        print("   🎬 Assembling video with FFmpeg...")

        # 1. Create concat file for FFmpeg
        concat_file = "outputs/concat_list.txt"
        with open(concat_file, "w") as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")

        # 2. Concatenate clips
        intermediate = "outputs/concatenated.mp4"
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            intermediate
        ])

        # 3. Add music (simplified - real impl would overlay narration too)
        final_output = "outputs/final_video.mp4"
        subprocess.run([
            "ffmpeg",
            "-i", intermediate,
            "-i", script['music']['track'],
            "-filter_complex", "[1:a]volume=0.3[a1];[0:a][a1]amix=inputs=2[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            final_output
        ])

        print(f"   ✅ Final video: {final_output}")

        return final_output


# ======================
# USAGE EXAMPLE
# ======================

async def main():
    """Example usage of VideoAgent"""

    # Initialize agent
    agent = VideoAgent(
        runway_api_key="your-runway-key",
        pika_api_key="your-pika-key"
    )

    # Define video brief
    brief = {
        "produto": "Tênis Nike Air Max 2024",
        "duracao": 30,
        "formato": "9:16",  # Instagram Reels
        "tom": "energético, esportivo",
        "objetivo": "destacar amortecimento Air e design moderno"
    }

    # Generate video
    result = await agent.generate_video(brief)

    print("\n" + "="*50)
    print("🎉 VIDEO GENERATION COMPLETE!")
    print("="*50)
    print(f"Video path: {result['video_path']}")
    print(f"Duration: {result['metadata']['duration']}s")
    print(f"Shots: {result['metadata']['shots']}")


if __name__ == "__main__":
    asyncio.run(main())
