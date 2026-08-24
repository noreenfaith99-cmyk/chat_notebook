import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from collections import deque

# Page config
st.set_page_config(
    page_title="SuperAI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.2em;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 1em;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        text-align: left;
        margin-right: 20%;
    }
    .support-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #ffc107;
    }
    .stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .stat-box {
        text-align: center;
        padding: 20px;
        background-color: #f0f0f0;
        border-radius: 10px;
        flex: 1;
        margin: 0 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = deque(maxlen=20)
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
if "pipe" not in st.session_state:
    st.session_state.pipe = None
if "tokenizer" not in st.session_state:
    st.session_state.tokenizer = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    st.markdown("---")
    st.subheader("Model Configuration")
    
    model_choice = st.radio(
        "Select Model:",
        ["Mistral 7B (Recommended)", "Llama 2 7B"],
        help="Mistral is faster, Llama 2 is more knowledgeable"
    )
    
    model_map = {
        "Mistral 7B (Recommended)": "mistralai/Mistral-7B-Instruct-v0.2",
        "Llama 2 7B": "meta-llama/Llama-2-7b-chat-hf"
    }
    
    max_tokens = st.slider("Response Length", 100, 1024, 512)
    temperature = st.slider("Creativity (0=Focused, 1=Random)", 0.0, 1.0, 0.7)
    top_p = st.slider("Diversity", 0.0, 1.0, 0.95)
    
    st.markdown("---")
    st.subheader("💾 Conversation")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages.clear()
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        memory_size = len(st.session_state.messages)
        st.metric("Messages", memory_size)
    
    st.markdown("---")
    st.subheader("📊 Info")
    st.info(f"""
    **Device:** {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}
    
    **VRAM:** {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB (if GPU)
    """)

# Main content
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("<h1 class='main-title'>🤖 SuperAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Advanced AI Chat - Powered by Local LLMs</p>", unsafe_allow_html=True)

st.markdown("---")

# Load model
@st.cache_resource
def load_model(model_name):
    with st.spinner("🔄 Loading model... (1-2 minutes)"):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                load_in_8bit=True
            )
            
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device_map="auto"
            )
            
            return pipe, tokenizer
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None, None

# Load model if not loaded
if not st.session_state.model_loaded:
    pipe, tokenizer = load_model(model_map[model_choice])
    if pipe and tokenizer:
        st.session_state.pipe = pipe
        st.session_state.tokenizer = tokenizer
        st.session_state.model_loaded = True
        st.success("✅ Model loaded successfully!")
    else:
        st.error("❌ Failed to load model. Check your GPU/VRAM.")

# Chat interface
if st.session_state.model_loaded and st.session_state.pipe:
    
    # Display chat history
    st.subheader("💬 Chat")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class='chat-message user-message'>
                    <b>You:</b> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-message assistant-message'>
                    <b>SuperAI:</b> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Type your message:",
            placeholder="Ask me anything...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    # Process message
    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            try:
                # Build context
                context = "\n".join([
                    f"{msg['role'].capitalize()}: {msg['content']}"
                    for msg in st.session_state.messages
                ])
                
                system_prompt = """You are SuperAI, an advanced conversational AI assistant. 
You are helpful, harmless, and honest. Provide detailed, thoughtful responses.
Keep responses concise but informative."""
                
                prompt = f"{system_prompt}\n\n{context}\nAssistant:"
                
                # Generate
                output = st.session_state.pipe(
                    prompt,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    return_full_text=False
                )
                
                response = output[0]["generated_text"].strip()
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
    
    # Support section
    st.markdown("---")
    st.markdown("""
    <div class='support-box'>
        <h3>❤️ Love SuperAI? Support the Project!</h3>
        <p>If you find SuperAI helpful, please consider supporting its development:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <a href="https://patreon.com" target="_blank">
            <button style="width: 100%; padding: 10px; background-color: #ff424d; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                💖 Support on Patreon
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <a href="https://ko-fi.com" target="_blank">
            <button style="width: 100%; padding: 10px; background-color: #13C3FF; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                ☕ Buy Me Coffee
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <a href="https://github.com/noreenfaith99-cmyk/chat_notebook" target="_blank">
            <button style="width: 100%; padding: 10px; background-color: #333; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                ⭐ Star on GitHub
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ---
    <p style="text-align: center; color: #666; font-size: 0.9em;">
    SuperAI © 2024 | Your support helps improve this project ❤️
    </p>
    """, unsafe_allow_html=True)

else:
    st.warning("⏳ Loading model... Please wait. This may take 1-2 minutes on first run.")
