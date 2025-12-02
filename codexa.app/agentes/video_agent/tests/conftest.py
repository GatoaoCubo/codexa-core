"""
video_agent Test Suite - Fixtures and Configuration
====================================================
Pytest configuration and shared fixtures for all tests.
"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock


# =============================================================================
# PATH FIXTURES
# =============================================================================

@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def fixtures_dir():
    """Return the fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def config_dir(project_root):
    """Return the config directory."""
    return project_root / "config"


@pytest.fixture
def templates_dir(project_root):
    """Return the templates directory."""
    return project_root / "templates"


# =============================================================================
# SAMPLE DATA FIXTURES
# =============================================================================

@pytest.fixture
def sample_brief():
    """Return a sample video brief."""
    return {
        "produto": "Nike Air Max 2024",
        "duracao": 30,
        "formato": "9:16",
        "tom": "energetico",
        "objetivo": "Mostrar conforto e estilo do novo Air Max para jovens urbanos",
        "preco": "R$ 599",
        "cta_text": "Compre Agora",
        "video_mode": "overlay",
        "voice": {
            "voice_id": "pMsXgVXv3BLzUgSXRplE",
            "voice_name": "Camila",
            "gender": "feminina"
        }
    }


@pytest.fixture
def sample_brief_clean():
    """Return a sample brief for clean (no text) mode."""
    return {
        "produto": "Nike Air Max 2024",
        "duracao": 45,
        "formato": "16:9",
        "tom": "cinematografico",
        "objetivo": "Video de marca premium para YouTube",
        "video_mode": "clean",
        "voice": {
            "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
            "voice_name": "Rafael",
            "gender": "masculina"
        }
    }


@pytest.fixture
def sample_concept():
    """Return a sample concept.json output from Stage 1."""
    return {
        "shots": [
            {
                "number": 1,
                "duration": 4,
                "description": "Close-up do tenis Nike Air Max girando 360 graus",
                "composition": "Product hero shot, white background",
                "narrative": "hook"
            },
            {
                "number": 2,
                "duration": 5,
                "description": "Pessoa caminhando com o tenis, foco nos pes",
                "composition": "Tracking shot, urban environment",
                "narrative": "build"
            },
            {
                "number": 3,
                "duration": 5,
                "description": "Detalhe do amortecimento Air sendo comprimido",
                "composition": "Extreme close-up, slow motion",
                "narrative": "benefit"
            },
            {
                "number": 4,
                "duration": 5,
                "description": "Pessoa sorrindo, satisfeita com conforto",
                "composition": "Medium shot, lifestyle",
                "narrative": "proof"
            },
            {
                "number": 5,
                "duration": 6,
                "description": "Tenis em destaque com varios colorways",
                "composition": "Product showcase, multiple products",
                "narrative": "build"
            },
            {
                "number": 6,
                "duration": 5,
                "description": "Pack shot final com logo Nike",
                "composition": "Product centered, logo visible",
                "narrative": "cta"
            }
        ],
        "total_duration": 30,
        "narrative_arc": "Hook -> Build -> Benefit -> Proof -> Build -> CTA"
    }


