from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_pipeline(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate PySpark pipelines"},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content