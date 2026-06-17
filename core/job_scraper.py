import requests
from bs4 import BeautifulSoup
import re


class JobScraper:

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    @staticmethod
    def clean_text(text):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    @classmethod
    def extract_job_description(
        cls,
        url
    ):

        try:

            response = requests.get(
                url,
                headers=cls.headers,
                timeout=20
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for tag in soup(
                [
                    "script",
                    "style",
                    "nav",
                    "footer",
                    "header"
                ]
            ):
                tag.decompose()

            text = soup.get_text(
                separator=" "
            )

            text = cls.clean_text(text)

            return text[:15000]

        except Exception as e:

            return f"Error: {str(e)}"