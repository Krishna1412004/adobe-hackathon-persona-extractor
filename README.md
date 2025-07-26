# Adobe Hackathon - Round 1A

**Challenge:** Extract structured outline (title + headings) from PDFs in a clean, hierarchical JSON format.

---

## 🚀 How It Works

This solution:
- Accepts `.pdf` files via `/app/input`
- Extracts:
  - Title
  - Headings (H1, H2, H3) with page numbers
- Outputs matching `.json` files into `/app/output`
- Fully offline and runs inside Docker in < 10s

---

## 🛠️ Tech Stack

- Python 3.10
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
- Docker (CPU-only, AMD64)

---

## 📂 Folder Structure

```
project/
├── extract_outline.py       # Main script
├── Dockerfile               # For building container
├── input/                   # Put your PDFs here
├── output/                  # JSONs will appear here
```

---

## 🐳 How to Build & Run

### 1. Build Docker Image

```bash
docker build --platform linux/amd64 -t outline_extractor:adobe .
```

### 2. Run the Container

**PowerShell:**

```bash
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none outline_extractor:adobe
```

**Command Prompt (CMD):**

```cmd
docker run --rm -v %cd%/input:/app/input -v %cd%/output:/app/output --network none outline_extractor:adobe
```

---

## 📄 Sample Output (JSON)

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## 🧠 Approach Summary

- Font size is used as a key signal to infer heading levels
- Top 3 font sizes are mapped to Title → H1 → H2
- Remaining smaller fonts are considered as H3
- Fully rule-based, fast, and works offline

---

## ✅ Constraints Met

| Constraint            | Status           |
|----------------------|------------------|
| CPU-only              | ✅ Yes           |
| Runtime < 10 sec      | ✅ Yes           |
| Model size < 200MB    | ✅ No ML used    |
| Offline execution     | ✅ Fully offline |
| Docker compatible     | ✅ Yes           |

---

## 👨‍💻 Author

**Krishna Arora**  
karora._be22@thapar.edu  
Thapar Institute of Engineering and Technology
