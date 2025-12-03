# Ovis-Image MCP Server

Model Context Protocol (MCP) interface for Ovis-Image text-to-image generation.

## Features

- ✅ Generate images from text prompts
- ✅ List generated images
- ✅ Get image information
- ✅ Full parameter control (size, steps, CFG scale, seed)

## Installation

### 1. Install MCP Server

The MCP server is already included in the project:
- `mcp_server.py` - MCP server implementation
- `mcp_config.json` - MCP configuration

### 2. Configure MCP Client

Add to your MCP client configuration (e.g., Claude Desktop):

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

For Claude Desktop on macOS:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

For Claude Desktop on Windows:
```
%APPDATA%\Claude\claude_desktop_config.json
```

## Available Tools

### 1. generate_image

Generate an image from text prompt.

**Parameters:**
- `prompt` (required): Text description of the image
- `image_size` (optional): Image size 512-2048, default: 1024
- `denoising_steps` (optional): Denoising steps 20-100, default: 50
- `cfg_scale` (optional): CFG scale 1.0-15.0, default: 5.0
- `seed` (optional): Random seed, default: 42

**Example:**
```json
{
  "name": "generate_image",
  "arguments": {
    "prompt": "A beautiful sunset over mountains",
    "image_size": 1024,
    "denoising_steps": 50,
    "cfg_scale": 5.0,
    "seed": 42
  }
}
```

### 2. list_images

List all generated images.

**Example:**
```json
{
  "name": "list_images",
  "arguments": {}
}
```

### 3. get_image_info

Get information about a specific image.

**Parameters:**
- `filename` (required): Image filename

**Example:**
```json
{
  "name": "get_image_info",
  "arguments": {
    "filename": "output_1234567890.png"
  }
}
```

## Testing

### Test MCP Server

```bash
cd /home/neo/upload/Ovis-Image
python3 test_mcp.py
```

### Manual Test

```bash
# Start MCP server
python3 mcp_server.py

# Send request (in another terminal)
echo '{"method": "tools/list", "params": {}}' | python3 mcp_server.py
```

## Usage Examples

### With Claude Desktop

After configuring the MCP server, you can use it in Claude:

```
User: Generate an image of a red apple on a table

Claude will use the generate_image tool:
- prompt: "A red apple on a table"
- Returns: Image URL and path
```

### Programmatic Usage

```python
import json
import subprocess

def call_mcp_tool(tool_name, arguments):
    request = {
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    proc = subprocess.Popen(
        ['python3', 'mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    stdout, _ = proc.communicate(json.dumps(request) + '\n')
    return json.loads(stdout)

# Generate image
result = call_mcp_tool("generate_image", {
    "prompt": "A cute cat",
    "image_size": 512,
    "denoising_steps": 20
})

print(result)
```

## Architecture

```
┌─────────────────────────────────────────┐
│         MCP Client (Claude)             │
└─────────────────┬───────────────────────┘
                  │ MCP Protocol
                  │ (JSON-RPC over stdio)
┌─────────────────▼───────────────────────┐
│         mcp_server.py                   │
│  - tools/list                           │
│  - tools/call                           │
│  - initialize                           │
└─────────────────┬───────────────────────┘
                  │ HTTP REST API
┌─────────────────▼───────────────────────┐
│    Ovis-Image API (FastAPI)             │
│    http://localhost:7870                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│    Ovis-Image Model (Docker)            │
│    GPU 0 - 19.6GB                       │
└─────────────────────────────────────────┘
```

## Troubleshooting

### MCP Server not responding
```bash
# Check if API is running
curl http://localhost:7870/docs

# Check Docker container
docker ps | grep ovis-image
```

### Image generation fails
```bash
# Check GPU memory
nvidia-smi

# Check container logs
docker-compose logs -f
```

### Permission issues
```bash
# Make scripts executable
chmod +x mcp_server.py test_mcp.py
```

## API Endpoints Mapping

| MCP Tool | API Endpoint | Method |
|----------|--------------|--------|
| generate_image | /api/generate | POST |
| list_images | File system | - |
| get_image_info | /outputs/{filename} | GET |

## Performance

- Image generation: ~15-30 seconds (512x512, 20-50 steps)
- GPU memory: ~20GB
- Concurrent requests: Supported (queued)

## Security Notes

- MCP server runs locally
- API accessible on localhost:7870
- For remote access, configure firewall appropriately
- Consider adding authentication for production use

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Test API: `./test_api.sh 7870`
- Test MCP: `python3 test_mcp.py`
