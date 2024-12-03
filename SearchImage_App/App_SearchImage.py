import os
import faiss
import numpy as np
import streamlit as st
from glob import glob
from PIL import Image
from sentence_transformers import SentenceTransformer

class ImageSearchApp:
    def __init__(self, model_name='clip-ViT-B-32'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.image_files = []

    def create_embeddings(self, image_path, chunk_size=256):
        """Create embeddings for images in the specified path"""
        self.image_files = glob(os.path.join(image_path, "*.jpg"))
        embeddings = []

        for i in range(0, len(self.image_files), chunk_size):
            chunk = self.image_files[i: i + chunk_size]
            images = [Image.open(image_file) for image_file in chunk]
            chunk_embeddings = self.model.encode(images)
            embeddings.extend(chunk_embeddings)

        return np.array(embeddings)

    def build_faiss_index(self, embeddings):
        """Build FAISS index with embeddings"""
        dimension = len(embeddings[0])
        index = faiss.IndexFlatIP(dimension)
        index = faiss.IndexIDMap(index)

        vectors = embeddings.astype("float32")
        index.add_with_ids(vectors, np.array(range(len(embeddings))))
        
        self.index = index
        return index

    def save_index(self, index_path="index.faiss", image_files_path="image_files.txt"):
        """Save FAISS index and image file paths"""
        faiss.write_index(self.index, index_path)
        
        with open(image_files_path, "w") as f:
            for image_file in self.image_files:
                f.write(image_file + "\n")

    def search_image(self, query, top_k=5):
        """Search images based on query (text or image path)"""
        if query.endswith(".jpg"):
            query = Image.open(query)

        query_embedding = self.model.encode(query)
        query_embedding = query_embedding.astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_embedding, top_k)
        retrieved_image_files = [self.image_files[i] for i in indices[0]]

        return query, retrieved_image_files

def main():
    st.title("🖼️ Flickr30k Image Search")
    
    # Initialize image search app
    if 'app' not in st.session_state:
        st.session_state.app = ImageSearchApp()
    
    # Image folder selection
    image_folder = st.text_input("Enter Flickr30k images folder path:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Process Images"):
            if os.path.isdir(image_folder):
                # Create embeddings
                embeddings = st.session_state.app.create_embeddings(image_folder)
                
                # Build FAISS index
                st.session_state.app.build_faiss_index(embeddings)
                
                # Save index and image files
                st.session_state.app.save_index()
                
                st.success(f"Processed {len(st.session_state.app.image_files)} images")
            else:
                st.error("Invalid folder path")
    
    with col2:
        # Search input
        query = st.text_input("Enter image description or path:")
        
        if st.button("Search Images"):
            if query:
                try:
                    results = st.session_state.app.search_image(query)
                    
                    # Display results
                    result_cols = st.columns(len(results[1]))
                    for i, img_path in enumerate(results[1]):
                        with result_cols[i]:
                            st.image(img_path, use_column_width=True)
                            st.write(os.path.basename(img_path))
                except Exception as e:
                    st.error(f"Search error: {e}")

if __name__ == "__main__":
    main()