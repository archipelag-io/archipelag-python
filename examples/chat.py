"""
Example: Chat completion with the Archipelag SDK
"""

import os
from archipelag import Client

# Get API key from environment
api_key = os.environ.get("ARCHIPELAG_API_KEY", "ak_test_xxx")

# Initialize client
client = Client(api_key=api_key)

# Simple chat
print("=== Simple Chat ===")
result = client.chat("What is the capital of France?")
print(f"Response: {result.content}")
print(f"Tokens used: {result.usage.total_tokens}")

# Streaming chat
print("\n=== Streaming Chat ===")
print("Response: ", end="")
for event in client.chat_stream("Tell me a short joke"):
    if event.type == "token":
        print(event.content, end="", flush=True)
    elif event.type == "done":
        print(f"\n[{event.usage.total_tokens} tokens]")

# Chat with system prompt
print("\n=== Chat with System Prompt ===")
result = client.chat(
    prompt="Explain recursion",
    system_prompt="You are a patient programming teacher. Use simple analogies.",
    max_tokens=200,
)
print(f"Response: {result.content}")

client.close()
