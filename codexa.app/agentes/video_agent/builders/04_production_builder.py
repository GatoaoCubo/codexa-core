"""
04_production_builder.py - Stage 4: Video Generation (API Calls)

Calls Runway/Pika APIs to generate video clips asynchronously.

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

import asyncio
import aiohttp
import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import time


@dataclass
class ClipResult:
    """Result of video clip generation"""
    shot_number: int
    clip_path: str
    duration: float
    success: bool
    error: Optional[str] = None
    generation_time: float = 0
    cost_usd: float = 0


class ProductionBuilder:
    """
    Stage 4: Generate video clips via APIs

    Responsibilities:
    - Call Runway/Pika APIs for each shot
    - Handle async parallel generation
    - Implement retry logic and fallbacks
    - Download and validate clips
    """

    def __init__(
        self,
        runway_api_key: Optional[str] = None,
        pika_api_key: Optional[str] = None,
        output_dir: str = "outputs/clips"
    ):
        self.runway_key = runway_api_key or os.getenv("RUNWAY_API_KEY")
        self.pika_key = pika_api_key or os.getenv("PIKA_API_KEY")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # API configuration
        self.runway_endpoint = "https://api.runwayml.com/v1"
        self.pika_endpoint = "https://api.pika.art/v1"

        # Rate limiting
        self.max_concurrent = 5
        self.semaphore = asyncio.Semaphore(self.max_concurrent)

        # Retry configuration
        self.max_retries = 3
        self.retry_delays = [10, 30, 60]  # seconds

        # Cost tracking
        self.runway_cost_per_second = 0.05
        self.pika_cost_per_second = 0.03

    async def generate_clips(self, visual_prompts: List[Dict]) -> List[Dict]:
        """
        Generate all video clips in parallel

        Args:
            visual_prompts: List of visual prompts from Stage 3

        Returns:
            List of clip results with paths
        """

        print(f"   Starting generation of {len(visual_prompts)} clips...")
        print(f"   Max concurrent: {self.max_concurrent}")

        start_time = time.time()

        # Create tasks for all clips
        tasks = [
            self._generate_single_clip(prompt)
            for prompt in visual_prompts
        ]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        clips = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   Error in shot {i+1}: {result}")
                clips.append({
                    "shot_number": i + 1,
                    "clip_path": None,
                    "success": False,
                    "error": str(result)
                })
            else:
                clips.append(result)

        total_time = time.time() - start_time
        successful = sum(1 for c in clips if c.get("success", False))

        print(f"   Completed: {successful}/{len(clips)} clips in {total_time:.1f}s")

        return clips

    async def _generate_single_clip(self, prompt_data: Dict) -> Dict:
        """
        Generate single clip with retry logic

        Args:
            prompt_data: Visual prompt from Stage 3

        Returns:
            Clip result dictionary
        """

        shot_number = prompt_data.get("shot_number", 0)
        duration = prompt_data.get("duration", 5)
        runway_prompt = prompt_data.get("runway_prompt", "")

        async with self.semaphore:  # Rate limiting
            print(f"      Generating shot {shot_number} ({duration}s)...")

            start_time = time.time()

            # Try Runway first
            for attempt in range(self.max_retries):
                try:
                    result = await self._call_runway_api(
                        prompt=runway_prompt,
                        duration=duration,
                        shot_number=shot_number
                    )

                    if result.get("success"):
                        generation_time = time.time() - start_time
                        cost = duration * self.runway_cost_per_second

                        print(f"      Shot {shot_number} completed ({generation_time:.1f}s, ${cost:.2f})")

                        return {
                            "shot_number": shot_number,
                            "clip_path": result["clip_path"],
                            "duration": duration,
                            "success": True,
                            "generation_time": generation_time,
                            "cost_usd": cost,
                            "api": "runway"
                        }

                except Exception as e:
                    print(f"      Shot {shot_number} attempt {attempt+1} failed: {e}")

                    if attempt < self.max_retries - 1:
                        delay = self.retry_delays[attempt]
                        print(f"      Retrying in {delay}s...")
                        await asyncio.sleep(delay)

            # Fallback to Pika
            print(f"      Falling back to Pika for shot {shot_number}...")

            try:
                result = await self._call_pika_api(
                    prompt=runway_prompt,
                    duration=min(duration, 8),  # Pika max is 8s
                    shot_number=shot_number
                )

                if result.get("success"):
                    generation_time = time.time() - start_time
                    cost = duration * self.pika_cost_per_second

                    print(f"      Shot {shot_number} completed via Pika ({generation_time:.1f}s)")

                    return {
                        "shot_number": shot_number,
                        "clip_path": result["clip_path"],
                        "duration": duration,
                        "success": True,
                        "generation_time": generation_time,
                        "cost_usd": cost,
                        "api": "pika"
                    }

            except Exception as e:
                print(f"      Pika fallback also failed: {e}")

            # All attempts failed
            return {
                "shot_number": shot_number,
                "clip_path": None,
                "duration": duration,
                "success": False,
                "error": "All generation attempts failed",
                "generation_time": time.time() - start_time
            }

    async def _call_runway_api(
        self,
        prompt: str,
        duration: int,
        shot_number: int
    ) -> Dict:
        """
        Call Runway Gen-3 API

        Note: This is a simplified implementation.
        Real implementation would use Runway's official SDK.
        """

        if not self.runway_key:
            raise ValueError("RUNWAY_API_KEY not configured")

        # For development/testing: simulate API call
        if os.getenv("VIDEO_AGENT_MOCK_API", "false").lower() == "true":
            return await self._mock_api_call(shot_number, duration, "runway")

        # Real API call (pseudo-code - adapt to actual Runway SDK)
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.runway_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": prompt,
                "duration": duration,
                "model": "gen-3-alpha",
                "resolution": "1080p"
            }

            # Submit generation job
            async with session.post(
                f"{self.runway_endpoint}/generations",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Runway API error: {response.status} - {error_text}")

                job_data = await response.json()
                job_id = job_data.get("id")

            # Poll for completion
            clip_url = await self._poll_runway_job(session, headers, job_id)

            # Download clip
            clip_path = await self._download_clip(session, clip_url, shot_number)

            return {
                "success": True,
                "clip_path": clip_path
            }

    async def _poll_runway_job(
        self,
        session: aiohttp.ClientSession,
        headers: Dict,
        job_id: str,
        timeout: int = 300
    ) -> str:
        """Poll Runway job until completion"""

        start = time.time()

        while time.time() - start < timeout:
            async with session.get(
                f"{self.runway_endpoint}/generations/{job_id}",
                headers=headers
            ) as response:
                if response.status != 200:
                    raise Exception(f"Poll error: {response.status}")

                data = await response.json()
                status = data.get("status")

                if status == "completed":
                    return data.get("output", {}).get("url")
                elif status == "failed":
                    raise Exception(f"Generation failed: {data.get('error')}")

            await asyncio.sleep(5)  # Poll every 5 seconds

        raise Exception("Generation timeout")

    async def _call_pika_api(
        self,
        prompt: str,
        duration: int,
        shot_number: int
    ) -> Dict:
        """
        Call Pika API as fallback

        Note: Simplified implementation.
        """

        if not self.pika_key:
            raise ValueError("PIKA_API_KEY not configured")

        # For development/testing: simulate API call
        if os.getenv("VIDEO_AGENT_MOCK_API", "false").lower() == "true":
            return await self._mock_api_call(shot_number, duration, "pika")

        # Real API call would go here
        # Similar structure to Runway

        raise NotImplementedError("Pika API integration pending")

    async def _mock_api_call(
        self,
        shot_number: int,
        duration: int,
        api: str
    ) -> Dict:
        """Mock API call for testing"""

        # Simulate API latency
        await asyncio.sleep(2)

        # Create mock clip path
        clip_path = str(self.output_dir / f"clip_{shot_number:03d}.mp4")

        # Create placeholder file
        Path(clip_path).parent.mkdir(parents=True, exist_ok=True)
        with open(clip_path, "w") as f:
            f.write(f"Mock clip {shot_number} from {api}")

        return {
            "success": True,
            "clip_path": clip_path
        }

    async def _download_clip(
        self,
        session: aiohttp.ClientSession,
        url: str,
        shot_number: int
    ) -> str:
        """Download clip from URL to local storage"""

        clip_path = self.output_dir / f"clip_{shot_number:03d}.mp4"

        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Download failed: {response.status}")

            with open(clip_path, "wb") as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

        return str(clip_path)

    def validate_clips(self, clips: List[Dict]) -> Dict:
        """
        Validate all generated clips

        Returns:
            Validation summary
        """

        import subprocess

        valid = 0
        invalid = 0
        errors = []

        for clip in clips:
            if not clip.get("success"):
                invalid += 1
                errors.append(f"Shot {clip['shot_number']}: Generation failed")
                continue

            clip_path = clip.get("clip_path")

            if not clip_path or not Path(clip_path).exists():
                invalid += 1
                errors.append(f"Shot {clip['shot_number']}: File not found")
                continue

            # Check video properties with ffprobe
            try:
                result = subprocess.run([
                    "ffprobe",
                    "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=width,height,duration",
                    "-of", "json",
                    clip_path
                ], capture_output=True, text=True)

                info = json.loads(result.stdout)
                stream = info.get("streams", [{}])[0]

                height = int(stream.get("height", 0))

                if height < 720:
                    invalid += 1
                    errors.append(f"Shot {clip['shot_number']}: Resolution too low ({height}p)")
                else:
                    valid += 1

            except Exception as e:
                invalid += 1
                errors.append(f"Shot {clip['shot_number']}: Validation error - {e}")

        return {
            "valid": valid,
            "invalid": invalid,
            "total": len(clips),
            "success_rate": valid / len(clips) if clips else 0,
            "errors": errors
        }


# ======================
# STANDALONE USAGE
# ======================

async def main():
    """Example usage of ProductionBuilder"""

    # Enable mock mode for testing
    os.environ["VIDEO_AGENT_MOCK_API"] = "true"

    builder = ProductionBuilder(output_dir="outputs/clips")

    prompts = [
        {"shot_number": 1, "duration": 4, "runway_prompt": "Nike sneaker rotating 360 degrees on white background, studio lighting, cinematic, 4k"},
        {"shot_number": 2, "duration": 5, "runway_prompt": "Person running in slow motion wearing Nike sneakers, urban street, golden hour"},
        {"shot_number": 3, "duration": 5, "runway_prompt": "Close-up of Nike Air Max cushioning system, macro shot, soft studio lighting"}
    ]

    print("Generating clips...")
    clips = await builder.generate_clips(prompts)

    print("\n" + "="*50)
    print("PRODUCTION RESULTS")
    print("="*50)

    for clip in clips:
        status = "OK" if clip.get("success") else "FAILED"
        print(f"Shot {clip['shot_number']}: {status}")
        if clip.get("success"):
            print(f"  Path: {clip['clip_path']}")
            print(f"  Time: {clip['generation_time']:.1f}s")
            print(f"  Cost: ${clip['cost_usd']:.2f}")

    # Validate
    validation = builder.validate_clips(clips)
    print(f"\nValidation: {validation['valid']}/{validation['total']} valid")


if __name__ == "__main__":
    asyncio.run(main())
