import os
import pytest
# import kedua fungsi agar dua-duanya dites
from ..app.services.extract import extract_action_items, extract_action_items_llm

def test_extract_bullets_and_checkboxes():
    """Tes asli dari folder tugas (Heuristics)."""
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items

def test_extract_llm_basic():
    """TODO 2: Mengetes fungsi ekstraksi berbasis AI (LLM)."""
    text = "Please fix the login bug and update the documentation."
    # Memanggil fungsi LLM baru
    items = extract_action_items_llm(text)
    
    # Memastikan hasilnya tidak kosong dan mengandung kata kunci penting
    assert len(items) >= 2
    assert any("fix" in item.lower() for item in items)
    assert any("documentation" in item.lower() for item in items)

def test_extract_llm_empty():
    """TODO 2: Mengetes AI dengan input kosong."""
    items = extract_action_items_llm("")
    assert items == []