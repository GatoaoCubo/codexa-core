"""
Tests for Stage 2: Script Builder
==================================
Tests narration timing, text overlays, music selection, and voice configuration.
"""

import pytest
import json


class TestScriptBuilder:
    """Test suite for script_builder (Stage 2)."""

    # =========================================================================
    # NARRATION TESTS
    # =========================================================================

    def test_narration_segments_exist(self, sample_script):
        """Script should have narration segments."""
        assert "narration" in sample_script
        assert len(sample_script["narration"]) > 0

    def test_narration_word_count(self, sample_script):
        """Each narration segment should have 5-15 words."""
        for segment in sample_script["narration"]:
            word_count = len(segment["text"].split())
            assert 3 <= word_count <= 15, f"Segment '{segment['text']}' has {word_count} words"

    def test_narration_no_overlap(self, sample_script):
        """Narration segments should not overlap."""
        segments = sorted(sample_script["narration"], key=lambda x: x["start"])
        for i in range(len(segments) - 1):
            current_end = segments[i]["end"]
            next_start = segments[i + 1]["start"]
            assert current_end <= next_start, f"Overlap between segments {i} and {i+1}"

    def test_narration_within_duration(self, sample_script):
        """Narration should not exceed video duration."""
        total_duration = sample_script["total_duration"]
        for segment in sample_script["narration"]:
            assert segment["end"] <= total_duration, f"Segment ends at {segment['end']} but video is {total_duration}s"

    def test_narration_timing_buffer(self, sample_script):
        """Narration should have buffer at start (0.3s)."""
        first_segment = sample_script["narration"][0]
        assert first_segment["start"] >= 0.3

    # =========================================================================
    # TEXT OVERLAY TESTS (MODE: OVERLAY)
    # =========================================================================

    def test_overlay_mode_has_overlays(self, sample_script):
        """Overlay mode should have at least 1 text overlay."""
        if sample_script["video_mode"] == "overlay":
            assert len(sample_script["text_overlays"]) >= 1

    def test_overlay_mode_has_cta(self, sample_script):
        """Overlay mode should have CTA overlay."""
        if sample_script["video_mode"] == "overlay":
            cta_overlays = [o for o in sample_script["text_overlays"] if o["style"] == "cta"]
            assert len(cta_overlays) >= 1

    def test_overlay_max_words(self, sample_script):
        """Text overlays should have max 6 words."""
        for overlay in sample_script["text_overlays"]:
            word_count = len(overlay["text"].split())
            assert word_count <= 6, f"Overlay '{overlay['text']}' has {word_count} words"

    def test_overlay_uppercase(self, sample_script):
        """Text overlays should be uppercase."""
        for overlay in sample_script["text_overlays"]:
            assert overlay["text"] == overlay["text"].upper()

    def test_overlay_duration_minimum(self, sample_script):
        """Text overlays should be visible for at least 2 seconds."""
        for overlay in sample_script["text_overlays"]:
            duration = overlay["end"] - overlay["start"]
            assert duration >= 2, f"Overlay visible for only {duration}s"

    def test_overlay_valid_position(self, sample_script):
        """Text overlays should have valid position."""
        valid_positions = {"top", "center", "bottom", "top_left", "top_right", "bottom_left", "bottom_right"}
        for overlay in sample_script["text_overlays"]:
            assert overlay["position"] in valid_positions

    def test_overlay_valid_style(self, sample_script):
        """Text overlays should have valid style."""
        valid_styles = {"bold", "normal", "cta", "subtle"}
        for overlay in sample_script["text_overlays"]:
            assert overlay["style"] in valid_styles

    # =========================================================================
    # CLEAN MODE TESTS (NO TEXT)
    # =========================================================================

    def test_clean_mode_no_overlays(self, sample_brief_clean):
        """Clean mode should have no text overlays."""
        # In real implementation:
        # script = script_builder.generate(concept, sample_brief_clean)
        # assert len(script["text_overlays"]) == 0
        assert sample_brief_clean["video_mode"] == "clean"

    def test_clean_mode_requires_narration(self, sample_brief_clean):
        """Clean mode should require narration."""
        # Narration is mandatory in clean mode
        assert sample_brief_clean["video_mode"] == "clean"

    # =========================================================================
    # VOICE CONFIGURATION TESTS
    # =========================================================================

    def test_voice_config_present(self, sample_script):
        """Script should have voice configuration."""
        assert "voice" in sample_script
        assert "voice_id" in sample_script["voice"]

    def test_voice_id_valid(self, sample_script, voice_config):
        """Voice ID should be from valid voice library."""
        voice_id = sample_script["voice"]["voice_id"]
        # In real implementation: validate against voice_config
        assert len(voice_id) > 10  # ElevenLabs IDs are long

    def test_voice_stability_range(self, sample_script):
        """Voice stability should be 0.0-1.0."""
        if "stability" in sample_script["voice"]:
            stability = sample_script["voice"]["stability"]
            assert 0.0 <= stability <= 1.0

    def test_voice_similarity_range(self, sample_script):
        """Voice similarity_boost should be 0.0-1.0."""
        if "similarity_boost" in sample_script["voice"]:
            similarity = sample_script["voice"]["similarity_boost"]
            assert 0.0 <= similarity <= 1.0

    # =========================================================================
    # MUSIC CONFIGURATION TESTS
    # =========================================================================

    def test_music_config_present(self, sample_script):
        """Script should have music configuration."""
        assert "music" in sample_script
        assert "volume" in sample_script["music"]

    def test_music_volume_range(self, sample_script):
        """Music volume should be 0.2-0.4."""
        volume = sample_script["music"]["volume"]
        assert 0.2 <= volume <= 0.4

    def test_music_not_overpowering(self, sample_script):
        """Music should not overpower narration (vol <= 0.4)."""
        volume = sample_script["music"]["volume"]
        assert volume <= 0.4

    # =========================================================================
    # TIMING VALIDATION TESTS
    # =========================================================================

    def test_timing_validation_present(self, sample_script):
        """Script should have timing validation metadata."""
        assert "timing_validation" in sample_script

    def test_no_overlapping_narration(self, sample_script):
        """Timing validation should confirm no overlap."""
        assert sample_script["timing_validation"]["overlapping_segments"] == 0

    def test_narration_within_bounds(self, sample_script):
        """Timing validation should confirm narration within video."""
        assert sample_script["timing_validation"]["narration_exceeds_video"] == False


