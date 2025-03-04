import pymupdf


#################################################################################
#################################################################################
def read_pdf(file_path: str, credentials: str | None = None) -> str:

    pdf_file = pymupdf.open(file_path)
    text = ""

    if pdf_file.is_encrypted:
        if not credentials:
            raise RuntimeError("PDF file is encrypted. Please provide credentials")
        pdf_file.authenticate(credentials)

    for page in pdf_file:
        text += page.get_text()

    pdf_file.close()

    return text
