from handler_pack import json_file_handler, image_generation_handler, doc_generation_handler

# ---------------------
# CONFIG
# ---------------------

BRD_FILE = "business_requirements.txt"
CHUNK_SIZE = 2000  # words per chunk

def load_brd(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def split_document(text, max_words=CHUNK_SIZE):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def main():
    global actor, svc, inter, architecture, graphviz_path

    # ---------------------
    # STEP 1: Load and Chunk BRD
    # ---------------------
    brd_text = load_brd(BRD_FILE)
    chunks = split_document(brd_text)
    print(f"✅ BRD loaded. Total chunks: {len(chunks)}")
    # brd_text = load_brd("business_requirements.pdf")

    # ---------------------
    # STEP 2: Extract JSON from each chunk
    # ---------------------
    architecture = json_file_handler.create_json_file_from_brd(chunks)

    # ---------------------
    # STEP 3: Generate C4 Container Diagram
    # ---------------------
    image_generation_handler.generate_architecture_png(architecture, output_file="c4_ai_full")

    # ---------------------
    # STEP 4: Generate Design Document
    # ---------------------
    doc_generation_handler.generate_design_doc(architecture)


if __name__ == "__main__":
   
    main()




