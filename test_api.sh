#!/bin/bash

PORT=${1:-7870}

echo "🧪 Testing Ovis-Image API on port $PORT..."
echo ""

echo "1️⃣ Testing UI endpoint..."
UI_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/)
if [ "$UI_RESPONSE" = "200" ]; then
    echo "✅ UI is accessible at http://localhost:$PORT/"
else
    echo "❌ UI failed with status code: $UI_RESPONSE"
fi
echo ""

echo "2️⃣ Testing API docs..."
DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/docs)
if [ "$DOCS_RESPONSE" = "200" ]; then
    echo "✅ API docs accessible at http://localhost:$PORT/docs"
else
    echo "❌ API docs failed with status code: $DOCS_RESPONSE"
fi
echo ""

echo "3️⃣ Testing image generation API..."
echo "   (This will take some time as models need to load...)"

RESPONSE=$(curl -s -X POST "http://localhost:$PORT/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A simple red circle on white background",
    "image_size": 512,
    "denoising_steps": 20,
    "cfg_scale": 5.0,
    "seed": 42
  }')

if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ Image generation successful!"
    IMAGE_PATH=$(echo "$RESPONSE" | grep -o '/outputs/[^"]*')
    echo "   Image saved to: $IMAGE_PATH"
    
    # Test image download
    IMAGE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT$IMAGE_PATH)
    if [ "$IMAGE_RESPONSE" = "200" ]; then
        echo "✅ Image download successful"
    else
        echo "❌ Image download failed with status code: $IMAGE_RESPONSE"
    fi
else
    echo "❌ Image generation failed"
    echo "   Response: $RESPONSE"
fi
echo ""

echo "4️⃣ Checking GPU usage..."
docker exec ovis-image nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo "⚠️  Could not query GPU info"
echo ""

echo "✨ Test complete!"
