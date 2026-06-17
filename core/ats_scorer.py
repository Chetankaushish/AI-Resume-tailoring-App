import re


class ATSScorer:

    @staticmethod
    def calculate_score(
        resume_text,
        job_description
    ):

        jd_words = set(
            re.findall(
                r"\w+",
                job_description.lower()
            )
        )

        resume_words = set(
            re.findall(
                r"\w+",
                resume_text.lower()
            )
        )

        if len(jd_words) == 0:
            return 0

        matched = (
            len(
                jd_words.intersection(
                    resume_words
                )
            )
        )

        score = (
            matched
            /
            len(jd_words)
        ) * 100

        return round(score)