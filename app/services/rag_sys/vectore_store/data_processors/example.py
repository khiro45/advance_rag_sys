from app.services.rag_sys.vectore_store.data_processing import BaseDocProcessor
class PDFProcessor(BaseDocProcessor):
    def process_docs(self, docs, meta_data):
        print("Processing PDF specific logic...")
        return [doc.strip().lower() for doc in docs]

    def chunk_docs(self, docs, meta_data):
        print("Chunking PDF into 500-token blocks...")
        return docs # logic here

class MarkdownProcessor(BaseDocProcessor):
    def process_docs(self, docs, meta_data):
        print("Removing Markdown headers and links...")
        return docs 

    def chunk_docs(self, docs, meta_data):
        print("Chunking Markdown by Headers...")
        return docs