# Ovis-Image Docker 部署

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.1-green.svg)](https://developer.nvidia.com/cuda-toolkit)

> **Ovis-Image 7B 文本生成图像模型的一键 Docker 部署方案，支持 Web UI、REST API 和 MCP 协议**

基于 [Ovis-U1](https://github.com/AIDC-AI/Ovis-U1) 构建，Ovis-Image 是一个 70 亿参数的文本生成图像模型，专门针对高质量文本渲染进行优化，在严格的计算约束下高效运行。

## ✨ 特性

- 🚀 **一键部署** - 单条命令启动，自动选择 GPU
- 🎨 **双模式** - Web UI + REST API 集成在一个容器
- 🌍 **多语言界面** - 支持英文、简体中文、繁体中文、日文
- 🔧 **智能 GPU 管理** - 自动选择、懒加载、自动卸载
- 📚 **Swagger API 文档** - 交互式 API 文档
- 🔌 **MCP 支持** - 支持 Claude Desktop 的模型上下文协议
- 💾 **自动下载模型** - 从 HuggingFace 自动下载（约 12GB）
- 🎯 **高质量文本渲染** - 图像中的文本生成效果出色

## 🚀 快速开始

### 前置要求

- Docker 和 Docker Compose
- NVIDIA GPU（20GB+ 显存）
- NVIDIA Docker Runtime

### 一键启动

```bash
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker
./start.sh
```

**访问地址：**
- 🎨 Web UI: http://localhost:7870
- 📚 API 文档: http://localhost:7870/docs
- 🖼️ 输出目录: ./outputs/

## 📦 安装

### 方式一：Docker（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker

# 启动服务
./start.sh

# 脚本会自动：
# - 选择显存占用最少的 GPU
# - 启动支持 GPU 的 Docker 容器
# - 首次运行时自动下载模型（约 12GB）
```

### 方式二：Docker Compose

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（可选）
nano .env

# 使用 docker-compose 启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 方式三：手动 Docker 运行

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

## ⚙️ 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MODEL_PATH` | `AIDC-AI/Ovis-Image-7B/ovis_image.safetensors` | 主模型路径 |
| `VAE_PATH` | `AIDC-AI/Ovis-Image-7B/ae.safetensors` | VAE 模型路径 |
| `OVIS_PATH` | `AIDC-AI/Ovis2.5-2B` | 文本编码器路径 |
| `PORT` | `7870` | 服务端口 |
| `IDLE_TIMEOUT` | `300` | 自动卸载超时（秒） |

### 配置文件

编辑 `.env` 文件：

```bash
MODEL_PATH=AIDC-AI/Ovis-Image-7B/ovis_image.safetensors
VAE_PATH=AIDC-AI/Ovis-Image-7B/ae.safetensors
OVIS_PATH=AIDC-AI/Ovis2.5-2B
PORT=7870
IDLE_TIMEOUT=300
```

## 📖 使用方法

### Web UI

1. 打开浏览器：http://localhost:7870
2. 在文本框中输入提示词
3. 调整参数（可选）
4. 点击"生成"按钮
5. 等待图像生成

### REST API

```bash
# 生成图像
curl -X POST "http://localhost:7870/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "山脉上的美丽日落",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }'

# 响应
{
  "status": "success",
  "image": "/outputs/output_1234567890.png"
}

# 下载图像
curl -O http://localhost:7870/outputs/output_1234567890.png
```

### Python 客户端

```python
import requests

response = requests.post(
    "http://localhost:7870/api/generate",
    json={
        "prompt": "一只戴帽子的可爱猫咪",
        "image_size": 1024,
        "denoising_steps": 50,
        "cfg_scale": 5.0,
        "seed": 42
    }
)

result = response.json()
print(f"图像: {result['image']}")
```

### MCP 集成（Claude Desktop）

添加到 Claude Desktop 配置：

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

然后在 Claude 中使用：
```
"生成一张红苹果的图片"
```

详见 [MCP_README.md](MCP_README.md)。

## 🎯 参数说明

| 参数 | 类型 | 默认值 | 范围 | 说明 |
|------|------|--------|------|------|
| `prompt` | string | - | - | 图像的文本描述 |
| `image_size` | int | 1024 | 512-2048 | 输出图像尺寸（正方形） |
| `denoising_steps` | int | 50 | 20-100 | 质量与速度的权衡 |
| `cfg_scale` | float | 5.0 | 1.0-15.0 | 提示词遵循强度 |
| `seed` | int | 42 | - | 可重现性种子 |

## 📊 性能

| 分辨率 | 步数 | 时间 | 显存 |
|--------|------|------|------|
| 512x512 | 20 | ~10秒 | ~18GB |
| 1024x1024 | 50 | ~30秒 | ~20GB |
| 2048x2048 | 50 | ~2分钟 | ~24GB |

**要求：**
- 最低：20GB 显存（RTX 3090、A5000）
- 推荐：24GB 显存（RTX 4090、A5500、L40S）
- 最佳：40GB+ 显存（A100、H100）

## 🏗️ 项目结构

```
ovis-image-docker/
├── app.py                  # 主应用程序（FastAPI + Gradio）
├── mcp_server.py          # MCP 服务器实现
├── Dockerfile             # Docker 镜像定义
├── docker-compose.yml     # Docker Compose 配置
├── start.sh               # 一键启动脚本
├── test_api.sh            # API 测试脚本
├── test_mcp.py            # MCP 测试脚本
├── .env.example           # 环境变量模板
├── ovis_image/            # 核心模型代码
│   ├── model/             # 模型定义
│   ├── sampling.py        # 采样算法
│   └── utils.py           # 工具函数
├── outputs/               # 生成的图像
└── docs/                  # 文档
    ├── QUICK_START.md
    ├── README_DOCKER.md
    ├── MCP_README.md
    └── DEPLOYMENT_SUMMARY.md
```

## 🛠️ 技术栈

- **模型**：Ovis-Image 7B + Ovis2.5-2B
- **框架**：PyTorch 2.6.0、Transformers 4.57.1
- **后端**：FastAPI、Uvicorn
- **前端**：Gradio 4.0+
- **容器**：Docker、NVIDIA Docker Runtime
- **GPU**：CUDA 12.1、cuDNN 8
- **协议**：MCP（模型上下文协议）

## 🔧 管理命令

```bash
# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 重新构建
docker-compose up -d --build

# 检查 GPU 使用
nvidia-smi

# 测试 API
./test_api.sh 7870

# 测试 MCP
python3 test_mcp.py
```

## 🐛 故障排查

### 端口已被占用

```bash
# 在 .env 中更改端口
PORT=7871

# 重启
docker-compose down && ./start.sh
```

### 显存不足

```bash
# 使用更小的图像尺寸
image_size: 512
denoising_steps: 20

# 或等待 GPU 释放
nvidia-smi
```

### 模型下载慢

```bash
# 使用 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com
docker-compose restart
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2025-12-04)
- ✨ 初始版本发布
- 🚀 一键 Docker 部署
- 🎨 Web UI + REST API
- 🌍 多语言支持
- 🔌 MCP 集成
- 📚 完整文档

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Ovis](https://github.com/AIDC-AI/Ovis) - 原始模型实现
- [FLUX](https://github.com/black-forest-labs/flux) - 架构灵感
- [AIDC-AI](https://github.com/AIDC-AI) - 模型训练和发布

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ovis-image-docker&type=Date)](https://star-history.com/#yourusername/ovis-image-docker)

## 📱 关注公众号

![公众号](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)

---

**用 ❤️ 制作**
