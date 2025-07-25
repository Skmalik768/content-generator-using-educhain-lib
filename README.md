# 🧠 EduChain MCP Server (Claude + Ollama)

This project exposes **educational AI tools** like multiple choice question (MCQ) generation, lesson planning, and flashcard creation via the **Model Context Protocol (MCP)**.

It connects:
- ✅ Local **Python MCP server**
- ✅ Local **Ollama LLM (e.g., Gemma)**
- ✅ **Claude for Desktop** using `claude_desktop_config.json`

---

## 🚀 Features

| Tool Name              | Description |
|------------------------|-------------|
| `generate_mcqs`        | Generates MCQs for a given topic |
| `generate_lesson_plan` | Creates structured lesson plans |
| `generate_flashcards`  | Builds flashcards from topics |

Powered by [`Educhain`](https://github.com/ritobanrc/educhain) and a local LLM from Ollama.

---

## 📁 Project Structure

mcp-educhain-server/
├── mcp_server.py # Main MCP server
├── educhain_content.py # AI tool logic using Educhain + Ollama
├── claude_desktop_config.json # Claude config (external)
├── README.md

yaml
Copy
Edit

---

## ⚙️ Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) (e.g., `gemma`, `mistral`)
- Claude for Desktop
- Dependencies:
  ```bash
  pip install educhain langchain_ollama
🔌 Claude Config (claude_desktop_config.json)
Located at:

bash
Copy
Edit
%APPDATA%\Claude\claude_desktop_config.json
Use this format:

json
Copy
Edit
{
  "mcpServers": {
    "educhain-server": {
      "command": "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Python\\Python310\\python.exe",
      "args": ["mcp_server.py"],
      "workingDirectory": "C:\\Users\\YourUsername\\Desktop\\mcp-educhain-server",
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
🧪 Test Your Server
In terminal:

bash
Copy
Edit
cd mcp-educhain-server
python mcp_server.py
Check with:

bash
Copy
Edit
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python mcp_server.py
🧠 Example Prompts in Claude
"Generate 5 MCQs on Photosynthesis"

"Create a lesson plan for Algebra"

"Make flashcards for World War 2"

🐛 Troubleshooting
✅ Use absolute paths in the config

✅ Add PYTHONIOENCODING=utf-8

✅ Print debug logs to stderr

Check Claude logs via “Open Logs Folder”

📜 License
MIT License

✨ Credits
Educhain

Ollama

Claude Desktop
