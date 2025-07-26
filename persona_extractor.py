import fitz  # PyMuPDF
import os
import json
import time
from datetime import datetime

# ----- Persona & Task (customize this for each test case) -----
persona = "PhD Researcher in Computational Biology"
job_to_be_done = "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
keywords = [
    "graph neural networks", "gnn", "drug discovery", 
    "methodologies", "datasets", "performance", "benchmark", 
    "experiment", "evaluation", "architecture", "framework"
]

# ----- Thresholds -----
DOCUMENT_KEYWORD_THRESHOLD = 5  # If fewer than this, skip the doc

# ----- Input/Output Folders -----
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# ----- Helper Function -----
def rank_section(text):
    score = 0
    lowered = text.lower()
    for kw in keywords:
        if kw in lowered:
            score += 1
    if score >= 3:
        return 1
    elif score == 2:
        return 2
    elif score == 1:
        return 3
    else:
        return None  # Completely irrelevant

# ----- Main Function -----
def process_documents():
    result = {
        "metadata": {
            "input_documents": [],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for filename in os.listdir(INPUT_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        filepath = os.path.join(INPUT_DIR, filename)
        doc = fitz.open(filepath)

        # Count global keyword hits
        total_hits = 0
        for page in doc:
            text = page.get_text()
            for kw in keywords:
                total_hits += text.lower().count(kw)

        if total_hits < DOCUMENT_KEYWORD_THRESHOLD:
            print(f"⛔ Skipping '{filename}' due to low relevance (only {total_hits} hits)")
            continue

        print(f"✅ Processing '{filename}' with {total_hits} keyword hits")
        result["metadata"]["input_documents"].append(filename)

        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                text = " ".join(
                    span["text"]
                    for line in block["lines"]
                    for span in line["spans"]
                    if span["text"].strip()
                ).strip()
                if len(text) < 10:
                    continue
                importance = rank_section(text)
                if importance is None:
                    continue  # skip irrelevant lines
                section_entry = {
                    "document": filename,
                    "page_number": page_num,
                    "section_title": text,
                    "importance_rank": importance
                }
                result["extracted_sections"].append(section_entry)
                if importance == 1:
                    result["subsection_analysis"].append({
                        "document": filename,
                        "refined_text": text,
                        "page_number": page_num
                    })

        doc.close()

    # Write result to JSON
    output_path = os.path.join(OUTPUT_DIR, "persona_summary.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Output saved to {output_path}")

# ----- Run -----
if __name__ == "__main__":
    start = time.time()
    process_documents()
    print(f"\n⏱️ Completed in {round(time.time() - start, 2)}s")
