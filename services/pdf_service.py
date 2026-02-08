from pypdf import PdfReader
import io

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file uploaded via Flask.
    """
    try:
        # 1. Read the PDF stream
        reader = PdfReader(pdf_file)
        text = ""

        # 2. Loop through all pages and extract text
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        
        return text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""