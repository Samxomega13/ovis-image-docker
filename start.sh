#!/bin/bash

set -e

echo "🔍 Finding GPU with lowest memory usage..."

get_gpu_memory() {
    nvidia-smi --query-gpu=index,memory.used --format=csv,noheader,nounits | \
    awk '{print $1, $2}' | sort -k2 -n | head -1 | awk '{print $1}'
}

GPU_ID=$(get_gpu_memory)
echo "✅ Selected GPU: $GPU_ID"

if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
fi

export GPU_ID=$GPU_ID
source .env

echo "🐳 Starting Docker container..."
docker-compose up -d

echo "✅ Container started on GPU $GPU_ID"
echo "🌐 Access UI at: http://localhost:${PORT}"
echo "📚 API docs at: http://localhost:${PORT}/docs"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"
