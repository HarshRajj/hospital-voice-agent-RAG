

import os
import hashlib
import json
from pathlib import Path
from typing import List, Optional, Dict
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.schema import TextNode
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core import SimpleDirectoryReader

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import MilvusClient

# Global embedding model instance for reuse
_embed_model = None

def get_embedding_model():
    """Get or create a singleton embedding model instance"""
    global _embed_model
    if _embed_model is None:
        _embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    return _embed_model

def get_content_hash(text: str) -> str:
    """Generate a hash for content-based caching"""
    return hashlib.md5(text.encode()).hexdigest()

class EmbeddingCache:
    """Simple file-based embedding cache"""
    
    def __init__(self, cache_dir: Path = Path("storage/embedding_cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "embeddings.json"
        self._cache = self._load_cache()
    
    def _load_cache(self) -> Dict[str, List[float]]:
        """Load cache from disk"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self._cache, f)
    
    def get(self, content_hash: str) -> Optional[List[float]]:
        """Get embedding from cache"""
        return self._cache.get(content_hash)
    
    def set(self, content_hash: str, embedding: List[float]):
        """Store embedding in cache"""
        self._cache[content_hash] = embedding
        self._save_cache()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def generate_embeddings_batch(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    """
    Generate embeddings in batches for improved efficiency
    
    Args:
        texts: List of text strings to embed
        batch_size: Number of texts to process in each batch
    
    Returns:
        List of embeddings corresponding to input texts
    """
    embed_model = get_embedding_model()
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        try:
            # Use OpenAI's batch embedding endpoint
            batch_embeddings = embed_model.get_text_embedding_batch(batch_texts)
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"Batch embedding failed for batch {i//batch_size + 1}: {str(e)}")
            # Fallback to individual processing for this batch
            for text in batch_texts:
                try:
                    embedding = embed_model.get_text_embedding(text)
                    all_embeddings.append(embedding)
                except Exception as individual_e:
                    print(f"Individual embedding failed: {str(individual_e)}")
                    all_embeddings.append(None)
    
    return all_embeddings

def generate_embeddings_with_cache(documents: List[Document], cache: EmbeddingCache) -> List[TextNode]:
    """
    Generate embeddings with caching support
    
    Args:
        documents: List of documents to process
        cache: Embedding cache instance
    
    Returns:
        List of TextNode objects with embeddings
    """
    nodes = []
    uncached_docs = []
    cached_nodes = []
    
    # First pass: check cache
    for doc in documents:
        content_hash = get_content_hash(doc.text)
        cached_embedding = cache.get(content_hash)
        
        if cached_embedding is not None:
            # Use cached embedding
            node = TextNode(text=doc.text, id_=doc.id_, embedding=cached_embedding)
            cached_nodes.append(node)
        else:
            # Need to generate embedding
            uncached_docs.append((doc, content_hash))
    
    print(f"Found {len(cached_nodes)} cached embeddings, generating {len(uncached_docs)} new embeddings")
    
    # Second pass: generate embeddings for uncached documents
    if uncached_docs:
        texts = [doc.text for doc, _ in uncached_docs]
        embeddings = generate_embeddings_batch(texts, batch_size=50)  # Smaller batch for stability
        
        for (doc, content_hash), embedding in zip(uncached_docs, embeddings):
            if embedding is not None and len(embedding) == 1536:
                # Cache the new embedding
                cache.set(content_hash, embedding)
                node = TextNode(text=doc.text, id_=doc.id_, embedding=embedding)
                nodes.append(node)
            else:
                print(f"Warning: Failed to generate valid embedding for document {doc.id_}")
    
    # Combine cached and new nodes
    all_nodes = cached_nodes + nodes
    print(f"Total valid nodes: {len(all_nodes)}")
    
    return all_nodes

def create_and_upload_index(persist_dir: Path, data_dir: Path):
    """
    Optimized version of create_and_upload_index with improved embedding efficiency
    """
    # Load environment variables
    zilliz_uri = os.getenv("ZILLIZ_CLUSTER_ENDPOINT")
    zilliz_api_key = os.getenv("ZILLIZ_API_KEY")
    
    if not zilliz_uri or not zilliz_api_key:
        raise ValueError("ZILLIZ_CLUSTER_ENDPOINT and ZILLIZ_API_KEY must be set in environment variables")
    
    # Initialize embedding cache
    cache = EmbeddingCache()
    
    # Load documents
    print("Loading documents...")
    documents = []
    for file_path in data_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.pdf']:
            try:
                if file_path.suffix.lower() == '.pdf':
                    from llama_index.readers.file import PDFReader
                    reader = PDFReader()
                    docs = reader.load_data(file_path)
                    documents.extend(docs)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        doc = Document(text=content, id_=str(file_path))
                        documents.append(doc)
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
    
    if not documents:
        raise ValueError("No documents found in the data directory")
    
    print(f"Loaded {len(documents)} documents")
    
    # Clean documents
    cleaned_documents = [doc for doc in documents if doc.text and doc.text.strip()]
    print(f"After cleaning: {len(cleaned_documents)} documents")
    
    # Generate embeddings with caching
    print("Generating embeddings with caching...")
    nodes = generate_embeddings_with_cache(cleaned_documents, cache)
    
    if not nodes:
        raise ValueError("No documents with valid embeddings.")
    
    # Create local storage context (fixed: removed incorrect vector_store arg)
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore(),
        index_store=SimpleIndexStore(),
    )
    
    # Create and persist local index (use from_nodes if available)
    print("Creating local index...")
    try:
        index = VectorStoreIndex.from_nodes(nodes, storage_context=storage_context)
    except AttributeError:
        index = VectorStoreIndex(nodes, storage_context=storage_context)
    storage_context.persist(persist_dir=persist_dir)
    print(f"Index saved locally to {persist_dir}")
    
    # Upload to Zilliz Cloud
    collection_name = "hospital_knowledge_base"
    milvus_client = MilvusClient(uri=zilliz_uri, token=zilliz_api_key)
    print(f"Connected to Zilliz Cloud: {zilliz_uri}")
    
    if milvus_client.has_collection(collection_name):
        milvus_client.drop_collection(collection_name)
        print(f"Dropped existing collection: {collection_name}")
    
    vector_store = MilvusVectorStore(
        uri=zilliz_uri,
        token=zilliz_api_key,
        collection_name=collection_name,
        dim=1536,
        overwrite=True
    )
    
    print(f"Uploading {len(nodes)} nodes to Zilliz Cloud...")
    vector_store.add(nodes)
    
    milvus_client.flush(collection_name)
    entity_count = milvus_client.get_collection_stats(collection_name)["row_count"]
    print(f"Total entities in collection {collection_name}: {entity_count}")
    
    if entity_count == 0:
        raise ValueError("Upload failed: No entities stored.")
    
    print("✅ Optimized embedding generation completed successfully!")

if __name__ == "__main__":
    persist_dir = Path("storage/vector_storage")
    data_dir = Path("data/knowledge_base")
    create_and_upload_index(persist_dir, data_dir)
