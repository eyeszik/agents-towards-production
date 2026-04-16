import pytest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prompt_manipulation_tools import (
    prompt_encoder,
    atbash_encode,
    caesar_encode,
    vigenere_encode,
    braille_encode,
    morse_encode,
    pig_latin_encode,
    leet_encode,
    binary_encode,
    hex_encode,
    base64_encode,
    rot13_encode,
    reverse_encode
)

def test_atbash_encode():
    assert atbash_encode("hello") == "svool"
    assert atbash_encode("abcdefghijklmnopqrstuvwxyz") == "zyxwvutsrqponmlkjihgfedcba"

def test_caesar_encode():
    assert caesar_encode("hello", 3) == "khoor"
    assert caesar_encode("xyz", 3) == "abc"
    assert caesar_encode("hello", 0) == "hello"

def test_vigenere_encode():
    assert vigenere_encode("hello", "key") == "rijvs"
    # Testing non-alphabetic characters
    assert vigenere_encode("hello world", "key") == "rijvs gspvh"
    assert vigenere_encode("HELLO", "key") == "rijvs" # Should convert to lower

def test_braille_encode():
    assert braille_encode("hi") == "⠓⠊"
    assert braille_encode("HI") == "⠓⠊"
    assert braille_encode("123") == "123" # Non-alphabetic should be unchanged

def test_morse_encode():
    assert morse_encode("sos") == "...---..."
    assert morse_encode("hello") == "......-...-..---"
    assert morse_encode("123") == "123" # Non-alphabetic should be unchanged

def test_pig_latin_encode():
    assert pig_latin_encode("hello") == "ellohay"
    assert pig_latin_encode("apple") == "appleyay"
    assert pig_latin_encode("hello apple") == "ellohay appleyay"

def test_leet_encode():
    assert leet_encode("hello") == "#3|_|_0"
    assert leet_encode("leet") == "|_33+"
    assert leet_encode("123") == "123" # Non-alphabetic

def test_binary_encode():
    assert binary_encode("hi") == "01101000 01101001"
    assert binary_encode("A") == "01000001"

def test_hex_encode():
    assert hex_encode("hi") == "68 69"
    assert hex_encode("A") == "41"

def test_base64_encode():
    assert base64_encode("hello") == "aGVsbG8="
    assert base64_encode("hello world") == "aGVsbG8gd29ybGQ="

def test_rot13_encode():
    assert rot13_encode("hello") == "uryyb"
    assert rot13_encode("uryyb") == "hello"
    assert rot13_encode("HELLO") == "URYYB"

def test_reverse_encode():
    assert reverse_encode("hello") == "olleh"
    assert reverse_encode("12345") == "54321"

def test_prompt_encoder_specific_encoding():
    assert prompt_encoder("hello", "reverse") == "olleh"
    assert prompt_encoder("hello", "base64") == "aGVsbG8="
    assert prompt_encoder("hello", "rot13") == "uryyb"

def test_prompt_encoder_unsupported_encoding():
    with pytest.raises(ValueError, match="Unsupported encoding type."):
        prompt_encoder("hello", "unknown_encoding")

@patch("random.choice")
def test_prompt_encoder_random_encoding(mock_choice):
    # Mock the random choice to return 'reverse'
    mock_choice.return_value = "reverse"

    # Should use 'reverse' encoding since no encoding is provided
    result = prompt_encoder("hello")
    assert result == "olleh"
    mock_choice.assert_called_once()

def test_prompt_encoder_all_encodings():
    """Test that prompt_encoder can route to all supported encodings"""
    assert prompt_encoder("hello", "atbash") == "svool"
    assert prompt_encoder("hello", "caesar") == "khoor"
    assert prompt_encoder("hello", "vigenere") == "rijvs"
    assert prompt_encoder("hi", "braille") == "⠓⠊"
    assert prompt_encoder("sos", "morse") == "...---..."
    assert prompt_encoder("hello", "pig_latin") == "ellohay"
    assert prompt_encoder("hello", "leet") == "#3|_|_0"
    assert prompt_encoder("hi", "binary") == "01101000 01101001"
    assert prompt_encoder("hi", "hex") == "68 69"
    # base64, rot13, reverse are already tested in test_prompt_encoder_specific_encoding
