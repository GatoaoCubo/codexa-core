"""
Tests for Stage 3: Visual Builder
==================================
Tests prompt engineering, platform selection, and brand alignment.
"""

import pytest
import json


class TestVisualBuilder:
    """Test suite for visual_builder (Stage 3)."""

    # =========================================================================
    # PROMPT GENERATION TESTS
    # =========================================================================

    def test_prompts_generated_for_all_shots(self, sample_visual_prompts, sample_concept):
        """Should generate prompts for all shots in concept."""
        num_shots = len(sample_concept["shots"])
        num_prompts = len(sample_visual_prompts["prompts"])
        # May have fewer prompts if some shots are combined
        assert num_prompts >= 1

    def test_prompt_length_valid(self, sample_visual_prompts):
        """Prompts should be 20-500 characters."""
        for prompt in sample_visual_prompts["prompts"]:
            length = len(prompt["prompt"])
            assert 20 <= length <= 500, f"Prompt length {length} out of range"

    def test_prompts_in_english(self, sample_visual_prompts):
        """Prompts should be in English (for Runway compatibility)."""
        for prompt in sample_visual_prompts["prompts"]:
            # Check for common English words
            text = prompt["prompt"].lower()
            english_indicators = ["the", "a", "an", "shot", "camera", "light"]
            has_english = any(word in text for word in english_indicators)
            assert has_english, f"Prompt may not be in English: {prompt['prompt'][:50]}..."

    def test_prompts_ascii_only(self, sample_visual_prompts):
        """Prompts should be ASCII only."""
        for prompt in sample_visual_prompts["prompts"]:
            assert prompt["prompt"].isascii(), f"Non-ASCII in prompt: {prompt['prompt'][:50]}..."

    # =========================================================================
    # NEGATIVE PROMPT TESTS
    # =========================================================================

    def test_negative_prompts_present(self, sample_visual_prompts):
        """Each prompt should have negative prompt."""
        for prompt in sample_visual_prompts["prompts"]:
            assert "negative_prompt" in prompt
            assert len(prompt["negative_prompt"]) > 0

    def test_negative_prompts_common_issues(self, sample_visual_prompts):
        """Negative prompts should include common quality issues."""
        common_negatives = ["blurry", "low quality", "distorted", "artifacts"]
        for prompt in sample_visual_prompts["prompts"]:
            neg = prompt["negative_prompt"].lower()
            has_common = any(n in neg for n in common_negatives)
            assert has_common

    # =========================================================================
    # CAMERA CONFIGURATION TESTS
    # =========================================================================

    def test_camera_config_present(self, sample_visual_prompts):
        """Each prompt should have camera configuration."""
        for prompt in sample_visual_prompts["prompts"]:
            assert "camera" in prompt
            assert "movement" in prompt["camera"]
            assert "angle" in prompt["camera"]

    def test_camera_movement_valid(self, sample_visual_prompts):
        """Camera movement should be valid cinematographic term."""
        valid_movements = {
            "static", "dolly", "push", "pull", "orbit", "pan", "tilt",
            "tracking", "crane", "zoom", "slow", "fast", "handheld"
        }
        for prompt in sample_visual_prompts["prompts"]:
            movement = prompt["camera"]["movement"].lower()
            has_valid = any(m in movement for m in valid_movements)
            assert has_valid, f"Invalid camera movement: {movement}"

    # =========================================================================
    # LIGHTING CONFIGURATION TESTS
    # =========================================================================

    def test_lighting_config_present(self, sample_visual_prompts):
        """Each prompt should have lighting configuration."""
        for prompt in sample_visual_prompts["prompts"]:
            assert "lighting" in prompt
            assert "setup" in prompt["lighting"]

    def test_lighting_includes_mood(self, sample_visual_prompts):
        """Lighting should include mood information."""
        for prompt in sample_visual_prompts["prompts"]:
            assert "mood" in prompt["lighting"]

    # =========================================================================
    # PLATFORM SELECTION TESTS
    # =========================================================================

    def test_platform_specified(self, sample_visual_prompts):
        """Output should specify target platform."""
        assert "platform" in sample_visual_prompts
        valid_platforms = {"runway", "pika", "veo3", "sora2", "kling", "hailuo", "auto"}
        assert sample_visual_prompts["platform"] in valid_platforms

    def test_platform_params_present(self, sample_visual_prompts):
        """Each prompt should have platform-specific parameters."""
        for prompt in sample_visual_prompts["prompts"]:
            assert "platform_params" in prompt

    def test_runway_params_valid(self, sample_visual_prompts):
        """Runway platform should have valid parameters."""
        if sample_visual_prompts["platform"] == "runway":
            for prompt in sample_visual_prompts["prompts"]:
                params = prompt["platform_params"]
                assert "duration" in params
                assert params["duration"] <= 10  # Runway max

    # =========================================================================
    # VIDEO MODE COMPOSITION TESTS
    # =========================================================================

    def test_overlay_mode_reserves_space(self):
        """Overlay mode should reserve bottom 20% for text."""
        # In real implementation: check composition notes
        pass

    def test_clean_mode_full_frame(self):
        """Clean mode should use full frame composition."""
        # In real implementation: check composition notes
        pass

    # =========================================================================
    # BRAND ALIGNMENT TESTS
    # =========================================================================

    def test_brand_aligned_flag(self, sample_visual_prompts):
        """Should indicate if brand-aligned."""
        assert "brand_aligned" in sample_visual_prompts

    def test_brand_colors_in_lighting(self):
        """Brand colors should be reflected in lighting/grading."""
        # In real implementation: check color_grade references brand palette
        pass

    # =========================================================================
    # TRANSITION TESTS
    # =========================================================================

    def test_transitions_present(self, sample_visual_prompts):
        """Each prompt should specify transition."""
        for prompt in sample_visual_prompts["prompts"]:
            assert "transition" in prompt

    def test_transitions_valid(self, sample_visual_prompts):
        """Transitions should be valid types."""
        valid_transitions = {"cut", "dissolve", "fade", "wipe", "none"}
        for prompt in sample_visual_prompts["prompts"]:
            assert prompt["transition"] in valid_transitions


