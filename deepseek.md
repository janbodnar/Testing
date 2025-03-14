# DeepSeek

```python
from openai import OpenAI

import os


client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
)

content = 'what day is today?'
# content += f"Use this HTML template as a reference: {template}"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": content,
        }
    ],
    temperature=0.9,
    top_p=0.7,
    model="deepseek-chat",
    max_completion_tokens=90_000
)

output = chat_completion.choices[0].message.content
print(output)

print('finished') 
```
