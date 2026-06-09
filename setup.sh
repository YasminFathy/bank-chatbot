#!/usr/bin/env bash
# setup.sh — run once after cloning to install dependencies and create .env
set -e

echo ""
echo "=== Bank Transaction Chatbot — Setup ==="
echo ""

# Install dependencies
echo "[1/3] Installing dependencies..."
pip install -r requirements.txt --user --quiet

# Install pytest-asyncio separately to ensure latest version
echo "[2/4] Installing pytest-asyncio..."
pip install pytest-asyncio --upgrade --user --quiet


export PATH=$PATH:$HOME/.local/bin
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc 2>/dev/null || true

# Verify adk is available
if ! command -v adk &> /dev/null; then
    echo "ERROR: 'adk' command not found after install."
    echo "Run: export PATH=\$PATH:\$HOME/.local/bin"
    exit 1
fi

echo "[2/3] ADK version: $(adk --version)"

# Create .env if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[3/3] Created .env from .env.example"
    echo ""
    echo "  *** ACTION REQUIRED ***"
    echo "  Edit .env and replace 'your_aistudio_key_here' with your real API key."
    echo "  Get a free key at: https://aistudio.google.com"
    echo ""
else
    echo "[3/3] .env already exists — skipping"
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Add GOOGLE_API_KEY to .env (if not done)"
echo "  2. CLI mode:  python main.py"
echo "  3. Web UI:    adk web --host 0.0.0.0 --port 8080 --allow_origins 'regex:https://.*\.cloudshell\.dev'"
echo "  4. Tests:     pytest tests/ -v"
echo ""
