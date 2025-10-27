#!/bin/bash
# setup.sh - Run this before first use

# 1. Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# 2. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# 3. Install Python dependencies
echo "Installing dependencies..."
pip install pyautogen autogen-ext openai ollama

# 4. Pull Ollama models
MODELS=("deepseek-coder:6.7b" "llava:7b")
for MODEL in "${MODELS[@]}"; do
    echo "Pulling Ollama model: $MODEL ..."
    ollama pull $MODEL
done

# 5. Kill any existing Ollama server running on default port
echo "Checking for existing Ollama server..."
PID=$(lsof -ti tcp:11434)
if [ ! -z "$PID" ]; then
    echo "Killing existing Ollama server with PID $PID ..."
    kill -9 $PID
fi

# 6. Start Ollama server in the background
echo "Starting Ollama server..."
# The '&' at the end runs it in the background
ollama serve &

# Wait a few seconds to let the server start
sleep 5

echo "--------------------------------------"
echo "Setup complete! Ollama server is running in the background."
echo "You can now run your Python scripts:"
echo "  python basics.py       # for code/text tasks"
echo "  python multimodal_agent.py  # for vision/image tasks"
echo "--------------------------------------"

