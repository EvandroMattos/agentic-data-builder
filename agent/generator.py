from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_pipeline(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
You are a Senior Data Engineer.

Generate a production-ready PySpark pipeline with:
- Bronze layer ingestion
- Silver layer transformation
- Clear function separation
- Comments and best practices
- SparkSession initialization

Return ONLY Python code.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content