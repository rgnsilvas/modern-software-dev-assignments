from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)

def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False

def extract_action_items(text: str) -> List[str]:
    """Fungsi lama menggunakan pendekatan berbasis aturan (heuristics)."""
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)

    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique

def extract_action_items_llm(text: str) -> List[str]:
    """
    TODO 1: Implementasi ekstraksi action items menggunakan LLM (Ollama).
    Fungsi ini meminta AI untuk mengidentifikasi tugas dan mengembalikannya dalam format JSON.
    """
    if not text.strip():
        return []

    # Instruksi sistem untuk AI
    system_prompt = (
        "You are an expert assistant that extracts actionable tasks from meeting notes. "
        "Your goal is to return a clean list of tasks. "
        "Each task should be a concise string. "
        "You MUST respond with a JSON object containing a key 'tasks' which is a list of strings."
    )

    user_prompt = f"Extract all action items from the following text:\n\n{text}"

    try:
        response = chat(
            model="llama3.1:8b", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format="json",
            options={"temperature": 0} # 0 agar jawaban lebih konsisten dan tidak ngasal
        )

        content = response.message.content
        data = json.loads(content)
        
        extracted_tasks = data.get("tasks", [])
        
        if isinstance(extracted_tasks, list):
            return [str(task).strip() for task in extracted_tasks]
        return []

    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return extract_action_items(text)

def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    imperative_starters = {
        "add", "create", "implement", "fix", "update", "write", 
        "check", "verify", "refactor", "document", "design", "investigate",
    }
    return first.lower() in imperative_starters