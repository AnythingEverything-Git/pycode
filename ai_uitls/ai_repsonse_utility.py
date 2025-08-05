from groq import Groq

MODEL_NAME = "llama3-8b-8192"  # Groq LLaMA model

client = Groq()

def ai_response(prompt, system_role):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response
