#!/usr/bin/env python3
"""
Unified LLM Client
Provides a single interface for Ollama, OpenAI, Anthropic, and Google Gemini.

Usage:
    python llm_client.py <model> <prompt> [options]
    
Options:
    --system <prompt>    System prompt
    --temperature <t>    Temperature (0.0-2.0)
    --max-tokens <n>     Max output tokens
    --stream             Stream output
    --compare <models>   Compare comma-separated models
    --json               Request JSON output (OpenAI only)

Examples:
    python llm_client.py gpt-4o "Hello"
    python llm_client.py claude-sonnet-4-20250514 "Write code" --system "You are a Python expert"
    python llm_client.py ollama/llama3 "Explain AI" --stream
    python llm_client.py --compare "gpt-4o,claude-sonnet-4-20250514" "What is ML?"
"""

import os
import sys
import argparse
from typing import Generator, Optional, Dict, Any


class LLMClient:
    """Unified client for multiple LLM providers."""
    
    def __init__(self):
        self._openai_client = None
        self._anthropic_client = None
        self._gemini_client = None
    
    def _get_provider(self, model: str) -> str:
        """Detect provider from model name."""
        model_lower = model.lower()
        
        if model_lower.startswith("ollama/"):
            return "ollama"
        elif "gpt" in model_lower or "o1" in model_lower or model_lower.startswith("ft:"):
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "gemini" in model_lower:
            return "gemini"
        else:
            # Default to Ollama for unknown models (assume local)
            return "ollama"
    
    def _get_openai(self):
        """Lazy load OpenAI client."""
        if self._openai_client is None:
            from openai import OpenAI
            self._openai_client = OpenAI()
        return self._openai_client
    
    def _get_anthropic(self):
        """Lazy load Anthropic client."""
        if self._anthropic_client is None:
            from anthropic import Anthropic
            self._anthropic_client = Anthropic()
        return self._anthropic_client
    
    def _get_gemini(self):
        """Lazy load Gemini client."""
        if self._gemini_client is None:
            from google import genai
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable required")
            self._gemini_client = genai.Client(api_key=api_key)
        return self._gemini_client
    
    def chat(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> str:
        """
        Send a chat message to the specified model.
        
        Args:
            model: Model identifier (e.g., "gpt-4o", "claude-sonnet-4-20250514", "ollama/llama3")
            prompt: User message
            system: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Provider-specific options
        
        Returns:
            Model response text
        """
        provider = self._get_provider(model)
        
        if provider == "ollama":
            return self._chat_ollama(model, prompt, system, temperature, max_tokens)
        elif provider == "openai":
            return self._chat_openai(model, prompt, system, temperature, max_tokens, **kwargs)
        elif provider == "anthropic":
            return self._chat_anthropic(model, prompt, system, temperature, max_tokens)
        elif provider == "gemini":
            return self._chat_gemini(model, prompt, system, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider for model: {model}")
    
    def _chat_ollama(self, model: str, prompt: str, system: Optional[str], 
                     temperature: float, max_tokens: int) -> str:
        """Chat via Ollama."""
        import ollama
        
        # Strip "ollama/" prefix if present
        model_name = model.replace("ollama/", "")
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        return response["message"]["content"]
    
    def _chat_openai(self, model: str, prompt: str, system: Optional[str],
                     temperature: float, max_tokens: int, **kwargs) -> str:
        """Chat via OpenAI."""
        client = self._get_openai()
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        create_kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Handle JSON mode
        if kwargs.get("response_format"):
            create_kwargs["response_format"] = kwargs["response_format"]
        
        response = client.chat.completions.create(**create_kwargs)
        return response.choices[0].message.content
    
    def _chat_anthropic(self, model: str, prompt: str, system: Optional[str],
                        temperature: float, max_tokens: int) -> str:
        """Chat via Anthropic."""
        client = self._get_anthropic()
        
        create_kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system:
            create_kwargs["system"] = system
        
        # Anthropic doesn't support temperature > 1
        if temperature <= 1.0:
            create_kwargs["temperature"] = temperature
        
        message = client.messages.create(**create_kwargs)
        return message.content[0].text
    
    def _chat_gemini(self, model: str, prompt: str, system: Optional[str],
                     temperature: float, max_tokens: int) -> str:
        """Chat via Google Gemini."""
        client = self._get_gemini()
        from google.genai import types
        
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        if system:
            config.system_instruction = system
        
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )
        return response.text
    
    def stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Generator[str, None, None]:
        """
        Stream a chat response from the specified model.
        
        Yields:
            Response text chunks
        """
        provider = self._get_provider(model)
        
        if provider == "ollama":
            yield from self._stream_ollama(model, prompt, system, temperature, max_tokens)
        elif provider == "openai":
            yield from self._stream_openai(model, prompt, system, temperature, max_tokens)
        elif provider == "anthropic":
            yield from self._stream_anthropic(model, prompt, system, temperature, max_tokens)
        elif provider == "gemini":
            yield from self._stream_gemini(model, prompt, system, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider for model: {model}")
    
    def _stream_ollama(self, model: str, prompt: str, system: Optional[str],
                       temperature: float, max_tokens: int) -> Generator[str, None, None]:
        """Stream via Ollama."""
        import ollama
        
        model_name = model.replace("ollama/", "")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        stream = ollama.chat(
            model=model_name,
            messages=messages,
            options={"temperature": temperature, "num_predict": max_tokens},
            stream=True
        )
        
        for chunk in stream:
            if chunk.get("message", {}).get("content"):
                yield chunk["message"]["content"]
    
    def _stream_openai(self, model: str, prompt: str, system: Optional[str],
                       temperature: float, max_tokens: int) -> Generator[str, None, None]:
        """Stream via OpenAI."""
        client = self._get_openai()
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def _stream_anthropic(self, model: str, prompt: str, system: Optional[str],
                          temperature: float, max_tokens: int) -> Generator[str, None, None]:
        """Stream via Anthropic."""
        client = self._get_anthropic()
        
        create_kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system:
            create_kwargs["system"] = system
        if temperature <= 1.0:
            create_kwargs["temperature"] = temperature
        
        with client.messages.stream(**create_kwargs) as stream:
            for text in stream.text_stream:
                yield text
    
    def _stream_gemini(self, model: str, prompt: str, system: Optional[str],
                       temperature: float, max_tokens: int) -> Generator[str, None, None]:
        """Stream via Google Gemini."""
        client = self._get_gemini()
        from google.genai import types
        
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        if system:
            config.system_instruction = system
        
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=prompt,
            config=config
        ):
            if chunk.text:
                yield chunk.text
    
    def list_ollama_models(self) -> list:
        """List available Ollama models."""
        import ollama
        models = ollama.list()
        return [m["name"] for m in models.get("models", [])]


def main():
    parser = argparse.ArgumentParser(description="Unified LLM Client")
    parser.add_argument("model", nargs="?", help="Model identifier")
    parser.add_argument("prompt", nargs="?", help="User prompt")
    parser.add_argument("--system", "-s", help="System prompt")
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--max-tokens", "-m", type=int, default=1024)
    parser.add_argument("--stream", action="store_true", help="Stream output")
    parser.add_argument("--compare", help="Compare comma-separated models")
    parser.add_argument("--json", action="store_true", help="Request JSON output")
    parser.add_argument("--list-ollama", action="store_true", help="List Ollama models")
    
    args = parser.parse_args()
    
    client = LLMClient()
    
    if args.list_ollama:
        models = client.list_ollama_models()
        print("Available Ollama models:")
        for m in models:
            print(f"  - ollama/{m}")
        return
    
    if args.compare:
        if not args.prompt:
            print("Error: prompt required for comparison", file=sys.stderr)
            sys.exit(1)
        
        models = [m.strip() for m in args.compare.split(",")]
        for model in models:
            print(f"\n{'='*60}")
            print(f"Model: {model}")
            print('='*60)
            try:
                response = client.chat(
                    model=model,
                    prompt=args.prompt,
                    system=args.system,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens
                )
                print(response)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
        return
    
    if not args.model or not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    kwargs = {}
    if args.json:
        kwargs["response_format"] = {"type": "json_object"}
    
    try:
        if args.stream:
            for chunk in client.stream(
                model=args.model,
                prompt=args.prompt,
                system=args.system,
                temperature=args.temperature,
                max_tokens=args.max_tokens
            ):
                print(chunk, end="", flush=True)
            print()  # Final newline
        else:
            response = client.chat(
                model=args.model,
                prompt=args.prompt,
                system=args.system,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                **kwargs
            )
            print(response)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
