from app.services.rag_sys.vector_store.base_processor import BaseDocProcessor

class PDFProcessor(BaseDocProcessor):
    async def load_doc(self, file, meta_data):
        return ["example pdf content"], meta_data

    def process_doc(self, texts, meta_data):
        print("Processing PDF specific logic...")
        return [doc.strip().lower() for doc in texts], meta_data

    def chunk_docs(self, texts, meta_data):
        print("Chunking PDF into 500-token blocks...")
        chunks = []
        chunk_metadatas = []
        for i, text in enumerate(texts):
            chunks.append(text)
            chunk_metadatas.append({"source": meta_data.source or "", "chunk_index": i})
        return chunks, chunk_metadatas

class MarkdownProcessor(BaseDocProcessor):
    async def load_doc(self, file, meta_data):
        return ["example md content"], meta_data

    def process_doc(self, texts, meta_data):
        print("Removing Markdown headers and links...")
        return texts, meta_data

    def chunk_docs(self, texts, meta_data):
        print("Chunking Markdown by Headers...")
        chunks = []
        chunk_metadatas = []
        for i, text in enumerate(texts):
            chunks.append(text)
            chunk_metadatas.append({"source": meta_data.source or "", "chunk_index": i})
        return chunks, chunk_metadatas