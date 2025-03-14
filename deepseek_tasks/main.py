from openai import OpenAI

import yaml
from pathlib import Path
import os
import time


client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
)

template_file_name = 'php_traits.html'
config_file_name = 'config_php.yaml'


def load_config(config_file_name):
    with open(config_file_name, 'r') as file:
        chat_completions = yaml.safe_load(file)

    return chat_completions


def read_template(template_file_name):

    with open(template_file_name, 'r') as file:
        html_template = file.read()

    return html_template


def create_file(path, content):
    # Create the directories if they do not exist

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create the file
    file_path.touch()

    # Write content to the file
    file_path.write_text(content)

def get_path_part(title):

    if '-' in title:
        parts = title.split().lower()
        part = '-'.join(parts)
    else:
        part = title.lower()

    return part


def log_link(link):
    with open('links.txt', 'a') as file:
        file.write(link + '\n')
        


template = read_template(template_file_name)
chat_completion_options = load_config(config_file_name)
# print(chat_completion_options)

for option in chat_completion_options['chat_completions']:
    messages = option['messages']
    temperature = option['temperature']
    top_p = option['top_p']
    model = option['model']
    max_completion_tokens = option['max_completion_tokens']
    path = option['path']
    title = option['title']

    content = messages[0]['content']
    content += f"Use this HTML template as a reference: {template}"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        temperature=temperature,
        top_p=top_p,
        model=model,
        max_completion_tokens=max_completion_tokens
    )

    # print(chat_completion.choices[0].message.content)
    tutorial = chat_completion.choices[0].message.content
    create_file(path, tutorial)

    # print(f"Messages: {messages}")
    # print(f"Temperature: {temperature}")
    # print(f"Top_p: {top_p}")
    # print(f"Model: {model}")
    # print(f"Max Completion Tokens: {max_completion_tokens}")
    # print(f"Path: {path}")

    # print(f"Content: {content}")
# <li><a href="/java/synchronized/">Java synchronized</a></li>
    part = get_path_part(title)
    link = f'<li><a href="/linux/{part}/">{title}</li>'

    print(link)

    log_link(link)

    print('finished')  # Add a blank line between completions
    # time.sleep(60)





