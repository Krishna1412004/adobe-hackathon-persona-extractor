
import fitz
from extract_outline import extract_outline_from_pdf


def test_extracts_title_and_heading(tmp_path):
    pdf_path = tmp_path / "sample.pdf"

    # Create a controlled sample PDF for testing.
    doc = fitz.open()
    page = doc.new_page()

    page.insert_text((72, 72), "Sample Document Title", fontsize=24)
    page.insert_text((72, 120), "Introduction to Testing", fontsize=18)
    page.insert_text((72, 160), "Testing Details", fontsize=14)

    doc.save(pdf_path)
    doc.close()

    result = extract_outline_from_pdf(str(pdf_path))

    # Verify the title.
    assert result["title"] == "Sample Document Title"

    # Verify that the expected heading was extracted.
    assert any(
        item["text"] == "Introduction to Testing"
        and item["level"] == "H1"
        and item["page"] == 1
        for item in result["outline"]
    )

def test_empty_pdf_returns_empty_title_and_outline(tmp_path):
    pdf_path = tmp_path / "empty.pdf"

    doc = fitz.open()
    doc.new_page()
    doc.save(pdf_path)
    doc.close()

    result = extract_outline_from_pdf(str(pdf_path))

    assert result["title"] == ""
    assert result["outline"] == []



import json


def test_process_all_pdfs_creates_json_output(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    # Create a sample PDF in the input folder.
    pdf_path = input_dir / "sample.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (72, 72),
        "Sample Processing Document",
        fontsize=24
    )
    page.insert_text(
        (72, 120),
        "Introduction to Processing",
        fontsize=18
    )
    doc.save(pdf_path)
    doc.close()

    # Process the PDF.
    from extract_outline import process_all_pdfs

    process_all_pdfs(str(input_dir), str(output_dir))

    # Verify that the JSON output file was created.
    json_path = output_dir / "sample.json"
    assert json_path.exists()

    # Verify that the JSON file contains the expected structure.
    with open(json_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert result["title"] == "Sample Processing Document"
    assert isinstance(result["outline"], list)
