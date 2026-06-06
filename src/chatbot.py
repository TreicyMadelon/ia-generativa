import csv
import logging
from src.preprocess import tokenize_for_bow
from src.vectorizer import LocalVectorizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatLitera")

# Palavras-chave que indicam conteúdo fora do domínio literário
OUT_OF_SCOPE_KEYWORDS = [
    'crime', 'assassinato', 'matar', 'droga', 'tráfico',
    'política', 'partido', 'eleição', 'futebol', 'esporte',
    'economia', 'investimento', 'ação', 'bolsa de valores',
    'namorado', 'relacionamento', 'receita', 'culinária',
]


class ChatLitera:
    def __init__(self, csv_path: str, similarity_threshold: float = 0.2):
        self.csv_path = csv_path
        self.threshold = similarity_threshold
        self.user_inputs: list = []        # textos originais (para debug/log)
        self.processed_inputs: list = []   # versões tokenizadas
        self.responses: list = []
        self._load_data()
        self.vectorizer = LocalVectorizer(self.processed_inputs)

    def _load_data(self):
        """Carrega o CSV e pré-processa os user_inputs."""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_input = row['user_input'].strip()
                response = row['response'].strip()
                if user_input and response:
                    self.user_inputs.append(user_input)
                    self.processed_inputs.append(tokenize_for_bow(user_input))
                    self.responses.append(response)
        logger.info(f"Carregadas {len(self.responses)} interações do dataset.")

    def _is_out_of_scope(self, message: str) -> bool:
        """Detecta rapidamente perguntas fora do domínio literário."""
        msg_lower = message.lower()
        return any(kw in msg_lower for kw in OUT_OF_SCOPE_KEYWORDS)

    def get_response(self, user_message: str) -> str:
        """
        Processa a mensagem do usuário e retorna a resposta mais adequada.

        Fluxo:
            1. Filtro de conteúdo fora do escopo.
            2. Vetorização e busca por similaridade de cosseno.
            3. Se score >= threshold -> devolve resposta do CSV.
            4. Se não -> mensagem de afunilamento pedindo mais detalhes.
        """
        if not user_message.strip():
            return "Por favor, envie uma mensagem para que eu possa ajudar!"

        if self._is_out_of_scope(user_message):
            return (
                "Desculpe, sou especializado apenas em feiras literárias brasileiras. "
                "Posso ajudar com informações sobre eventos, autores, datas, programação, "
                "ingressos e curiosidades literárias do Brasil."
            )

        processed_query = tokenize_for_bow(user_message)
        best_idx, score = self.vectorizer.get_most_similar(processed_query, self.threshold)

        logger.debug(f"Query processada: '{processed_query}' | Score: {score:.4f} | Idx: {best_idx}")

        if best_idx == -1:
            return (
                "Hmm, não entendi bem. Você pode me perguntar sobre:\n"
                "Datas e edições de feiras\n"
                "Locais e cidades\n"
                "Autores participantes\n"
                "Ingressos e preços\n"
                "Programação e atividades\n\n"
                "Exemplo: 'Quando é a Bienal do Rio?' ou 'Quanto custa o ingresso da FLIP?'"
            )

        return self.responses[best_idx]
