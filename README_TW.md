# Ovis-Image Docker 部署

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.1-green.svg)](https://developer.nvidia.com/cuda-toolkit)

> **Ovis-Image 7B 文字生成圖像模型的一鍵 Docker 部署方案，支援 Web UI、REST API 和 MCP 協定**

基於 [Ovis-U1](https://github.com/AIDC-AI/Ovis-U1) 構建，Ovis-Image 是一個 70 億參數的文字生成圖像模型，專門針對高品質文字渲染進行優化。

## ✨ 特性

- 🚀 **一鍵部署** - 單條命令啟動，自動選擇 GPU
- 🎨 **雙模式** - Web UI + REST API 整合在一個容器
- 🌍 **多語言介面** - 支援英文、簡體中文、繁體中文、日文
- 🔧 **智慧 GPU 管理** - 自動選擇、懶載入、自動卸載
- 📚 **Swagger API 文件** - 互動式 API 文件
- 🔌 **MCP 支援** - 支援 Claude Desktop 的模型上下文協定
- 💾 **自動下載模型** - 從 HuggingFace 自動下載（約 12GB）

## 🚀 快速開始

```bash
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker
./start.sh
```

**訪問地址：**
- 🎨 Web UI: http://localhost:7870
- 📚 API 文件: http://localhost:7870/docs

## 📦 安裝

### Docker 部署（推薦）

```bash
# 克隆倉庫
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker

# 啟動服務
./start.sh
```

### Docker Compose

```bash
cp .env.example .env
docker-compose up -d
```

## 📖 使用方法

### REST API

```bash
curl -X POST "http://localhost:7870/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "山脈上的美麗日落",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }'
```

## 🎯 參數說明

| 參數 | 類型 | 預設值 | 範圍 | 說明 |
|------|------|--------|------|------|
| `prompt` | string | - | - | 圖像的文字描述 |
| `image_size` | int | 1024 | 512-2048 | 輸出圖像尺寸 |
| `denoising_steps` | int | 50 | 20-100 | 品質與速度的權衡 |
| `cfg_scale` | float | 5.0 | 1.0-15.0 | 提示詞遵循強度 |
| `seed` | int | 42 | - | 可重現性種子 |

## 📊 效能

| 解析度 | 步數 | 時間 | 顯存 |
|--------|------|------|------|
| 512x512 | 20 | ~10秒 | ~18GB |
| 1024x1024 | 50 | ~30秒 | ~20GB |
| 2048x2048 | 50 | ~2分鐘 | ~24GB |

**要求：**
- 最低：20GB 顯存（RTX 3090、A5000）
- 推薦：24GB 顯存（RTX 4090、A5500、L40S）

## 🛠️ 技術棧

- **模型**：Ovis-Image 7B + Ovis2.5-2B
- **框架**：PyTorch 2.6.0、Transformers 4.57.1
- **後端**：FastAPI、Uvicorn
- **前端**：Gradio 4.0+
- **容器**：Docker、NVIDIA Docker Runtime

## 📄 授權

本專案採用 Apache License 2.0 授權 - 詳見 [LICENSE](LICENSE) 檔案。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ovis-image-docker&type=Date)](https://star-history.com/#yourusername/ovis-image-docker)

## 📱 關注公眾號

![公眾號](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)
