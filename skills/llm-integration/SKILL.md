---
name: llm-integration
description: Unified interface for LLM integration across local (Ollama) and remote providers (OpenAI, Anthropic Claude, Google Gemini). Use when tasks require generating text, chat completions, embeddings, structured outputs, or orchestrating multiple LLMs. Triggers include "call GPT", "use Claude", "run local LLM", "generate with Ollama", "compare models", or any task requiring LLM API integration.
---

# LLM Integration

Unified Python interface for local and remote LLM providers.

## Setup

```bash
pip install ollama openai anthropic google-genai --break-system-packages
```

**Environment Variables:**
```bash
# Remote APIs
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Ollama (local)
# No API key needed - runs on localhost:11434
```

## Quick Start

```python
from scripts.llm_client import LLMClient

# Auto-detects provider from model name
client = LLMClient()

# Remote providers
response = client.chat("gpt-4o", "Explain quantum computing")
response = client.chat("claude-sonnet-4-20250514", "Write a haiku about code")
response = client.chat("gemini-2.0-flash", "Summarize this document")

# Local Ollama
response = client.chat("ollama/llama3", "Hello, how are you?")
response = client.chat("ollama/mistral", "Explain recursion")
```

## Provider Reference

### Ollama (Local)

```python
import ollama

# Simple generation
response = ollama.generate(model='llama3', prompt='Why is the sky blue?')
print(response['response'])

# Chat with history
response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Hello!'},
    ]
)
print(response['message']['content'])

# Streaming
stream = ollama.chat(model='llama3', messages=[...], stream=True)
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

# List available models
models = ollama.list()
```

**Ollama Setup:**
```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3
ollama pull mistral
ollama pull codellama

# Run server (if not running as service)
ollama serve
```

### OpenAI

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

# Chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=1024,
    temperature=0.7
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

# JSON mode
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    response_format={"type": "json_object"}
)
```

**Current Models:**
| Model | Context | Best For |
|-------|---------|----------|
| `gpt-4o` | 128K | Best overall |
| `gpt-4o-mini` | 128K | Cost-effective |
| `gpt-4-turbo` | 128K | Complex reasoning |
| `o1-preview` | 128K | Deep reasoning |

### Anthropic Claude

```python
from anthropic import Anthropic

client = Anthropic()  # Uses ANTHROPIC_API_KEY env var

# Message creation
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain machine learning"}
    ]
)
print(message.content[0].text)

# With system prompt
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are an expert Python developer.",
    messages=[
        {"role": "user", "content": "Review this code..."}
    ]
)

# Streaming
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[...]
) as stream:
    for text in stream.text_stream:
        print(text, end='', flush=True)
```

**Current Models:**
| Model | Context | Best For |
|-------|---------|----------|
| `claude-opus-4-20250514` | 200K | Most capable |
| `claude-sonnet-4-20250514` | 200K | Balanced |
| `claude-haiku-4-20250514` | 200K | Fast, cheap |

### Google Gemini

```python
from google import genai

client = genai.Client(api_key='GEMINI_API_KEY')

# Generate content
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Explain how AI works'
)
print(response.text)

# With configuration
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Write a poem',
    config=types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=500,
        system_instruction='You are a creative poet.'
    )
)

# Streaming
for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash',
    contents='Tell me a story'
):
    print(chunk.text, end='', flush=True)
```

**Current Models:**
| Model | Context | Best For |
|-------|---------|----------|
| `gemini-2.0-flash` | 1M | Fast, multimodal |
| `gemini-2.5-pro` | 1M | Best reasoning |
| `gemini-2.5-flash` | 1M | Cost-effective |

## Unified Client Usage

The included `scripts/llm_client.py` provides a unified interface:

```python
from scripts.llm_client import LLMClient

client = LLMClient()

# Automatic provider detection
response = client.chat("gpt-4o", "Hello")           # → OpenAI
response = client.chat("claude-sonnet-4-20250514", "Hello")  # → Anthropic
response = client.chat("gemini-2.0-flash", "Hello") # → Gemini
response = client.chat("ollama/llama3", "Hello")    # → Ollama

# With options
response = client.chat(
    model="gpt-4o",
    prompt="Analyze this data",
    system="You are a data analyst.",
    temperature=0.3,
    max_tokens=2000
)

# Streaming (all providers)
for chunk in client.stream("claude-sonnet-4-20250514", "Write a story"):
    print(chunk, end='', flush=True)
```

## Common Patterns

### Multi-Model Comparison

```python
models = ["gpt-4o", "claude-sonnet-4-20250514", "gemini-2.0-flash", "ollama/llama3"]
prompt = "Explain the Pythagorean theorem in simple terms."

for model in models:
    response = client.chat(model, prompt)
    print(f"\n=== {model} ===\n{response}")
```

### Fallback Chain

```python
def chat_with_fallback(prompt, models):
    """Try models in order until one succeeds."""
    for model in models:
        try:
            return client.chat(model, prompt)
        except Exception as e:
            print(f"{model} failed: {e}")
            continue
    raise Exception("All models failed")

response = chat_with_fallback(
    "Hello",
    ["gpt-4o", "claude-sonnet-4-20250514", "ollama/llama3"]
)
```

### Structured Output

```python
# OpenAI JSON mode
response = client.chat(
    "gpt-4o",
    "List 3 programming languages with their use cases. Return as JSON.",
    response_format={"type": "json_object"}
)

# Claude with prefilled response
response = client.chat(
    "claude-sonnet-4-20250514",
    "List 3 languages as JSON array",
    system="Always respond with valid JSON only."
)
```

## Script Usage

```bash
# Simple query
python scripts/llm_client.py "gpt-4o" "What is 2+2?"

# With system prompt
python scripts/llm_client.py "claude-sonnet-4-20250514" "Review this code" --system "You are a code reviewer"

# Compare models
python scripts/llm_client.py --compare "gpt-4o,claude-sonnet-4-20250514,ollama/llama3" "Explain recursion"

# Streaming output
python scripts/llm_client.py "gemini-2.0-flash" "Write a story" --stream
```

## Reference Documents

- `references/provider-comparison.md` — Model capabilities, pricing, rate limits
- `references/advanced-patterns.md` — Tool use, embeddings, vision, async patterns
