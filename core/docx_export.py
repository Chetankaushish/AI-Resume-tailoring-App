from docx import Document

def export_docx(content, path):

    doc = Document()

    doc.add_paragraph(content)

    doc.save(path)

    return path