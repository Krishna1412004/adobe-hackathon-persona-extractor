import os
import fitz  # PyMuPDF
import json
import datetime

# Load persona info
with open("persona.json", "r") as f:
    persona_info = json.load(f)

persona = persona_info["persona"]
job = persona_info["job_to_be_done"]

input_dir = "input"
output_dir = "output"

summary = {
    "metadata": {
        "input_documents": [],
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": str(datetime.datetime.now())
    },
    "extracted_sections": [],
    "subsection_analysis": []
}

keywords = job.lower().split()

def is_relevant(text):
    return any(keyword in text.lower() for keyword in keywords)

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        summary["metadata"]["input_documents"].append(filename)
        doc = fitz.open(os.path.join(input_dir, filename))

        for page_num, page in enumerate(doc, 1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    text = ""
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text += span["text"] + " "
                    text = text.strip()
                    if is_relevant(text):
                        summary["extracted_sections"].append({
                            "document": filename,
                            "page_number": page_num,
                            "section_title": text[:100],  # take first 100 chars
                            "importance_rank": 1  # basic, could improve later
                        })
                        summary["subsection_analysis"].append({
                            "document": filename,
                            "page_number": page_num,
                            "refined_text": text
                        })

# Save output
with open(os.path.join(output_dir, "summary_output.json"), "w") as f:
    json.dump(summary, f, indent=2)
