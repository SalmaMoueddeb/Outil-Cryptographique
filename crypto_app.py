"""
Cryptography Tool — Streamlit Interface
=======================================
Run with:  streamlit run crypto_app.py
"""

import base64
import streamlit as st

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Outil Cryptographique",
    page_icon="🔐",
    layout="centered",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Header */
  .crypto-header {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
  }
  .crypto-header h1 {
    font-family: 'Space Mono', monospace;
    color: #e8e8f0;
    font-size: 1.7rem;
    margin: 0 0 0.3rem 0;
    letter-spacing: 0.02em;
  }
  .crypto-header p {
    color: #8888aa;
    font-size: 0.85rem;
    margin: 0;
    font-family: 'Space Mono', monospace;
  }

  /* Method cards */
  .method-card {
    background: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #aaaacc;
    line-height: 1.7;
  }
  .method-card .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-left: 8px;
    vertical-align: middle;
  }
  .badge-sub  { background: #1a2e4a; color: #66aaee; border: 1px solid #2a4a7a; }
  .badge-poly { background: #1a3020; color: #66cc88; border: 1px solid #2a5030; }
  .badge-xor  { background: #3a2010; color: #ee9933; border: 1px solid #6a4010; }

  /* Output box */
  .output-box {
    background: #0a0a14;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #88ffcc;
    word-break: break-all;
    line-height: 1.7;
    min-height: 80px;
  }
  .output-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #555577;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }

  /* Steps box */
  .steps-box {
    background: #0d0d1c;
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #334;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #7777aa;
    line-height: 1.9;
  }
  .steps-title {
    color: #4444aa;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }

  /* Error box */
  .error-box {
    background: #1a0808;
    border: 1px solid #5a1a1a;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #ee5555;
  }

  /* Streamlit overrides */
  .stRadio > div { gap: 0.5rem; }
  .stRadio label { font-family: 'Space Mono', monospace; font-size: 0.85rem; }
  .stTextArea textarea, .stTextInput input, .stNumberInput input {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    background: #0f0f1a !important;
    color: #ddddee !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
  }
  .stButton > button {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.06em;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.15);
    background: #1a1a2e;
    color: #ccccee;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
  }
  .stButton > button:hover {
    background: #2a2a4e;
    border-color: rgba(255,255,255,0.3);
    color: #ffffff;
  }
  div[data-testid="stSelectbox"] label,
  div[data-testid="stRadio"] label,
  .stMarkdown p { color: #aaaacc; }

  /* Hide Streamlit branding */
  #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# CIPHER FUNCTIONS
# ──────────────────────────────────────────────

def caesar_encode(text: str, shift: int) -> tuple[str, list[str]]:
    shift = shift % 26
    result, steps = [], []
    for i, ch in enumerate(text):
        if ch.isupper():
            nc = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            if len(steps) < 4:
                steps.append(f"'{ch}' ({ord(ch)-65}) + {shift} mod 26 → '{nc}'")
            result.append(nc)
        elif ch.islower():
            nc = chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
            if len(steps) < 4:
                steps.append(f"'{ch}' ({ord(ch)-97}) + {shift} mod 26 → '{nc}'")
            result.append(nc)
        else:
            result.append(ch)
    if len(text) > 4:
        steps.append(f"... et {len(text) - 4} caractères supplémentaires traités")
    return ''.join(result), steps


def caesar_decode(text: str, shift: int) -> tuple[str, list[str]]:
    return caesar_encode(text, -shift)


def _clean_key(key: str) -> str:
    cleaned = ''.join(ch for ch in key if ch.isalpha()).upper()
    if not cleaned:
        raise ValueError("La clé doit contenir au moins une lettre.")
    return cleaned


def vigenere_encode(text: str, key: str) -> tuple[str, list[str]]:
    key = _clean_key(key)
    result, steps, ki = [], [], 0
    for ch in text:
        if ch.isupper():
            s = ord(key[ki % len(key)]) - ord('A')
            nc = chr((ord(ch) - ord('A') + s) % 26 + ord('A'))
            if len(steps) < 4:
                steps.append(f"'{ch}' + clé[{ki % len(key)}]='{key[ki % len(key)]}'({s}) → '{nc}'")
            result.append(nc)
            ki += 1
        elif ch.islower():
            s = ord(key[ki % len(key)]) - ord('A')
            nc = chr((ord(ch) - ord('a') + s) % 26 + ord('a'))
            if len(steps) < 4:
                steps.append(f"'{ch}' + clé[{ki % len(key)}]='{key[ki % len(key)]}'({s}) → '{nc}'")
            result.append(nc)
            ki += 1
        else:
            result.append(ch)
    steps.append(f"Clé '{key}' répétée cycliquement sur toutes les lettres")
    return ''.join(result), steps


def vigenere_decode(text: str, key: str) -> tuple[str, list[str]]:
    key = _clean_key(key)
    result, steps, ki = [], [], 0
    for ch in text:
        if ch.isupper():
            s = ord(key[ki % len(key)]) - ord('A')
            nc = chr((ord(ch) - ord('A') - s) % 26 + ord('A'))
            if len(steps) < 4:
                steps.append(f"'{ch}' - clé[{ki % len(key)}]='{key[ki % len(key)]}'({s}) → '{nc}'")
            result.append(nc)
            ki += 1
        elif ch.islower():
            s = ord(key[ki % len(key)]) - ord('A')
            nc = chr((ord(ch) - ord('a') - s) % 26 + ord('a'))
            if len(steps) < 4:
                steps.append(f"'{ch}' - clé[{ki % len(key)}]='{key[ki % len(key)]}'({s}) → '{nc}'")
            result.append(nc)
            ki += 1
        else:
            result.append(ch)
    steps.append(f"Clé '{key}' inversée cycliquement pour annuler le chiffrement")
    return ''.join(result), steps


def xor_encode(text: str, key: str) -> tuple[str, list[str]]:
    if not key:
        raise ValueError("La clé ne peut pas être vide.")
    tb = text.encode('utf-8')
    kb = key.encode('utf-8')
    xored = bytes(b ^ kb[i % len(kb)] for i, b in enumerate(tb))
    steps = [
        f"octet[{i}] 0x{tb[i]:02x} XOR 0x{kb[i % len(kb)]:02x} = 0x{xored[i]:02x}"
        for i in range(min(4, len(tb)))
    ]
    if len(tb) > 4:
        steps.append("... résultat encodé en Base64 pour un affichage sûr")
    return base64.b64encode(xored).decode('ascii'), steps


def xor_decode(encoded: str, key: str) -> tuple[str, list[str]]:
    if not key:
        raise ValueError("La clé ne peut pas être vide.")
    try:
        raw = base64.b64decode(encoded.strip())
    except Exception:
        raise ValueError("Base64 invalide — collez le texte chiffré pour le déchiffrer.")
    kb = key.encode('utf-8')
    xored = bytes(b ^ kb[i % len(kb)] for i, b in enumerate(raw))
    steps = [
        f"octet[{i}] 0x{raw[i]:02x} XOR 0x{kb[i % len(kb)]:02x} = 0x{xored[i]:02x}"
        for i in range(min(4, len(raw)))
    ]
    steps.append("Le XOR est sa propre inverse — la même clé et opération annule le chiffrement")
    return xored.decode('utf-8'), steps


# ──────────────────────────────────────────────
# UI
# ──────────────────────────────────────────────

# Header
st.markdown("""
<div class="crypto-header">
  <h1>🔐 Outil Cryptographique</h1>
  <p>// chiffrer &amp; déchiffrer avec trois méthodes de cryptographie classique</p>
</div>
""", unsafe_allow_html=True)

# Method selection
METHOD_LABELS = {
    "Chiffre de César":    ("SUB",  "badge-sub",  "Décale chaque lettre d'un nombre fixe dans l'alphabet. Les caractères non alphabétiques restent inchangés. Simple à comprendre, facile à casser sans la clé."),
    "Chiffre de Vigenère": ("POLY", "badge-poly", "Utilise un mot-clé répété pour appliquer des décalages variables — bien plus difficile à casser que César."),
    "Chiffre XOR":         ("BIT",  "badge-xor",  "XOR bit à bit de chaque octet avec la clé répétée. La sortie est encodée en Base64. Fonctionne sur n'importe quel texte."),
}

method = st.selectbox("**Méthode de chiffrement**", list(METHOD_LABELS.keys()), label_visibility="visible")
badge_text, badge_cls, desc = METHOD_LABELS[method]

st.markdown(f"""
<div class="method-card">
  <strong style="color:#ccccee; font-size:0.85rem;">{method}</strong>
  <span class="badge {badge_cls}">{badge_text}</span><br/>
  {desc}
</div>
""", unsafe_allow_html=True)

# Saisie de la clé
st.markdown("**Clé / paramètres**")
col_key, col_mode = st.columns([2, 1])

with col_key:
    if method == "Chiffre de César":
        shift = st.number_input("Décalage (1–25)", min_value=1, max_value=25, value=3, step=1)
        key_val = shift
    else:
        key_val = st.text_input(
            "Clé secrète",
            placeholder="ex. SECRET" if method == "Chiffre de Vigenère" else "ex. MaCle123",
            type="password",
        )

with col_mode:
    mode = st.radio("Mode", ["Chiffrer", "Déchiffrer"], horizontal=False)

# Zone de texte
st.markdown("**Texte à traiter**")
input_text = st.text_area("", placeholder="Saisissez votre message ici...", height=130, label_visibility="collapsed")

# Boutons
col_a, col_b, col_c = st.columns([1, 1, 2])
run_btn   = col_a.button("[ LANCER ]", use_container_width=True)
clear_btn = col_b.button("[ EFFACER ]", use_container_width=True)

if clear_btn:
    st.session_state["output"] = ""
    st.session_state["steps"]  = []
    st.session_state["error"]  = ""

# Process
if run_btn:
    st.session_state.setdefault("output", "")
    st.session_state.setdefault("steps", [])
    st.session_state.setdefault("error", "")

    if not input_text.strip():
        st.session_state["error"]  = "Veuillez saisir un texte avant de continuer."
        st.session_state["output"] = ""
        st.session_state["steps"]  = []
    elif method != "Chiffre de César" and not key_val:
        st.session_state["error"]  = "Veuillez entrer une clé secrète."
        st.session_state["output"] = ""
        st.session_state["steps"]  = []
    else:
        try:
            encode = (mode == "Chiffrer")
            if method == "Chiffre de César":
                fn = caesar_encode if encode else caesar_decode
                out, steps = fn(input_text, int(key_val))
            elif method == "Chiffre de Vigenère":
                fn = vigenere_encode if encode else vigenere_decode
                out, steps = fn(input_text, key_val)
            else:
                fn = xor_encode if encode else xor_decode
                out, steps = fn(input_text, key_val)

            st.session_state["output"] = out
            st.session_state["steps"]  = steps
            st.session_state["error"]  = ""
        except ValueError as e:
            st.session_state["error"]  = str(e)
            st.session_state["output"] = ""
            st.session_state["steps"]  = []

# Output display
st.markdown("---")
output = st.session_state.get("output", "")
error  = st.session_state.get("error",  "")
steps  = st.session_state.get("steps",  [])

if error:
    st.markdown(f'<div class="error-box">✗ {error}</div>', unsafe_allow_html=True)

if output:
    label = "RÉSULTAT CHIFFRÉ" if mode == "Chiffrer" else "RÉSULTAT DÉCHIFFRÉ"
    st.markdown(f'<div class="output-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{output}</div>', unsafe_allow_html=True)
    st.code(output, language=None)   # provides the native copy button
    st.caption("👆 Utilisez le bouton copier ci-dessus pour récupérer le résultat.")

    if steps:
        steps_html = "".join(
            f"<div><span style='color:#334488;min-width:20px;display:inline-block'>{i+1}.</span> {s}</div>"
            for i, s in enumerate(steps)
        )
        st.markdown(f"""
        <div class="steps-box">
          <div class="steps-title">// comment ça a fonctionné</div>
          {steps_html}
        </div>
        """, unsafe_allow_html=True)

# ── Pied de page ──
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-family: Space Mono, monospace; "
    "font-size:0.7rem; color:#44445a;'>"
    "César · Vigenère · XOR &nbsp;|&nbsp; tout le traitement est local — rien ne quitte votre machine"
    "</p>",
    unsafe_allow_html=True,
)