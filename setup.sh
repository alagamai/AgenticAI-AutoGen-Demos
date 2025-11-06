#!/bin/bash
# ----------------------------------------------------
# 🚀 Full Setup for AutoGen (Python + Studio)
# ----------------------------------------------------

PROJECT_ROOT="$(pwd)"
VENV_PATH="$PROJECT_ROOT/.autogen"
AUTOGENSTUDIO_HOME="$PROJECT_ROOT/autogen-studio/.autogenstudio"


echo "📁 Using project root: $PROJECT_ROOT"

# 0️⃣ Check if env is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ ERROR: Virtual environment not activated."
    echo "👉 Please run: source activate_env.sh"
    echo "Then re-run: bash setup.sh"
    exit 1
fi

# Set AutoGen Studio home inside the project
export AUTOGENSTUDIO_HOME="$AUTOGENSTUDIO_HOME"
echo "📁 Setting AutoGen Studio home to: $AUTOGENSTUDIO_HOME"

# Create the directory if missing
mkdir -p "$AUTOGENSTUDIO_HOME"


# 1️⃣ Ensure Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "⚙️ Installing Python 3.11..."
    brew install python@3.11
fi

# 2️⃣ Create virtual environment if missing
if [ ! -d "$VENV_PATH" ]; then
    echo "🧱 Creating virtual environment (.autogen)..."
    python3.11 -m venv "$VENV_PATH"
else
    echo "✅ Virtual environment already exists."
fi

# 3️⃣ Activate env (redundant but safe)
source "$VENV_PATH/bin/activate"

# 4️⃣ Upgrade pip & wheel
echo "⬆️ Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# 5️⃣ Install core AutoGen + Studio
echo "📦 Installing AutoGen and dependencies..."
pip install -U autogen-core==0.6.4 autogen-agentchat==0.6.4 autogen-ext==0.6.4
pip install -U autogenstudio==0.4.3.dev2
pip install openai ollama tiktoken

# 6️⃣ Verify setup
python -c "import autogen, autogenstudio; print('✅ AutoGen + Studio imported successfully')"

# 7️⃣ Pull Ollama models
MODELS=("deepseek-coder:6.7b" "llava:7b" "llama3.1:latest")
for MODEL in "${MODELS[@]}"; do
    echo "📥 Pulling Ollama model: $MODEL ..."
    ollama pull "$MODEL"
done

# 8️⃣ Restart Ollama server cleanly
PID=$(lsof -ti tcp:11434)
if [ ! -z "$PID" ]; then
    echo "🧹 Restarting Ollama server..."
    kill -9 "$PID"
fi
ollama serve &

sleep 5
curl http://localhost:11434/api/tags || echo "⚠️ Ollama not responding yet..."

# 9️⃣ Set AutoGen Studio data path
mkdir -p "$AUTOGENSTUDIO_HOME"
export AUTOGENSTUDIO_HOME

# 🔟 Done
echo "--------------------------------------"
echo "✅ Setup Complete!"
echo "Virtual Env: $VENV_PATH"
echo "Studio Data: $AUTOGENSTUDIO_HOME"
echo "--------------------------------------"
echo "Next steps:"
echo "  1️⃣ Run:  source activate_env.sh"
echo "  2️⃣ Launch Studio UI:  autogenstudio ui"
echo "--------------------------------------"

