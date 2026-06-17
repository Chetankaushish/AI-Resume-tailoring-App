from core.gemini_chain import (
    get_llm
)


def generate_cover_letter(
    resume_text,
    job_description
):

    llm = get_llm()

    prompt = f"""

Write a professional
cover letter.

Resume:

{resume_text}

Job Description:

{job_description}

"""

    response = llm.invoke(
        prompt
    )

    return response.content