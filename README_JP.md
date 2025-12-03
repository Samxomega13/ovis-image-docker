# Ovis-Image Docker デプロイ

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.1-green.svg)](https://developer.nvidia.com/cuda-toolkit)

> **Ovis-Image 7B テキスト画像生成モデルのワンクリック Docker デプロイ、Web UI、REST API、MCP サポート付き**

[Ovis-U1](https://github.com/AIDC-AI/Ovis-U1) をベースに構築された Ovis-Image は、高品質なテキストレンダリングに最適化された 70 億パラメータのテキスト画像生成モデルです。

## ✨ 特徴

- 🚀 **ワンクリックデプロイ** - 単一コマンドで起動、GPU 自動選択
- 🎨 **デュアルモード** - Web UI + REST API を 1 つのコンテナに統合
- 🌍 **多言語 UI** - 英語、中国語（簡体字/繁体字）、日本語対応
- 🔧 **スマート GPU 管理** - 自動選択、遅延ロード、自動アンロード
- 📚 **Swagger API ドキュメント** - インタラクティブ API ドキュメント
- 🔌 **MCP サポート** - Claude Desktop のモデルコンテキストプロトコル対応
- 💾 **自動モデルダウンロード** - HuggingFace から自動ダウンロード（約 12GB）

## 🚀 クイックスタート

```bash
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker
./start.sh
```

**アクセス：**
- 🎨 Web UI: http://localhost:7870
- 📚 API ドキュメント: http://localhost:7870/docs

## 📦 インストール

### Docker デプロイ（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/ovis-image-docker.git
cd ovis-image-docker

# サービスを起動
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
    "prompt": "山の上の美しい夕日",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }'
```

## 🎯 パラメータ

| パラメータ | 型 | デフォルト | 範囲 | 説明 |
|-----------|------|---------|------|------|
| `prompt` | string | - | - | 画像のテキスト説明 |
| `image_size` | int | 1024 | 512-2048 | 出力画像サイズ |
| `denoising_steps` | int | 50 | 20-100 | 品質と速度のトレードオフ |
| `cfg_scale` | float | 5.0 | 1.0-15.0 | プロンプト遵守強度 |
| `seed` | int | 42 | - | 再現性シード |

## 📊 パフォーマンス

| 解像度 | ステップ | 時間 | VRAM |
|--------|---------|------|------|
| 512x512 | 20 | ~10秒 | ~18GB |
| 1024x1024 | 50 | ~30秒 | ~20GB |
| 2048x2048 | 50 | ~2分 | ~24GB |

**要件：**
- 最小：20GB VRAM（RTX 3090、A5000）
- 推奨：24GB VRAM（RTX 4090、A5500、L40S）

## 🛠️ 技術スタック

- **モデル**：Ovis-Image 7B + Ovis2.5-2B
- **フレームワーク**：PyTorch 2.6.0、Transformers 4.57.1
- **バックエンド**：FastAPI、Uvicorn
- **フロントエンド**：Gradio 4.0+
- **コンテナ**：Docker、NVIDIA Docker Runtime

## 📄 ライセンス

このプロジェクトは Apache License 2.0 の下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ovis-image-docker&type=Date)](https://star-history.com/#yourusername/ovis-image-docker)

## 📱 公式アカウントをフォロー

![WeChat](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)