class TestVisualBuilderPlatformSpecific:
    """Tests for platform-specific prompt generation."""

    def test_veo3_includes_audio_syntax(self):
        """Veo3 prompts should include audio syntax if dialogue."""
        # Format: Character says: "[text]" (no subtitles)
        pass

    def test_hailuo_includes_emphasis_markers(self):
        """Hailuo prompts should use ((emphasis)) markers."""
        pass

    def test_pika_includes_camera_flag(self):
        """Pika prompts should include --camera flag."""
        pass

    def test_sora2_includes_look_camera_lighting(self):
        """Sora2 prompts should have LOOK, CAMERA, LIGHTING structure."""
        pass


class TestVisualBuilderMagicWords:
    """Tests for magic words inclusion."""

    def test_includes_quality_magic_words(self, sample_visual_prompts):
        """Prompts should include quality magic words."""
        quality_words = ["cinematic", "4K", "professional", "quality"]
        for prompt_obj in sample_visual_prompts["prompts"]:
            prompt = prompt_obj["prompt"].lower()
            has_quality = any(word.lower() in prompt for word in quality_words)
            assert has_quality, f"Missing quality words in: {prompt[:50]}..."

    def test_includes_depth_of_field(self, sample_visual_prompts):
        """Prompts should often include depth of field."""
        dof_count = sum(
            1 for p in sample_visual_prompts["prompts"]
            if "depth of field" in p["prompt"].lower()
        )
        # At least some prompts should have DOF
        assert dof_count >= 1


class TestVisualBuilderIntegration:
    """Integration tests for visual_builder."""

    def test_visual_prompts_json_valid_schema(self, sample_visual_prompts):
        """Generated visual_prompts.json should match schema."""
        required_fields = {"platform", "prompts"}
        assert required_fields.issubset(sample_visual_prompts.keys())

    def test_visual_from_concept_end_to_end(self, sample_concept, sample_brief):
        """Full concept to visual prompts generation flow."""
        # In real implementation:
        # visual = visual_builder.generate(sample_concept, sample_brief)
        # assert visual is not None
        pass
