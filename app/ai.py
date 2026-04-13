from openai import OpenAI
from django.conf import settings

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=settings.NVIDIA_API_KEY
)

def get_ai_advice(condition, result):
    prompt = f"""
    User health condition: {condition}
    Prediction: {result}

    Give:
    1. Simple explanation
    2. 3 tips
    3. 1 small habit
    4. 1 fun activity or game
    """

    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5,
        max_tokens=500
    )

    return completion.choices[0].message.content