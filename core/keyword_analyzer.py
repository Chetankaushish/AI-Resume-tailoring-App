import re


class KeywordAnalyzer:

    @staticmethod
    def extract_keywords(text):

        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            text.lower()
        )

        stop_words = {
            "with","from","that",
            "have","will","your",
            "this","their","they",
            "into","about","using",
            "must","should","years"
        }

        words = [
            w for w in words
            if w not in stop_words
        ]

        return set(words)

    @staticmethod
    def missing_keywords(
        resume_text,
        job_description
    ):

        resume_words = (
            KeywordAnalyzer
            .extract_keywords(
                resume_text
            )
        )

        jd_words = (
            KeywordAnalyzer
            .extract_keywords(
                job_description
            )
        )

        missing = list(
            jd_words - resume_words
        )

        return sorted(
            missing
        )[:30]