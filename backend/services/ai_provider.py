"""Multi-provider AI calling layer.

Supports Anthropic, OpenAI, and Gemini. Picks a provider based on
AI_PROVIDER if set, otherwise the first one with an API key configured
(checked in that order). Every call site treats a missing/failed provider
the same way: fall back to static placeholder copy. A draft should never
hard-fail just because a provider key isn't set or a call didn't come back
clean.
"""
import json
import os
import re

PROVIDER_ORDER = ["anthropic", "openai", "gemini"]

DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-5",
    "openai": "gpt-5.5",
    "gemini": "gemini-3.7-flash",
}

_API_KEY_ENV = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
}

_MODEL_ENV = {
    "anthropic": "ANTHROPIC_MODEL",
    "openai": "OPENAI_MODEL",
    "gemini": "GEMINI_MODEL",
}

PROVIDER_DISPLAY_NAMES = {
    "anthropic": "Claude",
    "openai": "OpenAI",
    "gemini": "Gemini",
}


def active_provider():
    """Which provider will actually be used right now, or None if nothing
    is configured. AI_PROVIDER overrides auto-detection when it names a
    provider that also has a key set."""
    requested = os.environ.get("AI_PROVIDER", "").strip().lower()
    if requested in PROVIDER_ORDER and os.environ.get(_API_KEY_ENV[requested]):
        return requested
    for provider in PROVIDER_ORDER:
        if os.environ.get(_API_KEY_ENV[provider]):
            return provider
    return None


def _model_for(provider):
    return os.environ.get(_MODEL_ENV[provider], DEFAULT_MODELS[provider])


def _call_anthropic(prompt):
    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ[_API_KEY_ENV["anthropic"]])
    response = client.messages.create(
        model=_model_for("anthropic"),
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def _call_openai(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ[_API_KEY_ENV["openai"]])
    response = client.chat.completions.create(
        model=_model_for("openai"),
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _call_gemini(prompt):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ[_API_KEY_ENV["gemini"]])
    response = client.models.generate_content(
        model=_model_for("gemini"),
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=1000),
    )
    return response.text


_CALLERS = {
    "anthropic": _call_anthropic,
    "openai": _call_openai,
    "gemini": _call_gemini,
}


def extract_json(text):
    """Strip markdown code fences (models love adding them despite being
    told not to) and parse. Raises on anything that isn't valid JSON."""
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return json.loads(text)


def generate(prompt):
    """Send a prompt to whichever provider is active and parse the JSON
    response. Returns (parsed_dict, provider_name), or (None, None) if no
    provider is configured or the call/parse fails for any reason."""
    provider = active_provider()
    if provider is None:
        return None, None
    try:
        raw = _CALLERS[provider](prompt)
        if not raw:
            return None, None
        return extract_json(raw), provider
    except Exception:
        return None, None
