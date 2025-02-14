from openai import OpenAI

client = OpenAI(api_key="sk-08a2733fe2b64e8993cedb805f8ce78e", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Me der um exmeplo de codigo em python usando pyside6 ?"},
    ],
    stream=False
)

print(response.choices[0].message.content)