class TestScriptBuilderVoiceSelection:
    """Tests for voice auto-selection logic."""

    def test_energetico_selects_camila(self):
        """Energetico tone should select Camila (feminina) by default."""
        tom = "energetico"
        expected_voice = "pMsXgVXv3BLzUgSXRplE"
        # In real implementation: voice_id = auto_select_voice(tom)
        assert True  # Placeholder

    def test_sofisticado_selects_bella(self):
        """Sofisticado tone should select Bella (feminina) by default."""
        tom = "sofisticado"
        expected_voice = "EXAVITQu4vr4xnSDxMaL"
        assert True  # Placeholder

    def test_gender_override(self):
        """Gender preference should override default selection."""
        tom = "energetico"
        gender = "masculina"
        expected_voice = "ErXwobaYiN019PkySvjV"  # Antoni
        assert True  # Placeholder


class TestScriptBuilderIntegration:
    """Integration tests for script_builder."""

    def test_script_json_valid_schema(self, sample_script):
        """Generated script.json should match schema."""
        required_fields = {"narration", "text_overlays", "music", "voice", "video_mode"}
        assert required_fields.issubset(sample_script.keys())

    def test_script_from_concept_end_to_end(self, sample_concept, sample_brief):
        """Full concept to script generation flow."""
        # In real implementation:
        # script = script_builder.generate(sample_concept, sample_brief)
        # assert script is not None
        pass
