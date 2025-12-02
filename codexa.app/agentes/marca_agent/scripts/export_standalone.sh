#!/bin/bash
# Brand Agent Standalone - Export Script for OpenAI Agent Builder
# Version: 1.0
# Date: 2025-11-09

set -e  # Exit on error

echo "================================================"
echo "  Brand Agent Standalone - Export Package"
echo "================================================"
echo ""

# Configuration
EXPORT_DIR="export_package"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
EXPORT_ZIP="brand-agent-export_${TIMESTAMP}.zip"

# Clean previous exports
echo "🧹 Cleaning previous exports..."
rm -rf "$EXPORT_DIR"
rm -f brand-agent-export_*.zip

# Create export directory
echo "📁 Creating export directory..."
mkdir -p "$EXPORT_DIR"

# Copy core files
echo "📋 Copying core files..."
cp README.md "$EXPORT_DIR/" 2>/dev/null || echo "⚠️  README.md not found"
cp QUICK_START.md "$EXPORT_DIR/" 2>/dev/null || echo "⚠️  QUICK_START.md not found"
cp IMPROVEMENT_ANALYSIS.md "$EXPORT_DIR/" 2>/dev/null || echo "⚠️  IMPROVEMENT_ANALYSIS.md not found"
cp IMPROVEMENTS_SUMMARY.md "$EXPORT_DIR/" 2>/dev/null || echo "⚠️  IMPROVEMENTS_SUMMARY.md not found"
cp ROADMAP_MELHORIAS.md "$EXPORT_DIR/" 2>/dev/null || echo "⚠️  ROADMAP_MELHORIAS.md not found"

# Copy vector store files (PRIORITY)
echo "📦 Copying OpenAI Vector Store files..."
if [ -d "openai_vector_store" ]; then
    cp -r openai_vector_store "$EXPORT_DIR/"

    # Count files
    FILE_COUNT=$(find "$EXPORT_DIR/openai_vector_store" -type f | wc -l)
    echo "   ✅ Copied $FILE_COUNT files from openai_vector_store/"
else
    echo "   ❌ ERROR: openai_vector_store/ directory not found!"
    exit 1
fi

# Copy config files
echo "⚙️  Copying config files..."
if [ -d "config" ]; then
    cp -r config "$EXPORT_DIR/"
    echo "   ✅ Config files copied"
else
    echo "   ⚠️  config/ directory not found (optional)"
fi

# Copy validation scripts (optional)
if [ -d "scripts" ]; then
    echo "🧪 Copying validation scripts..."
    cp -r scripts "$EXPORT_DIR/"
    echo "   ✅ Scripts copied"
fi

# Create manifest file
echo "📝 Creating EXPORT_MANIFEST.txt..."
cat > "$EXPORT_DIR/EXPORT_MANIFEST.txt" << EOF
========================================
BRAND AGENT STANDALONE - Export Package
========================================

Export Date: $(date)
Export Version: 1.0

CONTENTS:
---------
📁 openai_vector_store/       - Upload ALL these files to OpenAI Vector Store
📁 config/                    - Configuration files (brand_archetypes.json)
📁 scripts/                   - Validation scripts (brand_validator.py)
📄 README.md                  - Main documentation
📄 QUICK_START.md             - Quick start guide
📄 IMPROVEMENT_ANALYSIS.md    - Gap analysis and roadmap
📄 IMPROVEMENTS_SUMMARY.md    - What was implemented
📄 ROADMAP_MELHORIAS.md       - Original improvement roadmap

INSTRUCTIONS:
-------------
1. Go to: https://platform.openai.com/agents
2. Create New Agent or open existing Brand Strategy Agent
3. Upload ALL files from openai_vector_store/ to Vector Store
4. Paste MASTER_INSTRUCTIONS.md content into Instructions field
5. Enable tools: file_search + code_interpreter
6. Set model: gpt-4-turbo or gpt-4o
7. Save and test with sample brief

PRIORITY FILES (Must upload):
------------------------------
EOF

# List priority files
if [ -f "$EXPORT_DIR/openai_vector_store/MASTER_INSTRUCTIONS.md" ]; then
    echo "✅ MASTER_INSTRUCTIONS.md" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"
fi
if [ -f "$EXPORT_DIR/openai_vector_store/OUTPUT_SCHEMA.md" ]; then
    echo "✅ OUTPUT_SCHEMA.md" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"
fi
if [ -f "$EXPORT_DIR/openai_vector_store/brand_archetypes.json" ]; then
    echo "✅ brand_archetypes.json" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"
fi
if [ -f "$EXPORT_DIR/openai_vector_store/positioning_frameworks.json" ]; then
    echo "✅ positioning_frameworks.json" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"
fi
if [ -f "$EXPORT_DIR/openai_vector_store/tone_taxonomies.json" ]; then
    echo "✅ tone_taxonomies.json" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"
fi

echo "" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"
echo "Total files in package: $(find $EXPORT_DIR -type f | wc -l)" >> "$EXPORT_DIR/EXPORT_MANIFEST.txt"

# Create ZIP archive
echo ""
echo "📦 Creating ZIP archive..."
if command -v zip &> /dev/null; then
    zip -r -q "$EXPORT_ZIP" "$EXPORT_DIR"
    ZIP_SIZE=$(du -h "$EXPORT_ZIP" | cut -f1)
    echo "   ✅ Archive created: $EXPORT_ZIP ($ZIP_SIZE)"
else
    echo "   ⚠️  'zip' command not found. Using tar instead..."
    tar -czf "${EXPORT_ZIP%.zip}.tar.gz" "$EXPORT_DIR"
    echo "   ✅ Archive created: ${EXPORT_ZIP%.zip}.tar.gz"
fi

# Summary
echo ""
echo "================================================"
echo "✅ EXPORT COMPLETE!"
echo "================================================"
echo ""
echo "📦 Package location:"
if [ -f "$EXPORT_ZIP" ]; then
    echo "   $(pwd)/$EXPORT_ZIP"
elif [ -f "${EXPORT_ZIP%.zip}.tar.gz" ]; then
    echo "   $(pwd)/${EXPORT_ZIP%.zip}.tar.gz"
fi
echo ""
echo "📁 Uncompressed package:"
echo "   $(pwd)/$EXPORT_DIR/"
echo ""
echo "📋 Next steps:"
echo "   1. Extract the archive or use $EXPORT_DIR/ directly"
echo "   2. Read EXPORT_MANIFEST.txt for upload instructions"
echo "   3. Upload files to OpenAI Agent Builder"
echo ""
echo "================================================"
