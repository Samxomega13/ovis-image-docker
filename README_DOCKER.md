# Ovis-Image Docker Deployment Guide

## Quick Start

```bash
# 1. One-command startup (auto-selects GPU with lowest memory)
./start.sh

# 2. Access the application
# UI: http://localhost:7860
# API Docs: http://localhost:7860/docs
```

## Features

### 🎨 Dual Mode Support
- **UI Mode**: Modern web interface with dark mode support
- **API Mode**: RESTful API with Swagger documentation

### 🚀 Smart GPU Management
- Auto-selects GPU with lowest memory usage on startup
- Auto-unloads models after idle timeout (configurable)
- Auto-reloads on new requests

### 🌍 Multi-language UI
- English
- 简体中文 (Simplified Chinese)
- 繁體中文 (Traditional Chinese)
- 日本語 (Japanese)

## Configuration

Edit `.env` file:

```bash
MODEL_PATH=AIDC-AI/Ovis-Image-7B/ovis_image.safetensors
VAE_PATH=AIDC-AI/Ovis-Image-7B/ae.safetensors
OVIS_PATH=AIDC-AI/Ovis-Image-7B/Ovis2.5-2B
PORT=7860
IDLE_TIMEOUT=300  # seconds
```

## API Usage

### Generate Image

```bash
curl -X POST "http://localhost:7860/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A creative 3D artistic render",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }'
```

### Response

```json
{
  "status": "success",
  "image": "/outputs/output_1234567890.png"
}
```

## Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| prompt | string | - | - | Text description of desired image |
| image_size | int | 1024 | 512-2048 | Output image dimensions (square) |
| denoising_steps | int | 50 | 20-100 | Quality vs speed tradeoff |
| cfg_scale | float | 5.0 | 1.0-15.0 | Prompt adherence strength |
| seed | int | 42 | - | Reproducibility seed |

## Management Commands

```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build

# Check GPU usage
nvidia-smi
```

## Troubleshooting

### Models not downloading
Ensure HuggingFace cache is accessible:
```bash
ls ~/.cache/huggingface
```

### Out of memory
Reduce `image_size` or increase `IDLE_TIMEOUT` to free GPU faster

### Port already in use
Change `PORT` in `.env` file

## Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI + Gradio App            │
├─────────────────────────────────────────┤
│  UI (/)          │  API (/api/*)        │
│  - Gradio Web    │  - REST Endpoints    │
│  - Multi-lang    │  - Swagger Docs      │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│         Model Manager                    │
│  - Auto GPU selection                    │
│  - Lazy loading                          │
│  - Idle timeout unloading                │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│    Ovis-Image Model (7B params)         │
│  - Text encoder (Ovis 2.5-2B)           │
│  - Diffusion model (7B)                  │
│  - VAE decoder                           │
└─────────────────────────────────────────┘
```
