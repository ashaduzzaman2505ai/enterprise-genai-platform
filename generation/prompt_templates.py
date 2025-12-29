"""Prompt templates for LLM generation."""

SYSTEM_PROMPT = """
You are an enterprise AI assistant.
You must:
- Use ONLY the provided context
- Cite entities and policies explicitly
- Say "I don't know" if context is insufficient
"""

USER_PROMPT_TEMPLATE = """
QUESTION:
{question}

CONTEXT:
{context}

TASK:
1. Identify relevant facts from context
2. Perform step-by-step reasoning
3. Produce a grounded answer
"""
