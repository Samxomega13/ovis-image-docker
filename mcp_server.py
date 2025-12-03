#!/usr/bin/env python3
"""
Ovis-Image MCP Server
Provides Model Context Protocol interface for Ovis-Image text-to-image generation
"""
import os
import json
import asyncio
from typing import Any
import requests

# MCP Server configuration
MCP_SERVER_NAME = "ovis-image"
MCP_SERVER_VERSION = "1.0.0"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7870")

def generate_image(prompt: str, image_size: int = 1024, denoising_steps: int = 50, 
                   cfg_scale: float = 5.0, seed: int = 42) -> dict:
    """Generate image using Ovis-Image API"""
    url = f"{API_BASE_URL}/api/generate"
    payload = {
        "prompt": prompt,
        "image_size": image_size,
        "denoising_steps": denoising_steps,
        "cfg_scale": cfg_scale,
        "seed": seed
    }
    response = requests.post(url, json=payload, timeout=300)
    return response.json()

def get_image_url(filename: str) -> str:
    """Get full URL for generated image"""
    return f"{API_BASE_URL}{filename}"

def list_generated_images() -> list:
    """List all generated images"""
    outputs_dir = "/app/outputs"
    if not os.path.exists(outputs_dir):
        return []
    files = [f for f in os.listdir(outputs_dir) if f.endswith('.png')]
    return sorted(files, reverse=True)

# MCP Protocol Implementation
async def handle_mcp_request(request: dict) -> dict:
    """Handle MCP protocol requests"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "generate_image",
                    "description": "Generate an image from text prompt using Ovis-Image model",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Text description of the image to generate"
                            },
                            "image_size": {
                                "type": "integer",
                                "description": "Image size (512-2048, default: 1024)",
                                "default": 1024
                            },
                            "denoising_steps": {
                                "type": "integer",
                                "description": "Number of denoising steps (20-100, default: 50)",
                                "default": 50
                            },
                            "cfg_scale": {
                                "type": "number",
                                "description": "Classifier-free guidance scale (1.0-15.0, default: 5.0)",
                                "default": 5.0
                            },
                            "seed": {
                                "type": "integer",
                                "description": "Random seed for reproducibility (default: 42)",
                                "default": 42
                            }
                        },
                        "required": ["prompt"]
                    }
                },
                {
                    "name": "list_images",
                    "description": "List all generated images",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "get_image_info",
                    "description": "Get information about a generated image",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Image filename"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "generate_image":
            result = generate_image(
                prompt=arguments.get("prompt"),
                image_size=arguments.get("image_size", 1024),
                denoising_steps=arguments.get("denoising_steps", 50),
                cfg_scale=arguments.get("cfg_scale", 5.0),
                seed=arguments.get("seed", 42)
            )
            if result.get("status") == "success":
                image_path = result.get("image")
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Image generated successfully!\nURL: {get_image_url(image_path)}\nPath: {image_path}"
                        },
                        {
                            "type": "resource",
                            "resource": {
                                "uri": get_image_url(image_path),
                                "mimeType": "image/png"
                            }
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: {result.get('detail', 'Unknown error')}"
                        }
                    ],
                    "isError": True
                }
        
        elif tool_name == "list_images":
            images = list_generated_images()
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Found {len(images)} generated images:\n" + "\n".join(images)
                    }
                ]
            }
        
        elif tool_name == "get_image_info":
            filename = arguments.get("filename")
            filepath = f"/app/outputs/{filename}"
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Image: {filename}\nSize: {size} bytes\nURL: {get_image_url(f'/outputs/{filename}')}"
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Image not found: {filename}"
                        }
                    ],
                    "isError": True
                }
    
    elif method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": MCP_SERVER_NAME,
                "version": MCP_SERVER_VERSION
            }
        }
    
    return {"error": "Unknown method"}

async def main():
    """Main MCP server loop"""
    import sys
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line)
            response = await handle_mcp_request(request)
            
            print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {
                "error": str(e)
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
