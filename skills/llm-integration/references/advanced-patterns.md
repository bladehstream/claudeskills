# Advanced LLM Patterns

## Tool Use / Function Calling

### OpenAI Tools

```python
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g., 'San Francisco, CA'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "fahrenheit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    tools=tools,
    tool_choice="auto"
)

# Check if model wants to call a tool
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    # Execute the function
    result = get_weather(**arguments)
    
    # Send result back to model
    messages = [
        {"role": "user", "content": "What's the weather in Boston?"},
        response.choices[0].message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
    ]
    
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
```

### Anthropic Tools

```python
from anthropic import Anthropic

client = Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state"
                }
            },
            "required": ["location"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Boston?"}]
)

# Check for tool use
for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        tool_use_id = block.id
        
        # Execute function
        result = get_weather(**tool_input)
        
        # Continue conversation with result
        messages = [
            {"role": "user", "content": "What's the weather in Boston?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(result)
                }]
            }
        ]
        
        final_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
```

### Gemini Tools

```python
from google import genai
from google.genai import types

client = genai.Client(api_key='...')

# Define function (automatically converted to tool)
def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Args:
        location: City and state, e.g., 'San Francisco, CA'
    """
    # Your implementation
    return f"Weather in {location}: 72°F, sunny"

# Automatic function calling
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='What is the weather in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_weather]  # Pass function directly
    )
)
print(response.text)  # Includes weather result
```

## Embeddings

### OpenAI Embeddings

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["Hello world", "How are you?"]
)

embeddings = [item.embedding for item in response.data]
# Each embedding is a list of 1536 floats
```

### Ollama Embeddings

```python
import ollama

response = ollama.embeddings(
    model='nomic-embed-text',
    prompt='Hello world'
)
embedding = response['embedding']
```

### Simple Vector Search

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query_embedding, documents, doc_embeddings, top_k=3):
    """Find most similar documents."""
    similarities = [
        cosine_similarity(query_embedding, doc_emb)
        for doc_emb in doc_embeddings
    ]
    
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [(documents[i], similarities[i]) for i in top_indices]
```

## Vision / Multimodal

### OpenAI Vision

```python
from openai import OpenAI
import base64

client = OpenAI()

# From URL
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
            ]
        }
    ]
)

# From local file (base64)
def encode_image(path):
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

image_data = encode_image("photo.jpg")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                }
            ]
        }
    ]
)
```

### Anthropic Vision

```python
from anthropic import Anthropic
import base64

client = Anthropic()

# Encode image
with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)
```

### Gemini Vision

```python
from google import genai
from google.genai import types
import PIL.Image

client = genai.Client(api_key='...')

# From file
image = PIL.Image.open('photo.jpg')

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        "What's in this image?",
        image
    ]
)
print(response.text)
```

## Async Patterns

### Async OpenAI

```python
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI()
    
    # Single request
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # Parallel requests
    prompts = ["Question 1", "Question 2", "Question 3"]
    tasks = [
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": p}]
        )
        for p in prompts
    ]
    responses = await asyncio.gather(*tasks)
    
asyncio.run(main())
```

### Async Anthropic

```python
import asyncio
from anthropic import AsyncAnthropic

async def main():
    client = AsyncAnthropic()
    
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
    
asyncio.run(main())
```

### Async Streaming

```python
async def stream_response():
    client = AsyncOpenAI()
    
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a story"}],
        stream=True
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
```

## Conversation Management

### Chat History

```python
class Conversation:
    def __init__(self, client, model, system=None):
        self.client = client
        self.model = model
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})
    
    def add_user(self, content):
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant(self, content):
        self.messages.append({"role": "assistant", "content": content})
    
    def chat(self, user_input):
        self.add_user(user_input)
        
        response = self.client.chat(
            model=self.model,
            messages=self.messages
        )
        
        self.add_assistant(response)
        return response
    
    def clear(self):
        system = self.messages[0] if self.messages and self.messages[0]["role"] == "system" else None
        self.messages = [system] if system else []

# Usage
conv = Conversation(client, "gpt-4o", system="You are a helpful assistant.")
response1 = conv.chat("Hello!")
response2 = conv.chat("What did I just say?")  # Has context
```

### Context Window Management

```python
import tiktoken

def count_tokens(text, model="gpt-4o"):
    """Count tokens in text."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def trim_messages(messages, max_tokens=8000, model="gpt-4o"):
    """Trim old messages to fit context window."""
    encoding = tiktoken.encoding_for_model(model)
    
    # Always keep system message
    system = messages[0] if messages[0]["role"] == "system" else None
    other_messages = messages[1:] if system else messages
    
    total_tokens = count_tokens(system["content"]) if system else 0
    kept_messages = []
    
    # Keep recent messages that fit
    for msg in reversed(other_messages):
        msg_tokens = count_tokens(msg["content"])
        if total_tokens + msg_tokens < max_tokens:
            kept_messages.insert(0, msg)
            total_tokens += msg_tokens
        else:
            break
    
    return ([system] if system else []) + kept_messages
```

## Structured Output

### JSON Mode (OpenAI)

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You output valid JSON only."},
        {"role": "user", "content": "List 3 countries with capitals as JSON"}
    ],
    response_format={"type": "json_object"}
)

data = json.loads(response.choices[0].message.content)
```

### Pydantic Validation

```python
from pydantic import BaseModel
from typing import List

class Country(BaseModel):
    name: str
    capital: str
    population: int

class CountryList(BaseModel):
    countries: List[Country]

def get_structured_output(prompt, schema: type[BaseModel]):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"Output valid JSON matching this schema: {schema.model_json_schema()}"
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return schema.model_validate_json(response.choices[0].message.content)

result = get_structured_output("List 3 European countries", CountryList)
print(result.countries[0].name)
```

## Error Handling

### Retry with Backoff

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    # Exponential backoff
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def call_llm(prompt):
    return client.chat("gpt-4o", prompt)
```

### Provider-Specific Error Handling

```python
from openai import RateLimitError, APIError
from anthropic import RateLimitError as AnthropicRateLimit

def safe_call(client, model, prompt):
    try:
        return client.chat(model, prompt)
    except RateLimitError:
        print("OpenAI rate limited, waiting...")
        time.sleep(60)
        return client.chat(model, prompt)
    except AnthropicRateLimit:
        print("Anthropic rate limited, waiting...")
        time.sleep(60)
        return client.chat(model, prompt)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
```
