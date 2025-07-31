# Voice Agent

## Overview
This project is an AI-driven conversational voice assistant built using LiveKit Agents and LLaMA Index. It leverages Retrieval-Augmented Generation (RAG) with a vector database to provide context-aware responses, optimized for efficient voice interactions. The assistant selectively retrieves document context based on trigger words, ensuring fast responses for simple queries.

Key features:
- **Selective RAG Retrieval**: Uses trigger words to determine when to retrieve document context.
- **Customizable Trigger Words**: Easily adjust which queries trigger RAG retrieval.
- **Scalable Knowledge Base**: Integrates with a vector database for document retrieval.

## Prerequisites
- Python 3.8+
- A vector database account (e.g., Zilliz Cloud, Milvus)
- OpenAI API key for LLM (GPT-4o)
- LiveKit Agents for voice interaction
- LLaMA Index for RAG integration

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/voice-agent.git
   cd voice-agent
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
   Example `requirements.txt`:
   ```
   livekit-agents
   llama-index
   openai
   ```

4. **Set Environment Variables**:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key
   VECTOR_DB_API_KEY=your-vector-db-api-key
   ```

5. **Prepare Instructions File**:
   Ensure a `config/instructions.txt` file exists with the system prompt for the assistant.

## Usage
1. **Run the Application**:
   ```bash
   python voice_server.py
   ```
   This starts the LiveKit Agents worker, initializes the vector database index, and begins listening for voice inputs.

2. **Interact with the Assistant**:
   - Use a voice client compatible with LiveKit to interact with the assistant.
   - Example queries:
     - "What is the vision of the company?"
     - "Who is the founder?"
     - "Hi, my name is Arjun." (RAG skipped for simple queries)

3. **Monitor Logs**:
   Logs will display RAG decisions (performed or skipped) and retrieved context for debugging.

## Project Structure
## Project Structure
```
coaching_rag_agent/
├── src/
│   ├── agents/
│   │   └── voice_agent.py          # Core voice agent logic with selective RAG retrieval
│   ├── core/
│   │   ├── config.py               # Configuration and project paths
│   │   └── indexing.py             # Index management and vector store operations
│   ├── vector_store/
│   │   ├── upload_documents.py     # Document upload to vector store
│   │   └── test_retrieval.py       # Test vector store retrieval
│   └── utils/
│       └── cloud_utils.py          # Cloud connection utilities
├── data/
│   └── knowledge_base/             # PDF documents for RAG
├── storage/
│   └── vector_storage/             # Local vector store persistence
├── config/
│   └── instructions.txt            # System prompt for the assistant
├── tests/                          # Test files
├── voice_server.py                 # Entry point for starting the LiveKit voice server
└── requirements.txt                # Python dependencies
```

## Customization
## Customization
- **Trigger Words**: Modify the `TRIGGER_WORDS` list in `src/agents/voice_agent.py` to control which queries trigger RAG retrieval. Example:
  ```python
  TRIGGER_WORDS = [
      "who", "what", "where", "when", "why", "how",
      "tell me", "explain", "describe", "give me",
      "information about", "details on", "facts about",
      "use case", "vision", "founder", "contact number",
  ]
  ```
- **RAG Parameters**: Adjust `similarity_top_k` in the `as_retriever()` call to balance retrieval speed and accuracy.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.