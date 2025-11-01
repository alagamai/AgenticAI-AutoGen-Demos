#!/bin/bash
# ----------------------------------------------------
# ⚡ Quick Activator for AutoGen Environment
# ----------------------------------------------------

PROJECT_ROOT="$(pwd)"
VENV_PATH="$PROJECT_ROOT/.autogen"
AUTOGENSTUDIO_HOME="$PROJECT_ROOT/autogen-studio/.autogenstudio"

# Create the venv if missing
if [ ! -d "$VENV_PATH" ]; then
    echo "⚙️  No virtual environment found. Creating one at:"
    echo "   $VENV_PATH"
    python3.11 -m venv "$VENV_PATH"
    echo "✅ Virtual environment created successfully."
fi

# Activate environment
echo "🔹 Activating AutoGen environment from: $VENV_PATH"
source "$VENV_PATH/bin/activate"

# Export studio data dir so Studio uses this folder
export AUTOGENSTUDIO_HOME="$AUTOGENSTUDIO_HOME"
mkdir -p "$AUTOGENSTUDIO_HOME"

alias agstudio='AUTOGENSTUDIO_HOME="$PWD/autogen-studio/.autogenstudio" AUTOGEN_CONFIG_HOME="$PWD/autogen-studio/.autogenstudio" autogenstudio ui --appdir "$PWD/autogen-studio/.autogenstudio"'


echo "✅ Environment activated successfully."
echo "Virtual Env: $VENV_PATH"
echo "Studio Data: $AUTOGENSTUDIO_HOME"
echo "--------------------------------------"
echo "Next steps:"
echo "  1️⃣ Run:  ./setup.sh"
echo "  2️⃣ Launch Studio UI:  autogenstudio ui"
echo "--------------------------------------"

