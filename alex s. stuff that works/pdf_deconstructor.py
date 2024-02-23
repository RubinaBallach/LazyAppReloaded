import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    try:
        pdf_document = fitz.open(file_path)
        text_content = ""

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_content += page.get_text()

        return text_content

    except Exception as e:
        # Handle exceptions such as file not found or PDF parsing issues
        print(f"Error extracting text from PDF: {e}")
        return None

# Example usage:
file_path = "/home/user/Desktop/jobsuche/final cvs/EN CV_AlexanderSimakov.pdf"
#file_path = "/home/user/Desktop/jobsuche/final cvs/TestCV Lazy App.pdf"
cv_text = extract_text_from_pdf(file_path)

if cv_text is not None:
    print("Extracted CV Text:")
    print(cv_text)
else:
    print("Failed to extract text from the PDF.")
