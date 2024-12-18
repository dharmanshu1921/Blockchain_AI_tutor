# AI Blockchain Tutor 🧠🔗

## Overview

The AI Blockchain Tutor is an innovative web application designed to simplify blockchain education through advanced AI technologies. Using Retrieval-Augmented Generation (RAG) and a multi-agent system, this tool provides personalized, dynamic, and contextually accurate blockchain learning experiences.

## Key Features

- 🤖 Multi-Agent AI System
- 📚 Comprehensive Knowledge Retrieval
- 🎙️ Multiple Input Methods (Text, Audio, Image)
- 🔍 Semantic Search Capabilities
- 📝 Interactive Learning Experiences

## Technology Stack

- **Language Model**: Groq (Llama3) & Gemini 1.5 pro
- **Embedding Model**: Cohere
- **Agent Framework**: CrewAI
- **Web Interface**: Streamlit
- **Search Tools**: TXTSearchTool, PDFSearchTool
- **Speech Recognition**: SpeechRecognition

## Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/ai-blockchain-tutor.git
cd ai-blockchain-tutor
```

2. Creating python env & installing dependencies
```bash
python -m venv tutor
source tutor/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables
- Create a `.env` file with:
  - `GROQ_API_KEY`
  - `COHERE_API_KEY`
  - `SERPER_API_KEY`
  - `GOOGLE_API_KEY`

4. Add Groq API key to ImageAnalyzer.py

5. go to cd blockchain_tutor/src and `python -m streamlit run streamlit_app.py`

## Input Methods

1. **Text Input**: Type blockchain-related questions directly
2. **Audio Input**: Speak your blockchain queries
3. **Image Input**: Upload images for analysis

## Agents

The system includes specialized agents:
- Knowledge Retrieval Agent
- Query Responder Agent
- Summarizer Agent
- Blockchain AI Tutor Agent
