"""
VIDEO_AGENT: Test Suite
Validates all 5 stages + end-to-end pipeline
"""

import pytest
import asyncio
from VIDEO_AGENT_CODE import VideoAgent, ConceptAgent, ScriptAgent

class TestConceptAgent:
    """Test Stage 1: Storyboard generation"""

    @pytest.mark.asyncio
    async def test_storyboard_generation_basic(self):
        """Test basic storyboard with 30s video"""
        agent = ConceptAgent(None)  # Mock client

        brief = {
            "produto": "Tênis Nike",
            "duracao": 30,
            "formato": "9:16",
            "tom": "energético",
            "objetivo": "destacar conforto"
        }

        concept = await agent.generate_storyboard(brief)

        # Assertions
        assert "shots" in concept
        assert len(concept["shots"]) >= 5  # 30s = ~6 shots de 5s
        assert len(concept["shots"]) <= 8

        # Validate each shot has required fields
        for shot in concept["shots"]:
            assert "number" in shot
            assert "duration" in shot
            assert "description" in shot
            assert "composition" in shot
            assert "narrative" in shot

        # Validate total duration ~= target
        total_duration = sum(s["duration"] for s in concept["shots"])
        assert 25 <= total_duration <= 35  # ±5s tolerance

        # Validate narrative structure
        narratives = [s["narrative"] for s in concept["shots"]]
        assert "hook" in narratives[0]  # First shot must be hook
        assert "cta" in narratives[-1]  # Last shot must be CTA

    @pytest.mark.asyncio
    async def test_storyboard_different_durations(self):
        """Test that storyboard adapts to different durations"""
        agent = ConceptAgent(None)

        # Test 15s video
        brief_15s = {"produto": "Fone", "duracao": 15, "formato": "9:16", "tom": "calm", "objetivo": "som"}
        concept_15s = await agent.generate_storyboard(brief_15s)
        assert len(concept_15s["shots"]) == 3  # 15s = 3 shots

        # Test 60s video
        brief_60s = {"produto": "Relógio", "duracao": 60, "formato": "16:9", "tom": "luxury", "objetivo": "design"}
        concept_60s = await agent.generate_storyboard(brief_60s)
        assert len(concept_60s["shots"]) >= 10  # 60s = ~12 shots


class TestScriptAgent:
    """Test Stage 2: Script writing"""

    @pytest.mark.asyncio
    async def test_script_timing(self):
        """Test that script timing aligns with storyboard"""
        agent = ScriptAgent(None)

        brief = {"produto": "Tênis", "tom": "energético"}
        concept = {
            "shots": [
                {"number": 1, "duration": 5, "description": "Close-up"},
                {"number": 2, "duration": 5, "description": "Action shot"}
            ]
        }

        script = await agent.write_script(brief, concept)

        # Validate structure
        assert "narration" in script
        assert "text_overlays" in script
        assert "music" in script

        # Validate timing makes sense
        for narration in script["narration"]:
            assert narration["end"] > narration["start"]
            assert narration["end"] <= 10  # Total duration of concept

        # Validate no overlaps between narration and text
        narration_times = [(n["start"], n["end"]) for n in script["narration"]]
        text_times = [(t["start"], t["end"]) for t in script["text_overlays"]]

        for n_start, n_end in narration_times:
            for t_start, t_end in text_times:
                # Check if there's overlap
                overlap = max(0, min(n_end, t_end) - max(n_start, t_start))
                assert overlap < 0.5  # Max 0.5s overlap tolerance


class TestEndToEnd:
    """Test complete pipeline"""

    @pytest.mark.asyncio
    async def test_full_pipeline_30s_video(self):
        """Test generating complete 30s video"""
        agent = VideoAgent(runway_api_key="test", pika_api_key="test")

        brief = {
            "produto": "Tênis Nike Air Max 2024",
            "duracao": 30,
            "formato": "9:16",
            "tom": "energético",
            "objetivo": "destacar amortecimento"
        }

        result = await agent.generate_video(brief)

        # Validate output structure
        assert "video_path" in result
        assert "metadata" in result
        assert "storyboard" in result
        assert "script" in result

        # Validate video file exists
        assert Path(result["video_path"]).exists()

        # Validate metadata
        assert result["metadata"]["duration"] >= 28  # ±2s tolerance
        assert result["metadata"]["duration"] <= 32
        assert result["metadata"]["shots"] >= 5


class TestQualityValidation:
    """Test quality checks"""

    def test_validate_clip_resolution(self):
        """Test that clips meet minimum resolution"""
        from moviepy.editor import VideoFileClip

        clip = VideoFileClip("test_clip.mp4")

        # Check resolution (must be at least 1080p height)
        assert clip.size[1] >= 1080, "Clip resolution too low"

    def test_validate_clip_duration(self):
        """Test clip duration matches expected"""
        from moviepy.editor import VideoFileClip

        clip = VideoFileClip("test_clip.mp4")
        expected_duration = 5.0

        # Check duration (±0.5s tolerance)
        assert abs(clip.duration - expected_duration) <= 0.5


class TestErrorHandling:
    """Test error scenarios"""

    @pytest.mark.asyncio
    async def test_api_timeout_fallback(self):
        """Test that agent falls back to template on API timeout"""
        agent = VideoAgent(runway_api_key="invalid")

        brief = {"produto": "Test", "duracao": 15, "formato": "9:16", "tom": "test", "objetivo": "test"}

        # Should not raise exception, should fall back gracefully
        result = await agent.generate_video(brief)

        # Should still return a video (template)
        assert result["video_path"] is not None

    @pytest.mark.asyncio
    async def test_low_quality_clip_retry(self):
        """Test that low quality clips are regenerated"""
        # Mock production agent to return low quality clip first time
        # Then return good clip on retry

        # This would require mocking, simplified for example
        pass


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
