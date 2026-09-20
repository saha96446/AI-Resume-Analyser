import pymupdf


def extract_text_from_pdf(pdf_bytes):
    try:
        pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")

        text = ""

        for page in pdf:
            text += page.get_text("text") + "\n"

        pdf.close()

        return text.strip()

    except Exception as e:
        print("PDF EXTRACTION ERROR:", str(e))
        return ""
