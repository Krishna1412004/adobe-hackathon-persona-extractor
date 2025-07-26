# Approach Explanation – Round 1B: Persona-Driven Document Intelligence

## 🧠 Problem Understanding

We were given a set of diverse documents, a defined persona, and a specific job-to-be-done. The goal was to extract and rank **only the most relevant content** from these documents for that persona and task.

## 🔍 Core Approach

We developed a lightweight, rule-based PDF parser using PyMuPDF. The pipeline:

1. **PDF Parsing**: Extracted all text blocks using `fitz` (PyMuPDF).
2. **Relevance Scoring**:
   - Matched keywords from the **persona description** and **job-to-be-done** against block text.
   - Ranked matches using keyword density and position.
   - Applied a 3-point scale (1 = most important, 3 = less relevant).
3. **Metadata Generation**:
   - Captured document names, timestamps, and structure.
4. **Subsection Analysis**:
   - For high-ranking blocks, refined content is stored separately for easier access.

## 🧪 Generalizability

Our method does not rely on domain-specific ML models, so it works across:
- Scientific documents
- Financial reports
- Educational textbooks

## ✅ Constraint Satisfaction

| Constraint             | Status         |
|------------------------|----------------|
| CPU-only               | ✅ Yes          |
| Model size < 1GB       | ✅ No ML used   |
| Runtime < 60s          | ✅ ~7–10s       |
| Offline Execution      | ✅ Fully offline|
| Docker Compatible      | ✅ Yes          |
