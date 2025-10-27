# 🤖 AgenticAI Demos – AutoGen + Ollama + Multi-Agent Systems

This repository showcases **Agentic AI examples** using AutoGen, Ollama, and local models like DeepSeek and LLaVA.  
It includes single-agent, multi-agent, multimodal (vision + text), and human-in-the-loop QA testing examples.

---

## 🌟 Example Scripts

| Script | Description | Screenshot / Test Result |
|--------|-------------|-------------------------|
| `single_agent.py` | Single-agent demo using DeepSeek for code/text tasks | ![Placeholder](docs/screenshots/single_agent.png) |
| `multi-agent.py` | Multi-agent (Round Robin) demo – teacher & student agents | ![Placeholder](docs/screenshots/multi_agent.png) |
| `multimodal_agent.py` | Vision + text processing using LLaVA | ![Placeholder](docs/screenshots/multimodal_agent.png) |
| `human-in-the-loop.py` | QA workflow where one agent validates another | ![Placeholder](docs/screenshots/human_in_the_loop.png) |

> Add your screenshots or exported test results in `docs/screenshots/` and update links above.

---
##  🧩 Highlights

---
🧠 Multi Agent coordination (teacher ↔ student - DeepSeek model)
🖼 Vision + text understanding (LLaVA)
![multi agent](screenshots/multiagent.png)

💬 Multimodal Agent (Vision - LLaVA model)
![multimodal agent](screenshots/multimodal.png)

🧪 Human-in-the-loop QA testing (DeepSeek model))
![Human In The Loop](screenshots/human1.png)
![Human In The Loop](screenshots/human2.png)


🧰 Fully integrated with Ollama local inference




## 🚀 Quick Setup (PyCharm + Ollama)

---
1. **Clone the repository**

```bash
git clone https://github.com/<yourusername>/AgenticAI-Demos.git
cd AgenticAI-Demos

2. **Run setup script**
 (creates virtual environment, installs dependencies, pulls Ollama model, starts server)

bash setup.sh

The setup script runs Ollama in the background. Keep it running while executing examples.

3. **Run any example in PyCharm**

Go to examples folder -> Open the script in PyCharm.

Ensure the interpreter points to .venv.

Run the script using Run → Run 'script_name'.
