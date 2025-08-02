# Hospital Voice Agent 🏥🤖

## Overview 🌟
This project is an AI-driven conversational voice assistant specifically designed for hospital reception and patient assistance. Built using LiveKit Agents and LlamaIndex, it leverages Retrieval-Augmented Generation (RAG) with Zilliz Cloud vector database to provide context-aware responses for medical inquiries, appointment scheduling, and hospital information.

The assistant is optimized for healthcare environments with selective RAG retrieval based on medical trigger words, ensuring fast responses for simple queries while providing detailed information when needed.

Key features:
- **Healthcare-Specific Voice Assistant**: Tailored responses for hospital reception tasks
- **Selective RAG Retrieval**: Uses medical trigger words to determine when to retrieve document context
- **Optimized Embedding Generation**: Advanced caching system to avoid regenerating embeddings
- **ElevenLabs Voice Synthesis**: High-quality, multilingual voice responses
- **Deepgram Speech Recognition**: Accurate speech-to-text with multilingual support
- **Scalable Knowledge Base**: Integrates with Zilliz Cloud for medical document retrieval

## About the Creator 👨‍💻
Hi, I'm a developer passionate about building intelligent healthcare systems that improve patient experience and hospital efficiency. This project integrates cutting-edge AI technologies specifically for medical environments:
- **LlamaIndex** for efficient medical document indexing and retrieval
- **LiveKit Agents** for seamless voice interaction in healthcare settings
- **OpenAI GPT-4o** for medical query understanding and generation
- **Zilliz Cloud** for scalable vector storage of medical knowledge
- **ElevenLabs TTS** for natural voice synthesis
- **Deepgram STT** for accurate speech recognition

Feel free to reach out for collaboration on healthcare AI projects! 🌐

## Prerequisites 📋
- Python 3.8+
- Zilliz Cloud account for vector database storage
- OpenAI API key for GPT-4o language model
- ElevenLabs API key for voice synthesis
- Deepgram API key for speech recognition
- LiveKit Agents for voice interaction framework
- LlamaIndex for RAG integration

## Installation 🛠️
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HarshRajj/hospital.git
   cd hospital
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ZILLIZ_CLUSTER_ENDPOINT=your-zilliz-cluster-endpoint
   ZILLIZ_API_KEY=your-zilliz-api-key
   ELEVENLABS_API_KEY=your-elevenlabs-api-key
   DEEPGRAM_API_KEY=your-deepgram-api-key
   ```

5. **Prepare Hospital Knowledge Base**:
   - Place medical documents and hospital information in `data/knowledge_base/`
   - Ensure `config/prompt.txt` contains the hospital-specific system prompt
   - Run the document upload script to generate embeddings:
   ```bash
   python src/vector_store/upload_documents.py
   ```

## Usage 🎙️
1. **Start the Hospital Voice Agent**:
   ```bash
   python voice_server.py console
   ```
   This initializes the LiveKit Agents worker, loads the medical knowledge base, and begins listening for voice inputs.

2. **Interact with the Hospital Assistant**:
   - Use a voice client compatible with LiveKit to interact with the assistant
   - Example medical queries:
     - "I need to schedule an appointment with Dr. Smith"
     - "What are your visiting hours?"
     - "Where is the emergency department?"
     - "Do you accept my insurance?"
     - "What services do you offer?"

3. **Monitor System Logs**:
   Logs display RAG decisions, medical query processing, and retrieved context for debugging and optimization.

## Project Structure 🗂️
```
hospital/
├── src/
│   ├── agents/
│   │   └── voice_agent.py          # Hospital voice agent with medical trigger words
│   ├── core/
│   │   ├── config.py               # Configuration and project paths
│   │   └── indexing.py             # Medical document indexing and vector operations
│   ├── vector_store/
│   │   ├── upload_documents.py     # Optimized document upload with embedding cache
│   │   ├── upload_documents_optimized.py  # Enhanced version with batch processing
│   │   └── test_retrieval.py       # Test medical document retrieval
│   └── utils/
│       └── cloud_utils.py          # Zilliz Cloud connection utilities
├── data/
│   └── knowledge_base/             # Medical documents and hospital information
├── storage/
│   ├── vector_storage/             # Local vector store persistence
│   └── embedding_cache/            # Cached embeddings for efficiency
├── config/
│   └── prompt.txt                  # Hospital-specific system prompt
├── tests/                          # Test files for medical scenarios
├── voice_server.py                 # Entry point for hospital voice server
├── requirements.txt                # Python dependencies (123 packages)
└── .env                           # Environment variables (API keys)
```

## Key Features ⭐

### 🧠 **Intelligent Embedding Caching**
- **Content-based hashing**: Avoids regenerating embeddings for existing content
- **Persistent cache**: Embeddings stored in `storage/embedding_cache/embeddings.json`
- **Batch processing**: Optimized API calls for multiple documents
- **Performance**: 5-10x faster processing for large knowledge bases

### 🏥 **Medical-Specific Trigger Words**
The system uses healthcare-specific trigger words to determine when to retrieve medical context:
```python
TRIGGER_WORDS = [
    "appointment", "doctor", "physician", "nurse",
    "emergency", "urgent", "pain", "symptoms",
    "insurance", "billing", "payment", "cost",
    "visiting hours", "location", "department",
    "services", "treatment", "medication", "prescription",
    "specialist", "surgery", "lab results", "test"
]
```

### 🎙️ **Advanced Voice Processing**
- **ElevenLabs TTS**: Voice ID "Xb7hH8MSUJpSbSDYk0k2" for natural hospital reception voice
- **Deepgram STT**: "nova-3" model with multilingual support for diverse patient base
- **Silero VAD**: Voice activity detection for seamless conversation flow

## Customization ✨
- **Medical Trigger Words**: Modify `TRIGGER_WORDS` in `src/agents/voice_agent.py` for specific medical domains
- **Voice Configuration**: Update voice ID in `voice_server.py` for different voice characteristics
- **Knowledge Base**: Add hospital-specific documents to `data/knowledge_base/`
- **System Prompt**: Customize hospital greeting and behavior in `config/prompt.txt`
- **RAG Parameters**: Adjust `similarity_top_k` for medical query precision vs. speed balance

## Performance Optimizations 🚀
1. **Embedding Cache**: Automatic caching prevents redundant API calls
2. **Batch Processing**: Processes multiple documents efficiently
3. **Selective RAG**: Only retrieves context for medical queries
4. **Content Hashing**: MD5-based deduplication of document content
5. **Retry Logic**: Robust error handling for API failures

## Contributing 🤝
Contributions to improve healthcare AI are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/medical-improvement`)
3. Make your changes and commit (`git commit -m "Add medical feature"`)
4. Push to your branch (`git push origin feature/medical-improvement`)
5. Open a pull request

## License 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Healthcare Compliance Note ⚖️
This system is designed for general hospital information and appointment assistance. For clinical decision support or patient diagnosis, ensure compliance with healthcare regulations (HIPAA, FDA, etc.) and involve qualified medical professionals.