@pytest.fixture
def sample_script():
    """Return a sample script.json output from Stage 2."""
    return {
        "video_mode": "overlay",
        "narration": [
            {
                "start": 0.3,
                "end": 3.5,
                "text": "Conheca o futuro do conforto"
            },
            {
                "start": 5.0,
                "end": 9.0,
                "text": "Nike Air Max com tecnologia revolucionaria"
            },
            {
                "start": 10.0,
                "end": 14.0,
                "text": "Amortecimento Air para o dia todo"
            },
            {
                "start": 20.0,
                "end": 24.0,
                "text": "Estilo que acompanha voce"
            },
            {
                "start": 25.5,
                "end": 29.5,
                "text": "Garanta o seu por apenas 599 reais"
            }
        ],
        "text_overlays": [
            {
                "start": 1,
                "end": 4,
                "text": "NIKE AIR MAX 2024",
                "position": "bottom",
                "style": "bold"
            },
            {
                "start": 10,
                "end": 14,
                "text": "AMORTECIMENTO AIR",
                "position": "center",
                "style": "normal"
            },
            {
                "start": 25,
                "end": 30,
                "text": "R$ 599 | COMPRE AGORA",
                "position": "center",
                "style": "cta"
            }
        ],
        "music": {
            "track": "music/upbeat_electronic.mp3",
            "volume": 0.3
        },
        "voice": {
            "voice_id": "pMsXgVXv3BLzUgSXRplE",
            "voice_name": "Camila",
            "gender": "feminina",
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }


@pytest.fixture
def sample_visual_prompts():
    """Return sample visual_prompts.json output from Stage 3."""
    return {
        "platform": "runway",
        "brand_aligned": True,
        "prompts": [
            {
                "shot_number": 1,
                "duration": 4,
                "prompt": "Slow orbit shot: Cinematic 4K quality, professional studio lighting. Nike Air Max 2024 sneaker rotating smoothly on pristine white surface. Shallow depth of field, dramatic rim light, high-end commercial aesthetic.",
                "negative_prompt": "blurry, low quality, distorted, artifacts, cluttered background",
                "camera": {
                    "movement": "slow orbit",
                    "angle": "eye level",
                    "effect": "draw viewer in"
                },
                "lighting": {
                    "setup": "professional studio lighting",
                    "color_grade": "neutral tones",
                    "mood": "premium"
                },
                "transition": "cut",
                "platform_params": {
                    "duration": 4,
                    "model": "gen3_alpha_turbo"
                }
            },
            {
                "shot_number": 2,
                "duration": 5,
                "prompt": "Tracking shot: Cinematic 4K quality, natural daylight. Person walking confidently on urban sidewalk wearing Nike Air Max. Focus on feet and sneakers. Shallow depth of field, lifestyle aesthetic.",
                "negative_prompt": "blurry, low quality, distorted faces, unnatural movement",
                "camera": {
                    "movement": "tracking",
                    "angle": "low angle",
                    "effect": "dynamic"
                },
                "lighting": {
                    "setup": "natural daylight",
                    "color_grade": "warm tones",
                    "mood": "lifestyle"
                },
                "transition": "cut",
                "platform_params": {
                    "duration": 5,
                    "model": "gen3_alpha_turbo"
                }
            }
        ]
    }


@pytest.fixture
def sample_clips_result():
    """Return sample clips result from Stage 4."""
    return [
        {
            "shot_number": 1,
            "clip_path": "outputs/clips/clip_001.mp4",
            "success": True,
            "cost_usd": 0.20,
            "duration": 4.0,
            "resolution": "1920x1080"
        },
        {
            "shot_number": 2,
            "clip_path": "outputs/clips/clip_002.mp4",
            "success": True,
            "cost_usd": 0.25,
            "duration": 5.0,
            "resolution": "1920x1080"
        },
        {
            "shot_number": 3,
            "clip_path": "outputs/clips/clip_003.mp4",
            "success": True,
            "cost_usd": 0.25,
            "duration": 5.0,
            "resolution": "1920x1080"
        }
    ]


# =============================================================================
# MOCK FIXTURES
# =============================================================================

@pytest.fixture
def mock_anthropic_client():
    """Return a mocked Anthropic client."""
    mock = MagicMock()
    mock.messages.create = AsyncMock(return_value=MagicMock(
        content=[MagicMock(text='{"result": "mocked response"}')]
    ))
    return mock


@pytest.fixture
def mock_runway_client():
    """Return a mocked Runway API client."""
    mock = MagicMock()
    mock.generate = AsyncMock(return_value={
        "id": "gen_123456",
        "status": "completed",
        "output_url": "https://runway.ml/outputs/video.mp4"
    })
    return mock


@pytest.fixture
def mock_elevenlabs_client():
    """Return a mocked ElevenLabs client."""
    mock = MagicMock()
    mock.generate = MagicMock(return_value=b"mock_audio_bytes")
    return mock


@pytest.fixture
def mock_ffmpeg():
    """Return mocked FFmpeg functions."""
    mock = MagicMock()
    mock.input = MagicMock(return_value=mock)
    mock.output = MagicMock(return_value=mock)
    mock.run = MagicMock(return_value=None)
    return mock


# =============================================================================
# CONFIG FIXTURES
# =============================================================================

@pytest.fixture
def video_styles_config(config_dir):
    """Load video_styles.json config."""
    config_path = config_dir / "video_styles.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


@pytest.fixture
def voice_config(config_dir):
    """Load voice_config.json config."""
    config_path = config_dir / "voice_config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


@pytest.fixture
def video_modes_config(config_dir):
    """Load video_modes.json config."""
    config_path = config_dir / "video_modes.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


# =============================================================================
# ENVIRONMENT FIXTURES
# =============================================================================

@pytest.fixture
def mock_env(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-key")
    monkeypatch.setenv("RUNWAY_API_KEY", "rw_test_key")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "el_test_key")
    monkeypatch.setenv("VIDEO_AGENT_MOCK_API", "true")
    monkeypatch.setenv("VIDEO_AGENT_DEBUG", "true")


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    (output_dir / "clips").mkdir()
    return output_dir


# =============================================================================
# VALIDATION FIXTURES
# =============================================================================

@pytest.fixture
def quality_thresholds():
    """Return quality validation thresholds."""
    return {
        "quality_score_minimum": 7.0,
        "brand_compliance_minimum": 8.0,
        "clip_success_rate_minimum": 0.80,
        "duration_tolerance": 0.10,
        "resolution_minimum": 720
    }


@pytest.fixture
def eleven_validation_points():
    """Return the 11-point validation checklist."""
    return [
        "duration",
        "resolution",
        "fps",
        "audio_sync",
        "text_visibility",
        "brand_compliance",
        "no_artifacts",
        "file_size",
        "codec",
        "aspect_ratio",
        "metadata_complete"
    ]
