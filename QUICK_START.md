# 🚀 Ovis-Image 快速开始指南

## 一键启动

```bash
./start.sh
```

就这么简单！脚本会自动：
- 🔍 检测并选择显存占用最少的 GPU
- 🐳 启动 Docker 容器
- 📦 首次运行时自动下载模型（约 12GB）

## 访问服务

启动成功后，访问以下地址：

| 服务 | 地址 | 说明 |
|------|------|------|
| 🎨 Web UI | http://localhost:7870 | 图形界面，支持中英日多语言 |
| 📚 API 文档 | http://localhost:7870/docs | Swagger 交互式文档 |
| 🖼️ 图像输出 | ./outputs/ | 生成的图像保存位置 |

## 使用示例

### 方式 1: Web UI（推荐新手）

1. 打开浏览器访问 http://localhost:7870
2. 输入提示词，例如：
   ```
   A creative 3D artistic render where the text "HELLO" is written 
   in bold colorful letters
   ```
3. 调整参数（可选）
4. 点击"生成"按钮
5. 等待图像生成完成

### 方式 2: API 调用（推荐开发者）

```bash
curl -X POST "http://localhost:7870/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }'
```

### 方式 3: Python 脚本

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
print(f"✅ 图像已生成: {result['image']}")
```

## 常用命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 测试 API
./test_api.sh 7870

# 查看 GPU 使用
nvidia-smi
```

## 参数说明

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| image_size | 1024 | 图像尺寸，越大越慢 |
| denoising_steps | 50 | 质量，20=快速预览，50=标准，100=高质量 |
| cfg_scale | 5.0 | 提示词遵循度，越高越严格 |
| seed | 42 | 固定种子可复现相同结果 |

## 性能参考

| 分辨率 | 步数 | 预计时间 | 显存占用 |
|--------|------|----------|----------|
| 512x512 | 20 | ~10秒 | ~15GB |
| 1024x1024 | 50 | ~30秒 | ~18GB |
| 2048x2048 | 50 | ~2分钟 | ~22GB |

## 故障排查

### 问题：端口被占用
```bash
# 修改 .env 文件中的 PORT
PORT=7871
docker-compose down && ./start.sh
```

### 问题：显存不足
```bash
# 使用更小的图像尺寸
image_size: 512
denoising_steps: 20
```

### 问题：模型下载慢
```bash
# 使用 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com
docker-compose restart
```

## 下一步

- 📖 查看完整文档: [README_DOCKER.md](README_DOCKER.md)
- 📊 查看部署总结: [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)
- 🔧 查看原项目文档: [README.md](README.md)

---

**提示**: 首次使用需要下载约 12GB 模型，请耐心等待 10-15 分钟。
