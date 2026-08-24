# 🤖 SuperAI Chat - Advanced Conversational AI

A powerful, locally-running AI chatbot powered by Mistral 7B or Llama 2, with conversation memory, tool integration, and GPU optimization.

## ✨ Features

- **Large Language Models**: Uses Mistral 7B or Llama 2 (way smarter than GPT-2)
- **Conversation Memory**: Maintains context across messages for natural conversations
- **Tool Integration**: Can calculate math, get time, and more
- **GPU Optimized**: 8-bit quantization + float16 precision for fast inference
- **Interactive Commands**: `/memory`, `/clear`, `/tools`, `/help`, `/exit`
- **Fully Local**: Runs entirely on your machine (no API calls needed)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- GPU with at least 8GB VRAM (or CPU for slower inference)
- ~13GB disk space for Mistral 7B model

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/noreenfaith99-cmyk/chat_notebook.git
   cd chat_notebook
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the notebook**
   - Open `chat_notebook.ipynb` in Jupyter Notebook or JupyterLab
   - Run each cell in order
   - Wait for models to load (~1-2 minutes on GPU)
   - Start chatting when you see "SuperAI Chat Ready!"

## 📖 Usage

### Basic Chat
```
You: Hello! What can you do?
Assistant: I'm SuperAI, an advanced conversational AI assistant...
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/memory` | Display conversation history |
| `/clear` | Clear conversation memory |
| `/tools` | List available tools |
| `/exit` | Exit the chat |

### Tool Usage

SuperAI can use tools inline:

- **Math Calculation**: Ask "What's 25 * 4?" → Uses [calculate: 25*4]
- **Get Time**: Ask "What time is it?" → Uses [time]
- **Available Tools**: Type `/tools` to see all options

## 🔧 Configuration

Edit these variables in the notebook to customize:

```python
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"  # Or "meta-llama/Llama-2-7b-chat-hf"
MAX_MEMORY = 10              # Conversation history length
MAX_NEW_TOKENS = 512         # Response length
TEMPERATURE = 0.7            # Creativity (0=deterministic, 1=random)
TOP_P = 0.95                 # Diversity
```

## 💡 Advanced Features

### Conversation Memory
SuperAI remembers the last 10 messages automatically, allowing for coherent multi-turn conversations.

### Tool System
Easily extend with new tools:

```python
@staticmethod
def custom_tool(input_data):
    # Your code here
    return result
```

## 🎯 Next Steps

Potential enhancements:
- [ ] Web search integration
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] File reading and analysis
- [ ] Multi-turn reasoning
- [ ] Fine-tuning on custom data
- [ ] REST API deployment
- [ ] Discord bot integration

## 📊 Performance

**GPU (RTX 3060+)**
- Load time: ~1-2 minutes
- Response time: ~5-15 seconds
- Memory usage: ~8-10GB

**GPU (RTX 4090)**
- Load time: ~30 seconds
- Response time: ~2-5 seconds
- Memory usage: ~8-10GB

**CPU (not recommended)**
- Load time: ~5-10 minutes
- Response time: ~1-5 minutes per message
- Memory usage: ~16GB+

## 🔐 Safety & Privacy

- All processing happens locally on your machine
- No data is sent to external servers
- No telemetry or logging
- Complete privacy guaranteed

## 📚 Model Options

### Mistral 7B (Default)
- **Pros**: Fast, smart, good at reasoning
- **Cons**: Slightly smaller knowledge base
- **Best for**: General conversations, quick responses

### Llama 2 7B
- **Pros**: Wide knowledge, good instruction following
- **Cons**: Slightly slower than Mistral
- **Best for**: Detailed explanations, creative tasks

Switch models by changing `MODEL_NAME` in the notebook.

## 🐛 Troubleshooting

**Error: Out of Memory**
- Reduce `MAX_MEMORY` from 10 to 5
- Use `load_in_8bit=True` (already enabled)
- Reduce `MAX_NEW_TOKENS`

**Error: Model not found**
- Ensure internet connection for first download
- Check HuggingFace authentication if needed

**Slow responses**
- Make sure GPU is being used (check with `nvidia-smi`)
- Reduce `MAX_NEW_TOKENS`
- Check for background processes

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit PRs for:
- New tools
- Performance improvements
- Bug fixes
- Documentation improvements

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Open a GitHub issue
3. Include your setup details (GPU, Python version, etc.)

---

**Happy chatting with SuperAI! 🚀**
