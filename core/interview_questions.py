from core.gemini_chain import (
    get_llm
)


def generate_questions(
    job_description
):

    llm = get_llm()

    prompt = f"""

Generate:

10 Technical Questions

10 HR Questions

Job Description:

{job_description}

"""

    response = llm.invoke(
        prompt
    )

    return response.content