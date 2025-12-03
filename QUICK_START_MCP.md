# 🚀 Ovis-Image MCP 快速开始

## 什么是 MCP？

Model Context Protocol (MCP) 是一个开放协议，让 AI 助手（如 Claude）可以直接调用本地工具和服务。

## 一键配置

### 1. 确保服务运行

```bash
cd /home/neo/upload/Ovis-Image
./start.sh
```

### 2. 配置 Claude Desktop

**macOS:**
```bash
# 编辑配置文件
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
记事本打开: %APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

**添加以下配置:**
```json
{
  "mcpServers": {
    "ovis-image": {
      "command": "python3",
      "args": ["/home/neo/upload/Ovis-Image/mcp_server.py"],
      "env": {
        "API_BASE_URL": "http://localhost:7870"
      }
    }
  }
}
```

### 3. 重启 Claude Desktop

配置完成后，重启 Claude Desktop 即可使用。

## 使用示例

在 Claude 中直接对话：

```
你: 帮我生成一张红色苹果的图片

Claude 会自动调用 generate_image 工具，返回图片链接
```

```
你: 列出所有已生成的图片

Claude 会调用 list_images 工具
```

## 可用功能

| 功能 | 说明 | 示例 |
|------|------|------|
| 生成图片 | 从文本生成图像 | "生成一只猫的图片" |
| 列出图片 | 查看所有生成的图片 | "显示所有图片" |
| 图片信息 | 获取图片详情 | "查看 output_xxx.png 的信息" |

## 参数说明

生成图片时可以指定：
- **提示词**: 图片描述
- **尺寸**: 512-2048 (默认 1024)
- **步数**: 20-100 (默认 50)
- **引导比例**: 1.0-15.0 (默认 5.0)
- **随机种子**: 任意整数 (默认 42)

## 测试

```bash
# 测试 MCP 服务器
cd /home/neo/upload/Ovis-Image
python3 test_mcp.py
```

## 故障排查

### Claude 找不到工具
1. 检查配置文件路径是否正确
2. 重启 Claude Desktop
3. 查看 Claude 的开发者工具（如有）

### 生成失败
```bash
# 检查服务状态
docker ps | grep ovis-image

# 查看日志
docker-compose logs -f
```

## 完整文档

详细文档请查看: [MCP_README.md](MCP_README.md)
