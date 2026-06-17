ATS_PROMPT = """

You are an ATS Resume Expert.

Analyze the Resume and Job Description.

Return:

1. ATS Score (0-100)

2. Missing Keywords

3. Skills Gap

4. Resume Summary Suggestions

5. Experience Improvements

6. Project Improvements

7. Final ATS Optimized Resume

Resume Context:

{resume_context}

Job Description:

{job_description}

"""