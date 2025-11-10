# -*- coding:utf-8 -*-
import json
import os
import base64
from io import BytesIO
from copy import deepcopy
from ._api_key import *
os.environ['OPENAI_API_KEY'] = get_openai_api_key()
os.environ['ANTHROPIC_API_KEY'] = get_claude_api_key()

def call_gpt4o(client, image, text_prompt, temperature:float=0.0, timeout:int=120):
    """
    from openai import OpenAI
    client = OpenAI()
    model = 'gpt-4o-2024-08-06'
    """
    # Only text
    if image is None:
        message = \
            [
                {'role': 'user', 'content': [
                    {'type': 'text', 'text': text_prompt},
                ]}
            ]
    # Single image
    elif type(image) != list:
        # PIL to base64
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        byte_data = img_buffer.getvalue()
        image_base64 = base64.b64encode(byte_data).decode('utf-8')
        message = \
            [
                {'role':'user', 'content':[
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_base64}'}},
                    {'type': 'text', 'text': text_prompt},
                    ]}
            ]
    # Multiple images
    else:
        images = deepcopy(image)
        message = [{'role':'user', 'content':[]}]
        for image in images:
            # PIL to base64
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')
            byte_data = img_buffer.getvalue()
            image_base64 = base64.b64encode(byte_data).decode('utf-8')
            message[0]['content'].append(
                {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_base64}'}})
        message[0]['content'].append({'type': 'text', 'text': text_prompt})
    # Invoke GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=message,
        temperature=temperature,
        timeout=timeout
    )
    output = response.choices[0].message.content
    # usage = response.usage
    return output


def call_gpt4o_mini(client, image, text_prompt, temperature:float=0.0, timeout:int=120):
    """
    from openai import OpenAI
    client = OpenAI()
    model = 'gpt-4o-mini-2024-07-18'
    """
    # Only text
    if image is None:
        message = \
            [
                {'role': 'user', 'content': [
                    {'type': 'text', 'text': text_prompt},
                ]}
            ]
    # Single image
    elif type(image) != list:
        # PIL to base64
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        byte_data = img_buffer.getvalue()
        image_base64 = base64.b64encode(byte_data).decode('utf-8')
        message = \
            [
                {'role':'user', 'content':[
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_base64}'}},
                    {'type': 'text', 'text': text_prompt},
                    ]}
            ]
    # Multiple images
    else:
        images = deepcopy(image)
        message = [{'role': 'user', 'content': []}]
        for image in images:
            # PIL to base64
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')
            byte_data = img_buffer.getvalue()
            image_base64 = base64.b64encode(byte_data).decode('utf-8')
            message[0]['content'].append(
                {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_base64}'}})
        message[0]['content'].append({'type': 'text', 'text': text_prompt})
    # Invoke GPT-4o-mini
    response = client.chat.completions.create(
    model='gpt-4o-mini-2024-07-18',
    messages=message,
    temperature=temperature,
    timeout=timeout)
    output = response.choices[0].message.content
    # usage = response.usage
    return output


def call_claude35sonnet(client, image, text_prompt, temperature:float=0.0, timeout:int=120):
    """
    from anthropic import Anthropic
    client = Anthropic()
    model = 'claude-3-5-sonnet-20241022'
    """
    # Only text
    if image is None:
        message = \
            [
                {'role': 'user', 'content': [
                    {'type': 'text', 'text': text_prompt},
                ]}
            ]
    # Single image
    elif type(image) != list:
        # PIL to base64
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        byte_data = img_buffer.getvalue()
        image_base64 = base64.standard_b64encode(byte_data).decode('utf-8')
        message = \
            [
                {'role':'user', 'content':[
                    {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': image_base64}},
                    {'type': 'text', 'text': text_prompt},
                    ]}
            ]
    # Multiple images
    else:
        images = deepcopy(image)
        message = [{'role':'user', 'content':[]}]
        i = 0
        for image in images:
            i += 1
            # PIL to base64
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')
            byte_data = img_buffer.getvalue()
            image_base64 = base64.standard_b64encode(byte_data).decode('utf-8')
            message[0]['content'].append({'type': 'text', 'text': f'Image {i}:'})
            message[0]['content'].append(
                {'type': 'image','source': {'type': 'base64', 'media_type': 'image/png', 'data': image_base64}})
        message[0]['content'].append({'type': 'text', 'text': text_prompt})
    # Invoke Claude-3.5-Sonnet
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=message,
        temperature=temperature,
        timeout=timeout
    )
    output = response.content[0].text
    # usage = response.usage
    return output

