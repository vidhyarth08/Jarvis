from openai import OpenAI

# pip install openai
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
   api_key = "sk-_vssegvTrNczQ9_cbMYFFFeReTnGNgddvTY2Hj_tjST3BlbkFJtrbiHyQoR8a98lChcpTU99Np5qzN5avnTWSKSp3PAA",
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant jarvis."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)