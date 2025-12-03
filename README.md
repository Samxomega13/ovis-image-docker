# Ovis-Image Docker Deployment

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.1-green.svg)](https://developer.nvidia.com/cuda-toolkit)

> **One-click Docker deployment for Ovis-Image 7B text-to-image model with Web UI, REST API, and MCP support**

Built upon [Ovis-U1](https://github.com/AIDC-AI/Ovis-U1), Ovis-Image is a 7B text-to-image model specifically optimized for high-quality text rendering, designed to operate efficiently under stringent computational constraints.

## ✨ Features

- 🚀 **One-Click Deployment** - Single command to start with automatic GPU selection
- 🎨 **Dual Mode** - Web UI + REST API in one container
- 🌍 **Multi-Language UI** - English, Chinese (Simplified/Traditional), Japanese
- 🔧 **Smart GPU Management** - Auto-select, lazy-load, auto-unload
- 📚 **Swagger API Docs** - Interactive API documentation
- 🔌 **MCP Support** - Model Context Protocol for Claude Desktop integration
- 💾 **Auto Model Download** - Automatic download from HuggingFace (~12GB)
- 🎯 **High-Quality Text Rendering** - Excellent text generation in images

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- NVIDIA GPU with 20GB+ VRAM
- NVIDIA Docker Runtime

### One-Command Start

```bash
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker
./start.sh
```

**Access:**
- 🎨 Web UI: http://localhost:7870
- 📚 API Docs: http://localhost:7870/docs
- 🖼️ Outputs: ./outputs/

## 📦 Installation

### Method 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker

# Start service
./start.sh

# The script will:
# - Auto-select GPU with lowest memory usage
# - Start Docker container with GPU support
# - Auto-download models on first run (~12GB)
```

### Method 2: Docker Compose

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional)
nano .env

# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Method 3: Manual Docker Run

```bash
docker run -d \
  --name ovis-image \
  --gpus all \
  -p 7870:7870 \
  -v $(pwd)/outputs:/app/outputs \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e MODEL_PATH=AIDC-AI/Ovis-Image-7B/ovis_image.safetensors \
  -e VAE_PATH=AIDC-AI/Ovis-Image-7B/ae.safetensors \
  -e OVIS_PATH=AIDC-AI/Ovis2.5-2B \
  -e PORT=7870 \
  -e IDLE_TIMEOUT=300 \
  ovis-image:latest
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `AIDC-AI/Ovis-Image-7B/ovis_image.safetensors` | Main model path |
| `VAE_PATH` | `AIDC-AI/Ovis-Image-7B/ae.safetensors` | VAE model path |
| `OVIS_PATH` | `AIDC-AI/Ovis2.5-2B` | Text encoder path |
| `PORT` | `7870` | Service port |
| `IDLE_TIMEOUT` | `300` | Auto-unload timeout (seconds) |

### Configuration File

Edit `.env` file:

```bash
MODEL_PATH=AIDC-AI/Ovis-Image-7B/ovis_image.safetensors
VAE_PATH=AIDC-AI/Ovis-Image-7B/ae.safetensors
OVIS_PATH=AIDC-AI/Ovis2.5-2B
PORT=7870
IDLE_TIMEOUT=300
```

## 📖 Usage

### Web UI

1. Open browser: http://localhost:7870
2. Enter prompt in text box
3. Adjust parameters (optional)
4. Click "Generate" button
5. Wait for image generation

### REST API

```bash
# Generate image
curl -X POST "http://localhost:7870/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }'

# Response
{
  "status": "success",
  "image": "/outputs/output_1234567890.png"
}

# Download image
curl -O http://localhost:7870/outputs/output_1234567890.png
```

### Python Client

```python
import requests

response = requests.post(
    "http://localhost:7870/api/generate",
    json={
        "prompt": "A cute cat wearing a hat",
        "image_size": 1024,
        "denoising_steps": 50,
        "cfg_scale": 5.0,
        "seed": 42
    }
)

result = response.json()
print(f"Image: {result['image']}")
```

### MCP Integration (Claude Desktop)

Add to Claude Desktop config:

```json
{
  "mcpServers": {
    "ovis-image": {
      "command": "python3",
      "args": ["/path/to/ovis-image-docker/mcp_server.py"],
      "env": {
        "API_BASE_URL": "http://localhost:7870"
      }
    }
  }
}
```

Then use in Claude:
```
"Generate an image of a red apple"
```

See [MCP_README.md](MCP_README.md) for details.

## 🎯 Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `prompt` | string | - | - | Text description of image |
| `image_size` | int | 1024 | 512-2048 | Output image size (square) |
| `denoising_steps` | int | 50 | 20-100 | Quality vs speed tradeoff |
| `cfg_scale` | float | 5.0 | 1.0-15.0 | Prompt adherence strength |
| `seed` | int | 42 | - | Reproducibility seed |

## 📊 Performance

| Resolution | Steps | Time | VRAM |
|------------|-------|------|------|
| 512x512 | 20 | ~10s | ~18GB |
| 1024x1024 | 50 | ~30s | ~20GB |
| 2048x2048 | 50 | ~2min | ~24GB |

**Requirements:**
- Minimum: 20GB VRAM (RTX 3090, A5000)
- Recommended: 24GB VRAM (RTX 4090, A5500, L40S)
- Optimal: 40GB+ VRAM (A100, H100)

## 🏗️ Project Structure

```
ovis-image-docker/
├── app.py                  # Main application (FastAPI + Gradio)
├── mcp_server.py          # MCP server implementation
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── start.sh               # One-click startup script
├── test_api.sh            # API testing script
├── test_mcp.py            # MCP testing script
├── .env.example           # Environment template
├── ovis_image/            # Core model code
│   ├── model/             # Model definitions
│   ├── sampling.py        # Sampling algorithms
│   └── utils.py           # Utilities
├── outputs/               # Generated images
└── docs/                  # Documentation
    ├── QUICK_START.md
    ├── README_DOCKER.md
    ├── MCP_README.md
    └── DEPLOYMENT_SUMMARY.md
```

## 🛠️ Tech Stack

- **Model**: Ovis-Image 7B + Ovis2.5-2B
- **Framework**: PyTorch 2.6.0, Transformers 4.57.1
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Gradio 4.0+
- **Container**: Docker, NVIDIA Docker Runtime
- **GPU**: CUDA 12.1, cuDNN 8
- **Protocol**: MCP (Model Context Protocol)

## 🔧 Management Commands

```bash
# View logs
docker-compose logs -f

# Restart service
docker-compose restart

# Stop service
docker-compose down

# Rebuild
docker-compose up -d --build

# Check GPU usage
nvidia-smi

# Test API
./test_api.sh 7870

# Test MCP
python3 test_mcp.py
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change port in .env
PORT=7871

# Restart
docker-compose down && ./start.sh
```

### Out of Memory

```bash
# Use smaller image size
image_size: 512
denoising_steps: 20

# Or wait for GPU to free up
nvidia-smi
```

### Model Download Slow

```bash
# Use HuggingFace mirror
export HF_ENDPOINT=https://hf-mirror.com
docker-compose restart
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### v1.0.0 (2025-12-04)
- ✨ Initial release
- 🚀 One-click Docker deployment
- 🎨 Web UI + REST API
- 🌍 Multi-language support
- 🔌 MCP integration
- 📚 Complete documentation

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ovis](https://github.com/AIDC-AI/Ovis) - Original model implementation
- [FLUX](https://github.com/black-forest-labs/flux) - Architecture inspiration
- [AIDC-AI](https://github.com/AIDC-AI) - Model training and release

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ovis-image-docker&type=Date)](https://star-history.com/#yourusername/ovis-image-docker)

## 📱 Follow Us

![WeChat](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)

---

**Made with ❤️ by the community**
