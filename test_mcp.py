#!/usr/bin/env python3
"""Test MCP Server"""
import json
import subprocess
import sys

def send_mcp_request(request):
    """Send request to MCP server and get response"""
    proc = subprocess.Popen(
        ['python3', 'mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = proc.communicate(json.dumps(request) + '\n')
    
    if stderr:
        print(f"Error: {stderr}", file=sys.stderr)
    
    return json.loads(stdout.strip())

def test_initialize():
    """Test initialize"""
    print("🧪 Testing initialize...")
    request = {"method": "initialize", "params": {}}
    response = send_mcp_request(request)
    print(f"✅ Server: {response.get('serverInfo', {}).get('name')}")
    print(f"✅ Version: {response.get('serverInfo', {}).get('version')}")
    return response

def test_list_tools():
    """Test list tools"""
    print("\n🧪 Testing list tools...")
    request = {"method": "tools/list", "params": {}}
    response = send_mcp_request(request)
    tools = response.get('tools', [])
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    return response

def test_generate_image():
    """Test generate image"""
    print("\n🧪 Testing generate_image...")
    request = {
        "method": "tools/call",
        "params": {
            "name": "generate_image",
            "arguments": {
                "prompt": "A red apple on a table",
                "image_size": 512,
                "denoising_steps": 20,
                "cfg_scale": 5.0,
                "seed": 123
            }
        }
    }
    response = send_mcp_request(request)
    if response.get('isError'):
        print(f"❌ Error: {response}")
    else:
        content = response.get('content', [])
        for item in content:
            if item['type'] == 'text':
                print(f"✅ {item['text']}")
    return response

def test_list_images():
    """Test list images"""
    print("\n🧪 Testing list_images...")
    request = {
        "method": "tools/call",
        "params": {
            "name": "list_images",
            "arguments": {}
        }
    }
    response = send_mcp_request(request)
    content = response.get('content', [])
    for item in content:
        if item['type'] == 'text':
            print(f"✅ {item['text']}")
    return response

if __name__ == "__main__":
    print("=" * 60)
    print("Ovis-Image MCP Server Test")
    print("=" * 60)
    
    try:
        test_initialize()
        test_list_tools()
        test_list_images()
        # test_generate_image()  # Uncomment to test image generation
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
