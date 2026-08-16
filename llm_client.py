import json
import os
import urllib.request
import urllib.error

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


def generate_section(system_prompt, user_prompt):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Set it before running --online mode.")

    body = json.dumps({
        "model": MODEL,
        "max_completion_tokens": 900,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "genar-challenge/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"Groq API error {e.code}: {error_body}") from e

    return result["choices"][0]["message"]["content"].strip()