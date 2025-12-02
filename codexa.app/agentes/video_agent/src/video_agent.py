"""
video_agent.py - Main Orchestrator

5-stage pipeline for automated video generation:
Brief → Concept → Script → Visual → Production → Editing → Final Video

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import builders from package (handles numeric-prefixed filenames)
from builders import (
    ConceptBuilder,
    ScriptBuilder,
    VisualBuilder,
    ProductionBuilder,
    EditingBuilder,
)


class VideoAgent:
    """
    Main orchestrator for video generation pipeline

    Pipeline:
    1. CONCEPT: Generate storyboard from brief
    2. SCRIPT: Write narration and timing
    3. VISUAL: Create Runway/Pika prompts
    4. PRODUCTION: Generate video clips (async)
    5. EDITING: Assemble final video

    Usage:
        agent = VideoAgent()
        result = await agent.generate_video(brief)
    """

    def __init__(
        self,
        runway_api_key: Optional[str] = None,
        pika_api_key: Optional[str] = None,
        elevenlabs_api_key: Optional[str] = None,
        output_dir: str = "outputs"
    ):
        """
        Initialize VideoAgent with API keys

        Args:
            runway_api_key: Runway Gen-3 API key
            pika_api_key: Pika API key (fallback)
            elevenlabs_api_key: ElevenLabs TTS API key
            output_dir: Directory for output files
        """

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set environment variables if provided
        if runway_api_key:
            os.environ["RUNWAY_API_KEY"] = runway_api_key
        if pika_api_key:
            os.environ["PIKA_API_KEY"] = pika_api_key
        if elevenlabs_api_key:
            os.environ["ELEVENLABS_API_KEY"] = elevenlabs_api_key

        # Initialize builders
        self.concept_builder = ConceptBuilder()
        self.script_builder = ScriptBuilder()
        self.visual_builder = VisualBuilder()
        self.production_builder = ProductionBuilder(
            output_dir=str(self.output_dir / "clips")
        )
        self.editing_builder = EditingBuilder(
            output_dir=str(self.output_dir)
        )

    async def generate_video(self, brief: Dict) -> Dict:
        """
        Generate complete video from brief

        Args:
            brief: {
                "produto": "Product name and description",
                "duracao": 30,  # seconds
                "formato": "9:16",  # aspect ratio
                "tom": "energetic",  # mood/tone
                "objetivo": "Main goal of video"
            }

        Returns:
            {
                "video_path": "outputs/final_video.mp4",
                "metadata": {...},
                "storyboard": {...},
                "script": {...},
                "quality_score": 8.5
            }
        """

        print("\n" + "="*60)
        print("VIDEO AGENT - STARTING GENERATION")
        print("="*60)
        print(f"Product: {brief.get('produto', 'Unknown')}")
        print(f"Duration: {brief.get('duracao', 30)}s")
        print(f"Format: {brief.get('formato', '9:16')}")
        print("="*60 + "\n")

        start_time = datetime.now()
        total_cost = 0.0

        try:
            # STAGE 1: CONCEPT (Storyboard)
            print("STAGE 1/5: CONCEPT (Storyboard Generation)")
            print("-" * 40)
            concept = await self.concept_builder.generate_storyboard(brief)
            print(f"   Generated {len(concept.get('shots', []))} shots")
            print(f"   Narrative: {concept.get('narrative_arc', 'N/A')[:60]}...")
            print()

            # STAGE 2: SCRIPT (Narration + Timing)
            print("STAGE 2/5: SCRIPT (Narration + Timing)")
            print("-" * 40)
            script = await self.script_builder.write_script(brief, concept)
            print(f"   Narration segments: {len(script.get('narration', []))}")
            print(f"   Text overlays: {len(script.get('text_overlays', []))}")
            print(f"   Music: {script.get('music', {}).get('track', 'N/A')}")
            print()

            # STAGE 3: VISUAL (Prompt Engineering)
            print("STAGE 3/5: VISUAL (Prompt Engineering)")
            print("-" * 40)
            visual_prompts = await self.visual_builder.create_prompts(concept, brief)
            print(f"   Generated {len(visual_prompts)} Runway prompts")
            print()

            # STAGE 4: PRODUCTION (API Calls)
            print("STAGE 4/5: PRODUCTION (Video Generation)")
            print("-" * 40)
            clips = await self.production_builder.generate_clips(visual_prompts)
            successful_clips = sum(1 for c in clips if c.get("success"))
            total_cost += sum(c.get("cost_usd", 0) for c in clips)
            print(f"   Successful clips: {successful_clips}/{len(clips)}")
            print(f"   Cost so far: ${total_cost:.2f}")
            print()

            # STAGE 5: EDITING (Timeline Assembly)
            print("STAGE 5/5: EDITING (Final Assembly)")
            print("-" * 40)
            output_name = self._generate_output_name(brief)
            editing_result = await self.editing_builder.assemble_video(
                clips=clips,
                script=script,
                format=brief.get("formato", "9:16"),
                output_name=output_name
            )
            print()

            # Calculate total time
            total_time = (datetime.now() - start_time).total_seconds()

            # Build result
            result = {
                "video_path": editing_result.get("final_path"),
                "metadata": {
                    "brief": brief,
                    "duration": editing_result.get("duration", 0),
                    "file_size_mb": editing_result.get("file_size_mb", 0),
                    "shots": len(clips),
                    "successful_shots": successful_clips,
                    "generation_time_seconds": total_time,
                    "cost_usd": total_cost,
                    "timestamp": datetime.now().isoformat()
                },
                "storyboard": concept,
                "script": script,
                "visual_prompts": visual_prompts,
                "clips": clips,
                "quality_score": self._calculate_quality_score(
                    editing_result, clips, script
                )
            }

            # Save metadata
            self._save_metadata(result, output_name)

            # Print summary
            print("="*60)
            print("VIDEO GENERATION COMPLETE!")
            print("="*60)
            print(f"Output: {result['video_path']}")
            print(f"Duration: {result['metadata']['duration']:.1f}s")
            print(f"Size: {result['metadata']['file_size_mb']:.1f}MB")
            print(f"Time: {total_time:.1f}s")
            print(f"Cost: ${total_cost:.2f}")
            print(f"Quality Score: {result['quality_score']:.1f}/10.0")
            print("="*60 + "\n")

            return result

        except Exception as e:
            print(f"\nERROR: Video generation failed: {e}")
            raise

    def _generate_output_name(self, brief: Dict) -> str:
        """Generate output filename from brief"""

        produto = brief.get("produto", "video")
        duracao = brief.get("duracao", 30)

        # Clean product name
        clean_name = "".join(
            c if c.isalnum() or c in " -_" else ""
            for c in produto.lower()
        ).replace(" ", "_")[:30]

        return f"{clean_name}_{duracao}s"

    def _calculate_quality_score(
        self,
        editing_result: Dict,
        clips: list,
        script: Dict
    ) -> float:
        """Calculate overall quality score (0-10)"""

        score = 10.0

        # Deduct for editing failure
        if not editing_result.get("success"):
            score -= 3.0

        # Deduct for failed clips
        failed_clips = sum(1 for c in clips if not c.get("success"))
        score -= failed_clips * 0.5

        # Deduct for missing narration
        if not script.get("narration"):
            score -= 1.0

        # Deduct for missing text overlays
        if not script.get("text_overlays"):
            score -= 0.5

        # Ensure score is in valid range
        return max(0.0, min(10.0, score))

    def _save_metadata(self, result: Dict, output_name: str):
        """Save metadata files (Trinity output)"""

        # .llm.json (structured for LLM consumption)
        llm_path = self.output_dir / f"{output_name}.llm.json"
        with open(llm_path, "w", encoding="utf-8") as f:
            json.dump({
                "video_path": result["video_path"],
                "storyboard": result["storyboard"],
                "script": result["script"],
                "quality_score": result["quality_score"]
            }, f, indent=2, ensure_ascii=False)

        # .meta.json (metadata for tracking)
        meta_path = self.output_dir / f"{output_name}.meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(result["metadata"], f, indent=2, ensure_ascii=False)

        print(f"   Metadata saved: {llm_path.name}, {meta_path.name}")


# ======================
# CLI INTERFACE
# ======================

async def main():
    """CLI interface for VideoAgent"""

    import argparse

    parser = argparse.ArgumentParser(description="Generate video from product brief")
    parser.add_argument("--produto", required=True, help="Product name/description")
    parser.add_argument("--duracao", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--formato", default="9:16", choices=["9:16", "16:9", "1:1"])
    parser.add_argument("--tom", default="energético", help="Video tone/mood")
    parser.add_argument("--objetivo", default="destacar produto", help="Video goal")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    parser.add_argument("--mock", action="store_true", help="Use mock APIs for testing")

    args = parser.parse_args()

    if args.mock:
        os.environ["VIDEO_AGENT_MOCK_API"] = "true"

    agent = VideoAgent(output_dir=args.output_dir)

    brief = {
        "produto": args.produto,
        "duracao": args.duracao,
        "formato": args.formato,
        "tom": args.tom,
        "objetivo": args.objetivo
    }

    result = await agent.generate_video(brief)

    print(f"\nVideo saved to: {result['video_path']}")


if __name__ == "__main__":
    asyncio.run(main())
