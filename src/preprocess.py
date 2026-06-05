import re
from unidecode import unidecode

# ---------------------------------------------------------------------------
# Aliases: normaliza variações coloquiais ANTES da substituição de entidades.
# Cada tupla é (regex_pattern, replacement_normalizado).
# A ordem importa: padrões mais específicos primeiro.
# ---------------------------------------------------------------------------
ALIASES = [
    # "Bienal do Livro do Rio [de Janeiro]" → "bienal do rio de janeiro"
    (r'\bbienal(?: internacional)? do livro do rio(?: de janeiro)?\b',
     'bienal do rio de janeiro'),
    # "Bienal do Rio" sem "livro" já é tratada pelas entidades
    # "Bienal do Livro de SP / São Paulo" → "bienal do livro de sao paulo"
    (r'\bbienal(?: internacional)? do livro (?:de )?s[aã]o paulo\b',
     'bienal do livro de sao paulo'),
    (r'\bbienal(?: internacional)? do livro sp\b',
     'bienal do livro de sao paulo'),
    # "Bienal do Livro da Bahia / Bahia" → "bienal do livro bahia"
    (r'\bbienal(?: internacional)? do livro (?:da )?bahia\b',
     'bienal do livro bahia'),
    # "Bienal do Livro de Pernambuco / PE" → "bienal internacional do livro de pernambuco"
    (r'\bbienal(?: internacional)? do livro (?:de )?pernambuco\b',
     'bienal internacional do livro de pernambuco'),
    (r'\bbienal(?: internacional)? do livro pe\b',
     'bienal internacional do livro de pernambuco'),
    # "Bienal de SP" / "Bienal de São Paulo" (sem "livro")
    (r'\bbienal (?:de )?s[aã]o paulo\b',
     'bienal do livro de sao paulo'),
    (r'\bbienal de sp\b',
     'bienal do livro de sao paulo'),
]

# Lista de entidades multi-palavra que devem virar um único token
MULTI_WORD_ENTITIES = [
    "bienal internacional do livro de sao paulo",
    "bienal internacional do livro de pernambuco",
    "bienal internacional do livro",
    "bienal do livro de sao paulo",
    "bienal do livro bahia",
    "bienal do livro",
    "festa literaria internacional de paraty",
    "festa literaria de paraty",
    "festa literaria de belo horizonte",
    "festa literaria de porto alegre",
    "feira literaria do orgulho e resistencia",
    "feira do livro de porto alegre",
    "feira do livro da unesp",
    "festival literario catarinense",
    "flipocos",
    "flip",
    "flic",
    "flor",
    "jose de alencar",
    "machado de assis",
    "clarice lispector",
    "jorge amado",
    "cora coralina",
    "guimaraes rosa",
    "graciliano ramos",
    "lygia fagundes telles",
    "ariano suassuna",
    "milton hatoum",
    "conceicao evaristo",
    "ailton krenak",
    "djamila ribeiro",
    "itamar vieira junior",
    "bienal do rio de janeiro",
    "bienal do rio",
    "camara brasileira do livro",
]

# Mapeamento: frase original (já normalizada) -> token único (sem espaços)
ENTITY_TO_TOKEN = {ent: ent.replace(" ", "_").upper() for ent in MULTI_WORD_ENTITIES}


def normalize_text(text: str) -> str:
    """Converte para minúsculas, remove acentos e pontuação simples."""
    text = text.lower()
    text = unidecode(text)          # remove acentos
    text = re.sub(r'[^\w\s]', ' ', text)  # pontuação vira espaço
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def apply_aliases(text: str) -> str:
    """Normaliza variações coloquiais antes da substituição de entidades."""
    for pattern, replacement in ALIASES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def replace_entities(text: str) -> str:
    """Substitui entidades multi-palavra por tokens únicos (após normalização)."""
    text = normalize_text(text)
    text = apply_aliases(text)        # ← aliases aplicados APÓS normalização
    # Ordena por tamanho decrescente para substituir as frases mais longas primeiro
    for phrase in sorted(ENTITY_TO_TOKEN.keys(), key=len, reverse=True):
        token = ENTITY_TO_TOKEN[phrase]
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b')
        text = pattern.sub(token, text)
    return text


def tokenize_for_bow(text: str) -> str:
    """Aplica substituição de entidades e retorna string limpa para o vetorizador."""
    return replace_entities(text)
