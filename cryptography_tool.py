"""
Cryptography Tool
=================
Three cipher methods:
  1. Caesar Cipher       — substitution (shift)
  2. Vigenère Cipher     — polyalphabetic substitution
  3. XOR Cipher          — bitwise XOR + Base64
"""

import base64


# ──────────────────────────────────────────────
# 1. CAESAR CIPHER
# ──────────────────────────────────────────────

def caesar_encode(text: str, shift: int) -> str:
    """Shift every letter forward by `shift` positions."""
    shift = shift % 26
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif ch.islower():
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decode(text: str, shift: int) -> str:
    """Reverse a Caesar encoding by shifting back."""
    return caesar_encode(text, -shift)


# ──────────────────────────────────────────────
# 2. VIGENÈRE CIPHER
# ──────────────────────────────────────────────

def _clean_key(key: str) -> str:
    """Keep only alphabetic characters and uppercase them."""
    cleaned = ''.join(ch for ch in key if ch.isalpha()).upper()
    if not cleaned:
        raise ValueError("Vigenère key must contain at least one letter.")
    return cleaned


def vigenere_encode(text: str, key: str) -> str:
    """Encrypt text using the Vigenère cipher."""
    key = _clean_key(key)
    result = []
    ki = 0  # key index (advances only on alphabetic chars)
    for ch in text:
        if ch.isupper():
            shift = ord(key[ki % len(key)]) - ord('A')
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            ki += 1
        elif ch.islower():
            shift = ord(key[ki % len(key)]) - ord('A')
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)


def vigenere_decode(text: str, key: str) -> str:
    """Decrypt text encoded with the Vigenère cipher."""
    key = _clean_key(key)
    result = []
    ki = 0
    for ch in text:
        if ch.isupper():
            shift = ord(key[ki % len(key)]) - ord('A')
            result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
            ki += 1
        elif ch.islower():
            shift = ord(key[ki % len(key)]) - ord('A')
            result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)


# ──────────────────────────────────────────────
# 3. XOR CIPHER
# ──────────────────────────────────────────────

def xor_encode(text: str, key: str) -> str:
    """XOR every byte of text with the repeating key, return Base64 string."""
    if not key:
        raise ValueError("XOR key cannot be empty.")
    text_bytes = text.encode('utf-8')
    key_bytes  = key.encode('utf-8')
    xored = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes))
    return base64.b64encode(xored).decode('ascii')


def xor_decode(encoded: str, key: str) -> str:
    """Decode a Base64 XOR-encoded string back to plaintext."""
    if not key:
        raise ValueError("XOR key cannot be empty.")
    try:
        raw = base64.b64decode(encoded.strip())
    except Exception:
        raise ValueError("Invalid Base64 input — paste the encoded text to decode.")
    key_bytes = key.encode('utf-8')
    xored = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw))
    return xored.decode('utf-8')


# ──────────────────────────────────────────────
# INTERACTIVE CLI
# ──────────────────────────────────────────────

METHODS = {
    '1': 'Caesar',
    '2': 'Vigenère',
    '3': 'XOR',
}

DESCRIPTIONS = {
    'Caesar':   'Shifts each letter by a fixed number (1–25). Non-letters unchanged.',
    'Vigenère': 'Polyalphabetic substitution using a keyword (letters only).',
    'XOR':      'Bitwise XOR with a repeating key. Output is Base64-encoded.',
}


def print_banner():
    print("\n" + "═" * 52)
    print("  CRYPTOGRAPHY TOOL  |  3 Cipher Methods")
    print("═" * 52)


def choose_method() -> str:
    print("\n  Select cipher method:")
    for k, v in METHODS.items():
        print(f"    [{k}] {v:12s}  — {DESCRIPTIONS[v]}")
    while True:
        choice = input("\n  Your choice (1/2/3): ").strip()
        if choice in METHODS:
            return METHODS[choice]
        print("  ✗ Enter 1, 2, or 3.")


def choose_mode() -> str:
    print("\n  Mode:")
    print("    [E] Encode")
    print("    [D] Decode")
    while True:
        mode = input("\n  Your choice (E/D): ").strip().upper()
        if mode in ('E', 'D'):
            return mode
        print("  ✗ Enter E or D.")


def get_key(method: str) -> object:
    if method == 'Caesar':
        while True:
            raw = input("  Shift value (1–25): ").strip()
            try:
                shift = int(raw)
                if 1 <= shift <= 25:
                    return shift
                print("  ✗ Shift must be between 1 and 25.")
            except ValueError:
                print("  ✗ Enter a whole number.")
    else:
        while True:
            key = input("  Secret key: ").strip()
            if key:
                if method == 'Vigenère' and not any(c.isalpha() for c in key):
                    print("  ✗ Vigenère key must contain at least one letter.")
                else:
                    return key
            else:
                print("  ✗ Key cannot be empty.")


def run():
    print_banner()

    while True:
        method = choose_method()
        mode   = choose_mode()
        key    = get_key(method)
        text   = input("  Text: ")

        print()
        try:
            if method == 'Caesar':
                output = caesar_encode(text, key) if mode == 'E' else caesar_decode(text, key)
            elif method == 'Vigenère':
                output = vigenere_encode(text, key) if mode == 'E' else vigenere_decode(text, key)
            else:
                output = xor_encode(text, key) if mode == 'E' else xor_decode(text, key)

            label = "Encoded" if mode == 'E' else "Decoded"
            print(f"  ┌─ {method} {label} {'─' * (40 - len(method) - len(label))}")
            print(f"  │  {output}")
            print(f"  └{'─' * 48}")

        except ValueError as e:
            print(f"  ✗ Error: {e}")

        again = input("\n  Try another? (Y/N): ").strip().upper()
        if again != 'Y':
            print("\n  Goodbye.\n")
            break


# ──────────────────────────────────────────────
# QUICK DEMO  (runs when executed directly)
# ──────────────────────────────────────────────

def demo():
    print("\n" + "═" * 52)
    print("  QUICK DEMO")
    print("═" * 52)

    # Caesar
    msg = "Hello, World!"
    enc = caesar_encode(msg, 13)
    dec = caesar_decode(enc, 13)
    print(f"\n  Caesar (shift=13)")
    print(f"    Original : {msg}")
    print(f"    Encoded  : {enc}")
    print(f"    Decoded  : {dec}")

    # Vigenère
    key = "SECRET"
    enc = vigenere_encode(msg, key)
    dec = vigenere_decode(enc, key)
    print(f"\n  Vigenère (key='{key}')")
    print(f"    Original : {msg}")
    print(f"    Encoded  : {enc}")
    print(f"    Decoded  : {dec}")

    # XOR
    key = "MyKey123"
    enc = xor_encode(msg, key)
    dec = xor_decode(enc, key)
    print(f"\n  XOR (key='{key}')")
    print(f"    Original : {msg}")
    print(f"    Encoded  : {enc}")
    print(f"    Decoded  : {dec}")

    print("\n" + "═" * 52)


if __name__ == '__main__':
    import sys
    if '--demo' in sys.argv:
        demo()
    else:
        run()