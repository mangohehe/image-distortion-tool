#!/bin/bash

# Setup script for Image Distortion Tool workspace

echo "🖼️  Image Distortion Tool - Workspace Setup"
echo "=========================================="

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p workspace/input/images
mkdir -p workspace/input/masks
mkdir -p workspace/pipelines
mkdir -p workspace/output
mkdir -p workspace/logs

# Create default pipeline
echo "⚙️  Creating default pipeline..."
cat > workspace/pipelines/default.json <<EOF
{
  "metadata": {
    "name": "Default Pipeline",
    "version": "1.0",
    "created_at": "$(date -Iseconds)",
    "description": "Simple optical distortion for testing"
  },
  "transforms": [
    {
      "id": "t1",
      "type": "OpticalDistortion",
      "category": "geometric",
      "params": {
        "distort_limit": 0.2,
        "shift_limit": 0.1,
        "p": 1.0
      }
    }
  ],
  "compose": {
    "type": "Sequential"
  }
}
EOF

echo ""
echo "✅ Workspace initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Copy your images to ./workspace/input/images/"
echo "2. (Optional) Copy masks to ./workspace/input/masks/"
echo "3. Run: docker-compose up"
echo "4. Open browser to http://localhost:8501"
echo ""
echo "Directory structure created at ./workspace/"
