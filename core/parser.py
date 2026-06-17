from pypdf import PdfReader
from docx import Document
import tempfile
import os


class ResumeParser:

    @staticmethod
    def parse_pdf(uploaded_file):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        text = ""

        try:

            reader = PdfReader(temp_path)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        finally:

            os.remove(temp_path)

        return text

    @staticmethod
    def parse_docx(uploaded_file):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".docx"
        ) as tmp:

            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        try:

            doc = Document(temp_path)

            text = "\n".join(
                para.text
                for para in doc.paragraphs
            )

        finally:

            os.remove(temp_path)

        return text

    @staticmethod
    def parse_txt(uploaded_file):

        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    @staticmethod
    def extract_text(uploaded_file):

        filename = uploaded_file.name.lower()

        if filename.endswith(".pdf"):
            return ResumeParser.parse_pdf(
                uploaded_file
            )

        elif filename.endswith(".docx"):
            return ResumeParser.parse_docx(
                uploaded_file
            )

        elif filename.endswith(".txt"):
            return ResumeParser.parse_txt(
                uploaded_file
            )

        else:

            raise ValueError(
                "Unsupported File Format"
            )