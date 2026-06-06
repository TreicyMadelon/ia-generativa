# ChatLitera 
### Chatbot Local sobre Feiras Literárias Brasileiras

---

## Descrição

O **ChatLitera** é um chatbot que responde perguntas sobre as principais feiras literárias do Brasil — como datas, locais, programação, ingressos e autores participantes — usando apenas um arquivo CSV e similaridade por cosseno (Bag-of-Words).

Roda **completamente offline**, sem necessidade de API externa, GPU ou conexão à internet.

---

## Feiras Cobertas

| Feira | Cidade | Período |
|-------|--------|---------|
| Bienal Internacional do Livro de SP | São Paulo (SP) | Julho |
| Bienal do Rio de Janeiro | Rio de Janeiro (RJ) | Setembro |
| FLIP – Festa Literária Internacional de Paraty | Paraty (RJ) | Julho/Agosto |
| FLIC – Festa Literária de Belo Horizonte | Belo Horizonte (MG) | Junho |
| Festa Literária de Porto Alegre | Porto Alegre (RS) | Novembro |
| Feira do Livro de Porto Alegre | Porto Alegre (RS) | Out./Nov. |
| FLOR – Feira Literária do Orgulho e Resistência | São Paulo (SP) | Junho |
| Bienal do Livro Bahia | Salvador (BA) | Outubro |
| Bienal Internacional do Livro de Pernambuco | Recife (PE) | Outubro |
| Feira do Livro da Unesp | São Paulo (SP) | Outubro |
| Flipoços – Festa Literária de Poços de Caldas | Poços de Caldas (MG) | Agosto |
| Festival Literário Catarinense | Florianópolis (SC) | Setembro |

---

## Requisitos

- Python 3.8 ou superior

---

## Instalação e Uso

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Gere o dataset (necessário apenas na primeira execução)

```bash
python src/generate_dataset.py
```

Isso cria o arquivo `data/feiras_literarias.csv` com ~1000 interações.

### 3. Execute o chatbot

```bash
python main.py
```

---

## Estrutura do Projeto

```
chatbot-local/
├── data/
│   └── feiras_literarias.csv      # Base de conhecimento (gerada pelo script)
├── src/
│   ├── __init__.py
│   ├── preprocess.py              # Normalização de texto e substituição de entidades
│   ├── vectorizer.py              # Bag-of-Words (CountVectorizer) e similaridade de cosseno
│   ├── chatbot.py                 # Classe principal ChatLitera
│   └── generate_dataset.py        # Gerador do CSV com ~1000 interações
├── requirements.txt
├── README.md
└── main.py                        # Ponto de entrada (interface terminal)
```

---

## Como Funciona

### Abordagem Técnica

1. **Pré-processamento**: remove acentos, pontuação e converte entidades multi-palavra como `"Bienal do Livro"` em tokens únicos (`BIENAL_DO_LIVRO`), garantindo que sejam tratados como uma unidade.

2. **Bag-of-Words com bigramas**: cada frase é transformada em um vetor numérico de frequência de palavras (e pares de palavras adjacentes).

3. **Similaridade de Cosseno**: a pergunta do usuário é vetorizada e comparada com todos os exemplos do CSV. A frase mais próxima (ângulo menor) tem sua resposta devolvida.

4. **Threshold (limiar)**: só aceita similaridade ≥ 0.2; caso contrário, o bot pede mais detalhes ao usuário.

### Fluxo da Resposta

```
Usuário digita mensagem
        ↓
Filtro de conteúdo fora do escopo?
   Sim → resposta de redirecionamento
   Não ↓
Pré-processamento + vetorização
        ↓
Busca por similaridade de cosseno
        ↓
Score ≥ 0.2? 
   Sim → retorna resposta do CSV
   Não → mensagem de afunilamento
```

---

## Exemplo de Uso

```
 ChatLitera – Feiras Literárias Brasileiras 

Você: Quando é a FLIP?
ChatLitera: A FLIP – Festa Literária Internacional de Paraty é realizada 
geralmente em julho/agosto. Para as datas exatas desta edição, 
consulte www.flip.org.br. 

Você: Quanto custa o ingresso da Bienal do Rio?
ChatLitera: Os preços dos ingressos da Bienal do Rio de Janeiro variam a cada 
edição. Em geral, há ingressos simbólicos (a partir de R$ 20,00) e costumam 
existir dias ou atividades de entrada gratuita. Verifique em www.bienaldorio.com.br 

Você: sair
ChatLitera: Até logo! Continue participando das feiras literárias! 
```

---

## Licença

MIT — livre para uso, modificação e distribuição.
