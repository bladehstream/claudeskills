# Provider Comparison

## Model Capabilities

### Context Windows

| Provider | Model | Context | Notes |
|----------|-------|---------|-------|
| **Ollama** | llama3 (8B) | 8K | Local, free |
| **Ollama** | llama3 (70B) | 8K | Requires ~40GB VRAM |
| **Ollama** | mistral | 32K | Good for long docs |
| **Ollama** | codellama | 16K | Code-focused |
| **OpenAI** | gpt-4o | 128K | Best multimodal |
| **OpenAI** | gpt-4o-mini | 128K | Cost-effective |
| **OpenAI** | o1-preview | 128K | Deep reasoning |
| **Anthropic** | claude-opus-4 | 200K | Most capable |
| **Anthropic** | claude-sonnet-4 | 200K | Balanced |
| **Anthropic** | claude-haiku-4 | 200K | Fastest |
| **Gemini** | gemini-2.0-flash | 1M | Fastest, huge context |
| **Gemini** | gemini-2.5-pro | 1M | Best reasoning |

### Multimodal Support

| Provider | Vision | Audio | Video | Documents |
|----------|--------|-------|-------|-----------|
| Ollama | ✅ (llava) | ❌ | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ❌ | ✅ (PDF) |
| Anthropic | ✅ | ❌ | ❌ | ✅ (PDF) |
| Gemini | ✅ | ✅ | ✅ | ✅ (PDF) |

### Tool Use / Function Calling

| Provider | Tool Use | Parallel Calls | Structured Output |
|----------|----------|----------------|-------------------|
| Ollama | ✅ (some models) | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ✅ (JSON mode) |
| Anthropic | ✅ | ✅ | ❌ (use prefill) |
| Gemini | ✅ | ✅ | ✅ |

## Pricing (as of 2024)

### Per 1M Tokens

| Model | Input | Output |
|-------|-------|--------|
| **Ollama** | Free | Free |
| **gpt-4o** | $2.50 | $10.00 |
| **gpt-4o-mini** | $0.15 | $0.60 |
| **claude-opus-4** | $15.00 | $75.00 |
| **claude-sonnet-4** | $3.00 | $15.00 |
| **claude-haiku-4** | $0.25 | $1.25 |
| **gemini-2.0-flash** | $0.10 | $0.40 |
| **gemini-2.5-pro** | $1.25 | $5.00 |

### Cost Optimization Tips

1. **Use smaller models for simple tasks** - gpt-4o-mini, claude-haiku, gemini-flash
2. **Batch requests** - Anthropic offers batch API at 50% discount
3. **Cache responses** - Avoid duplicate API calls
4. **Use local models** - Ollama is free for unlimited use
5. **Prompt caching** - OpenAI and Anthropic offer cached input pricing

## Rate Limits

### Default Tier Limits

| Provider | Requests/min | Tokens/min | Daily |
|----------|--------------|------------|-------|
| **Ollama** | Unlimited | Unlimited | Unlimited |
| **OpenAI** (Tier 1) | 500 | 30,000 | — |
| **Anthropic** (Free) | 5 | 20,000 | 300K/month |
| **Gemini** (Free) | 15 | 1M | 1.5M/day |

### Handling Rate Limits

```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def call_with_retry(client, model, prompt):
    return client.chat(model, prompt)
```

## Model Selection Guide

### By Task Type

| Task | Recommended Model | Why |
|------|-------------------|-----|
| **Code generation** | claude-sonnet-4, gpt-4o | Best code quality |
| **Long document analysis** | gemini-2.0-flash | 1M context |
| **Cost-sensitive** | ollama/llama3 | Free |
| **Complex reasoning** | o1-preview, claude-opus-4 | Deep thinking |
| **Quick responses** | gpt-4o-mini, gemini-flash | Low latency |
| **Privacy-critical** | ollama/* | Local, no data leaves |
| **Multimodal** | gpt-4o, gemini-2.0-flash | Vision + audio |

### By Use Case

**Development/Testing:**
- Use Ollama for rapid iteration (no API costs)
- Use gpt-4o-mini for quick validation

**Production:**
- Start with claude-sonnet-4 or gpt-4o for quality
- Scale down to cheaper models after tuning prompts

**Research/Analysis:**
- Use gemini-2.0-flash for large document processing
- Use claude-opus-4 for nuanced analysis

## Local vs. Remote Trade-offs

### Local (Ollama)

**Pros:**
- No API costs
- No rate limits
- Full privacy (data never leaves machine)
- Works offline
- Customizable (fine-tuning possible)

**Cons:**
- Requires capable hardware (16GB+ RAM, GPU recommended)
- Smaller model selection
- Lower quality than top cloud models
- Self-managed (updates, troubleshooting)

### Remote (OpenAI, Anthropic, Gemini)

**Pros:**
- Access to most capable models
- No hardware requirements
- Automatic updates and improvements
- Better tool use and structured output support

**Cons:**
- API costs (can be significant at scale)
- Rate limits
- Data sent to third party
- Requires internet connection
- Potential for service outages

## Hardware Requirements for Ollama

### Minimum Specs by Model Size

| Model Size | RAM | VRAM | Example |
|------------|-----|------|---------|
| 7B | 8GB | 6GB | llama3-8b, mistral |
| 13B | 16GB | 10GB | codellama-13b |
| 34B | 32GB | 24GB | codellama-34b |
| 70B | 64GB | 48GB | llama3-70b |

### Recommended Setup

**Budget:**
- 16GB RAM
- RTX 3060 12GB
- Run: 7B models comfortably, 13B with offloading

**Mid-Range:**
- 32GB RAM
- RTX 4080 16GB
- Run: Up to 34B models

**High-End:**
- 64GB+ RAM
- RTX 4090 24GB or 2x 3090
- Run: 70B models
