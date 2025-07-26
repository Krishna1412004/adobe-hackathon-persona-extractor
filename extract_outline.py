import fitz  # PyMuPDF
import json
import os

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    font_sizes = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]
                        if len(text) > 5:
                            font_sizes.append(size)

    top_sizes = sorted(list(set(font_sizes)), reverse=True)[:3]
    size_to_level = {}
    if len(top_sizes) > 0:
        size_to_level[top_sizes[0]] = "Title"
    if len(top_sizes) > 1:
        size_to_level[top_sizes[1]] = "H1"
    if len(top_sizes) > 2:
        size_to_level[top_sizes[2]] = "H2"

    for s in set(font_sizes):
        if s not in size_to_level and s < top_sizes[-1]:
            size_to_level[s] = "H3"

    outline = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]
                        level = size_to_level.get(size, None)
                        if level:
                            if level == "Title" and not title:
                                title = text
                            elif level in {"H1", "H2", "H3"}:
                                outline.append({
                                    "level": level,
                                    "text": text,
                                    "page": page_num + 1
                                })

    return {
        "title": title,
        "outline": outline
    }

def process_all_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            result = extract_outline_from_pdf(pdf_path)

            json_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(json_path, "w") as f:
                json.dump(result, f, indent=2)

            print(f"Processed: {filename}")

if __name__ == "__main__":
    process_all_pdfs("/app/input", "/app/output")
