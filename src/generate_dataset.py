# src/generate_dataset.py
"""
Gera o arquivo data/feiras_literarias.csv com ~1000 interações sintéticas
cobrindo os principais temas do ChatLitera.

Execute uma única vez antes de iniciar o chatbot:
    python src/generate_dataset.py
"""

import csv
import os
import random

random.seed(42)

# ---------------------------------------------------------------------------
# Dados base
# ---------------------------------------------------------------------------

FEIRAS = [
    {
        "nome": "Bienal Internacional do Livro de São Paulo",
        "sigla": "Bienal do Livro SP",
        "local": "São Paulo (SP) – Pavilhão do Anhembi",
        "endereco": "Av. Olavo Fontoura, 1209 – Santana, São Paulo (SP) – CEP 02012-021 (Pavilhão do Anhembi)",
        "mes": "julho",
        "site": "www.bienaldolivro.com.br",
        "descricao": (
            "um dos maiores eventos literários da América Latina, "
            "reunindo editoras, autores e leitores do mundo inteiro"
        ),
        "homenageados": ["Clarice Lispector", "Jorge Amado", "Ariano Suassuna"],
        "convidados_exemplos": ["Milton Hatoum", "Djamila Ribeiro", "Itamar Vieira Junior",
                                "Ailton Krenak", "Conceição Evaristo"],
    },
    {
        "nome": "Bienal do Rio de Janeiro",
        "sigla": "Bienal Rio",
        "local": "Rio de Janeiro (RJ) – Riocentro",
        "endereco": "Av. Salvador Allende, 6555 – Barra da Tijuca, Rio de Janeiro (RJ) – CEP 22783-127 (Riocentro, Pavilhão 3)",
        "mes": "setembro",
        "site": "www.bienaldorio.com.br",
        "descricao": (
            "um dos eventos mais aguardados do Rio, com lançamentos exclusivos "
            "e encontros com grandes autores brasileiros e internacionais"
        ),
        "homenageados": ["Machado de Assis", "Clarice Lispector", "Graciliano Ramos"],
        "convidados_exemplos": ["Conceição Evaristo", "Djamila Ribeiro", "Milton Hatoum",
                                "Lygia Fagundes Telles", "Ailton Krenak"],
    },
    {
        "nome": "FLIP – Festa Literária Internacional de Paraty",
        "sigla": "FLIP",
        "local": "Paraty (RJ)",
        "endereco": "Praça da Matriz, s/n – Centro Histórico, Paraty (RJ) – CEP 23970-000 (Casa da Cultura de Paraty e espaços do centro histórico)",
        "mes": "julho/agosto",
        "site": "www.flip.org.br",
        "descricao": (
            "um festival intimista e sofisticado realizado na histórica cidade de Paraty, "
            "reconhecido internacionalmente pela qualidade de sua programação"
        ),
        "homenageados": ["Guimarães Rosa", "Cora Coralina", "Lima Barreto",
                         "Hilda Hilst", "Manoel de Barros", "Carlos Drummond de Andrade"],
        "convidados_exemplos": ["Conceição Evaristo", "Djamila Ribeiro", "Ailton Krenak",
                                "Itamar Vieira Junior", "Milton Hatoum", "Lygia Fagundes Telles"],
    },
    {
        "nome": "FLIC – Festa Literária de Belo Horizonte",
        "sigla": "FLIC",
        "local": "Belo Horizonte (MG)",
        "endereco": "Praça da Liberdade, s/n – Funcionários, Belo Horizonte (MG) – CEP 30140-010 (Circuito Liberdade)",
        "mes": "junho",
        "site": "www.flicbh.com.br",
        "descricao": (
            "um festival mineiro com forte identidade cultural, "
            "promovendo debates, oficinas e lançamentos de livros"
        ),
        "homenageados": ["Drummond de Andrade", "Guimarães Rosa", "Conceição Evaristo"],
        "convidados_exemplos": ["Itamar Vieira Junior", "Djamila Ribeiro", "Ailton Krenak",
                                "Milton Hatoum"],
    },
    {
        "nome": "Festa Literária de Porto Alegre",
        "sigla": "Festa Literária POA",
        "local": "Porto Alegre (RS)",
        "endereco": "Usina do Gasômetro – Av. Presidente João Goulart, 551 – Centro Histórico, Porto Alegre (RS) – CEP 90010-310",
        "mes": "novembro",
        "site": "festaliterariaportaalegre.com.br",
        "descricao": (
            "um dos principais eventos literários do Sul do Brasil, "
            "com intensa programação de autores regionais e nacionais"
        ),
        "homenageados": ["Érico Veríssimo", "Moacyr Scliar", "Rubem Braga"],
        "convidados_exemplos": ["Milton Hatoum", "Conceição Evaristo", "Djamila Ribeiro",
                                "Ailton Krenak"],
    },
    {
        "nome": "Feira do Livro de Porto Alegre",
        "sigla": "Feira do Livro POA",
        "local": "Porto Alegre (RS) – Praça da Alfândega",
        "endereco": "Praça da Alfândega, s/n – Centro Histórico, Porto Alegre (RS) – CEP 90010-150",
        "mes": "outubro/novembro",
        "site": "www.feiradolivro.com.br",
        "descricao": (
            "a mais antiga feira literária do Brasil, realizada ao ar livre "
            "na icônica Praça da Alfândega desde 1955"
        ),
        "homenageados": ["Érico Veríssimo", "Moacyr Scliar", "Josué Guimarães",
                         "Lya Luft", "Rubem Alves"],
        "convidados_exemplos": ["Conceição Evaristo", "Ailton Krenak", "Djamila Ribeiro",
                                "Itamar Vieira Junior", "Milton Hatoum"],
    },
    {
        "nome": "FLOR – Feira Literária do Orgulho e Resistência",
        "sigla": "FLOR",
        "local": "São Paulo (SP)",
        "endereco": "Largo do Arouche, s/n – República, São Paulo (SP) – CEP 01219-010 (Largo do Arouche e adjacências)",
        "mes": "junho",
        "site": "www.feiraflor.com.br",
        "descricao": (
            "uma feira literária dedicada a vozes LGBTQIA+, periféricas e de resistência, "
            "celebrando a diversidade e o poder transformador da literatura"
        ),
        "homenageados": ["Caio Fernando Abreu", "Cassandra Rios", "João Silvério Trevisan"],
        "convidados_exemplos": ["Djamila Ribeiro", "Ailton Krenak", "Conceição Evaristo",
                                "Itamar Vieira Junior"],
    },
    {
        "nome": "Bienal do Livro Bahia",
        "sigla": "Bienal Bahia",
        "local": "Salvador (BA) – Centro de Convenções",
        "endereco": "Centro de Convenções da Bahia – Av. Antônio Carlos Magalhães, s/n – Stiep, Salvador (BA) – CEP 41770-019",
        "mes": "outubro",
        "site": "www.bienaldolivrobahia.com.br",
        "descricao": (
            "um dos maiores eventos literários do Nordeste, reunindo autores, editoras "
            "e leitores em Salvador com forte identidade cultural baiana"
        ),
        "homenageados": ["Jorge Amado", "Ariano Suassuna", "Conceição Evaristo"],
        "convidados_exemplos": ["Itamar Vieira Junior", "Djamila Ribeiro", "Ailton Krenak",
                                "Milton Hatoum"],
    },
    {
        "nome": "Bienal Internacional do Livro de Pernambuco",
        "sigla": "Bienal PE",
        "local": "Recife (PE) – Centro de Convenções",
        "endereco": "Centro de Convenções de Pernambuco – Complexo Viário Via Expressa, s/n – Camaragibe (PE) – CEP 54768-000",
        "mes": "outubro",
        "site": "www.bienaldolivrope.com.br",
        "descricao": (
            "um dos grandes festivais do livro no coração do Nordeste, destacando autores "
            "regionais e internacionais com rica programação cultural"
        ),
        "homenageados": ["Ariano Suassuna", "João Cabral de Melo Neto", "Clarice Lispector"],
        "convidados_exemplos": ["Conceição Evaristo", "Itamar Vieira Junior", "Djamila Ribeiro",
                                "Ailton Krenak"],
    },
    {
        "nome": "Feira do Livro da Unesp",
        "sigla": "Feira Unesp",
        "local": "São Paulo (SP) – Campus da Unesp",
        "endereco": "Rua Quirino de Andrade, 215 – Centro, São Paulo (SP) – CEP 01049-010 (Editora Unesp / Livraria da Unesp)",
        "mes": "outubro",
        "site": "www.livraria.unesp.br",
        "descricao": (
            "uma feira acadêmica e literária promovida pela Editora Unesp, "
            "com forte presença de títulos universitários, técnicos e de divulgação científica"
        ),
        "homenageados": ["Mário de Andrade", "Paulo Freire", "Florestan Fernandes"],
        "convidados_exemplos": ["Ailton Krenak", "Djamila Ribeiro", "Milton Hatoum",
                                "Conceição Evaristo"],
    },
    {
        "nome": "Flipoços – Festa Literária de Poços de Caldas",
        "sigla": "Flipoços",
        "local": "Poços de Caldas (MG)",
        "endereco": "Thermas Antonio Carlos – Av. Francisco Salles, 544 – Centro, Poços de Caldas (MG) – CEP 37701-366",
        "mes": "agosto",
        "site": "www.flipocos.com.br",
        "descricao": (
            "um festival literário encantador na cidade das águas, com programação "
            "intimista e diversificada para leitores de todas as idades"
        ),
        "homenageados": ["Guimarães Rosa", "Lygia Fagundes Telles", "Rubem Braga"],
        "convidados_exemplos": ["Milton Hatoum", "Conceição Evaristo", "Djamila Ribeiro",
                                "Itamar Vieira Junior"],
    },
    {
        "nome": "Festival Literário Catarinense",
        "sigla": "Festival Literário SC",
        "local": "Florianópolis (SC)",
        "endereco": "Centro Integrado de Cultura – Av. Irineu Bornhausen, 5600 – Agronômica, Florianópolis (SC) – CEP 88034-100 (CIC Florianópolis)",
        "mes": "setembro",
        "site": "www.festivalliterariosc.com.br",
        "descricao": (
            "um dos principais festivais do Sul do Brasil, celebrando a literatura "
            "catarinense e nacional com debates, lançamentos e oficinas"
        ),
        "homenageados": ["Cruz e Sousa", "Antonieta de Barros", "Salim Miguel"],
        "convidados_exemplos": ["Conceição Evaristo", "Ailton Krenak", "Milton Hatoum",
                                "Djamila Ribeiro"],
    },
]

AUTORES = [
    "Machado de Assis", "Clarice Lispector", "Jorge Amado",
    "José de Alencar", "Cora Coralina", "Guimarães Rosa",
    "Graciliano Ramos", "Lygia Fagundes Telles", "Rubem Braga",
    "Ariano Suassuna", "Milton Hatoum", "Conceição Evaristo",
    "Ailton Krenak", "Djamila Ribeiro", "Itamar Vieira Junior",
]

GENEROS = [
    "romance", "poesia", "conto", "crônica", "literatura infantil",
    "ficção científica", "thriller", "não-ficção", "biografia", "ensaio",
]

# ---------------------------------------------------------------------------
# Templates de perguntas e respostas
# ---------------------------------------------------------------------------

TEMPLATES = [
    # -- Saudações --
    (
        ["oi", "olá", "oi tudo bem", "olá, tudo bem?", "bom dia", "boa tarde",
         "boa noite", "hey", "salve", "eai", "e aí", "opa"],
        "Olá! 📚 Sou o ChatLitera, seu guia sobre feiras literárias brasileiras. "
        "Posso ajudar com datas, locais, programação, ingressos e muito mais. O que você quer saber?",
    ),
    # -- Despedidas --
    (
        ["tchau", "até logo", "até mais", "obrigado tchau", "valeu, tchau",
         "foi ótimo obrigado", "até", "xau", "flw", "falou"],
        "Até logo! 📖 Espero ter ajudado. Continue participando das feiras literárias do Brasil!",
    ),
    # -- Agradecimentos --
    (
        ["obrigado", "obrigada", "valeu", "muito obrigado", "thanks",
         "grato", "grata", "agradeço"],
        "Fico feliz em ajudar! 😊 Se tiver mais dúvidas sobre feiras literárias, é só perguntar.",
    ),
]

# Perguntas dinâmicas (preenchidas com dados das feiras)
DYNAMIC_TEMPLATES = [
    # Datas
    (
        [
            "quando é a {sigla}?",
            "qual a data da {sigla}?",
            "em que mês acontece a {sigla}?",
            "quando vai ser a {sigla} esse ano?",
            "qual o período da {sigla}?",
            "em que época do ano rola a {sigla}?",
            "quais as datas da {nome}?",
            "quando ocorre a {nome}?",
        ],
        "A {nome} geralmente acontece em {mes}. "
        "Para as datas exatas desta edição, consulte {site}. 📅",
    ),
    # Local / Cidade
    (
        [
            "onde fica a {sigla}?",
            "onde acontece a {sigla}?",
            "qual é o local da {sigla}?",
            "em que cidade é a {sigla}?",
            "onde é realizada a {nome}?",
            "qual a cidade da {sigla}?",
            "a {sigla} é em qual cidade?",
        ],
        "A {nome} é realizada em {local}. "
        "Ótima oportunidade para conhecer a cidade também! 📍",
    ),
    # Endereço completo
    (
        [
            "qual o endereço da {sigla}?",
            "qual o endereço da {nome}?",
            "onde exatamente fica a {sigla}?",
            "me dá o endereço da {sigla}",
            "qual o endereço completo da {sigla}?",
            "em que rua fica a {sigla}?",
            "como chegar na {sigla}?",
            "qual o local exato da {sigla}?",
        ],
        "O endereço da {nome} é: {endereco}. "
        "Para informações de transporte e estacionamento, consulte {site}. 🗺️",
    ),
    # O que é
    (
        [
            "o que é a {sigla}?",
            "me fale sobre a {sigla}",
            "me conta sobre a {nome}",
            "o que é a {nome}?",
            "qual a história da {sigla}?",
            "me explica o que é a {sigla}",
            "fala sobre a {sigla}",
        ],
        "A {nome} é {descricao}. "
        "Acesse {site} para mais informações. 📚",
    ),
    # Ingresso
    (
        [
            "quanto custa o ingresso da {sigla}?",
            "qual o preço do ingresso para a {sigla}?",
            "a {sigla} é paga?",
            "precisa pagar para entrar na {sigla}?",
            "tem entrada gratuita na {sigla}?",
            "quanto é o ticket da {sigla}?",
            "a {nome} cobra entrada?",
        ],
        "Os preços dos ingressos da {nome} variam a cada edição. "
        "Em geral, há ingressos simbólicos (a partir de R$ 20,00) e costumam existir dias ou atividades de entrada gratuita. "
        "Verifique os valores atuais em {site}. 🎟️",
    ),
    # Programação
    (
        [
            "qual a programação da {sigla}?",
            "quais as atividades da {sigla}?",
            "o que tem na {sigla}?",
            "quais eventos têm na {sigla}?",
            "o que acontece na {sigla}?",
            "tem bate-papo com autores na {sigla}?",
            "tem oficinas na {sigla}?",
        ],
        "A {nome} costuma oferecer: bate-papos com autores, mesas de debate, "
        "lançamentos de livros, oficinas literárias e espaços para crianças. "
        "A programação completa é divulgada em {site} próximo ao evento. 🎤",
    ),
    # Autores CONVIDADOS (já estiveram no evento)
    (
        [
            "quais autores já foram convidados para a {sigla}?",
            "quem já participou da {sigla}?",
            "quais escritores já estiveram na {sigla}?",
            "quem já foi convidado para a {sigla}?",
            "quais autores participam da {nome}?",
            "quais escritores costumam ir à {sigla}?",
            "me diz autores que já foram na {sigla}",
        ],
        "A {nome} já recebeu como convidados nomes como {conv1}, {conv2} e {conv3}, "
        "entre outros autores brasileiros e internacionais. "
        "Os convidados de cada nova edição são anunciados em {site}. ✍️",
    ),
    # Autores HOMENAGEADOS
    (
        [
            "quem foi homenageado na {sigla}?",
            "quem são os homenageados da {sigla}?",
            "quais autores foram homenageados na {sigla}?",
            "a {sigla} já homenageou quais autores?",
            "quem recebeu homenagem na {nome}?",
            "quais escritores foram homenageados pela {sigla}?",
            "quem é o homenageado da {sigla}?",
        ],
        "A {nome} já prestou homenagem a grandes nomes da literatura, como {hom1}, {hom2} e {hom3}. "
        "O autor ou autora homenageado(a) de cada edição é anunciado(a) em {site}. 🏆",
    ),
    # Importância
    (
        [
            "por que a {sigla} é importante?",
            "qual a importância da {sigla}?",
            "qual o impacto da {sigla}?",
            "por que devo ir à {sigla}?",
            "vale a pena ir na {sigla}?",
        ],
        "A {nome} é fundamental para fomentar a leitura e a cultura no Brasil, "
        "conectando autores, editoras e leitores de todo o país. "
        "É uma experiência enriquecedora para qualquer amante da literatura! 🌟",
    ),
]

# Perguntas gerais (sem feira específica)
GENERAL_QA = [
    (
        "quais são as principais feiras literárias do Brasil?",
        "As principais feiras literárias do Brasil são: Bienal Internacional do Livro de SP, "
        "Bienal do Rio, FLIP (Paraty), FLIC (Belo Horizonte), Festa Literária POA, "
        "Feira do Livro de Porto Alegre, FLOR (São Paulo), Bienal Bahia, Bienal PE (Recife), "
        "Feira Unesp, Flipoços (Poços de Caldas) e Festival Literário Catarinense. "
        "Cada uma tem sua identidade única! 📚",
    ),
    (
        "qual a maior feira literária do Brasil?",
        "A Bienal Internacional do Livro de São Paulo é considerada a maior feira literária do Brasil "
        "e uma das maiores da América Latina, recebendo milhões de visitantes por edição. 🏆",
    ),
    (
        "qual a mais antiga feira literária do Brasil?",
        "A Feira do Livro de Porto Alegre, realizada desde 1955 na Praça da Alfândega, "
        "é a mais antiga feira literária do Brasil. Uma tradição de mais de 60 anos! 🎂",
    ),
    (
        "tem feira literária perto de mim?",
        "Isso depende de onde você mora! As principais feiras acontecem em São Paulo, Rio de Janeiro, "
        "Paraty (RJ), Belo Horizonte (MG) e Porto Alegre (RS). Qual cidade fica mais próxima de você?",
    ),
    (
        "quais feiras literárias têm atividades para crianças?",
        "A maioria das grandes feiras tem espaços dedicados ao público infantil! "
        "Bienal do Livro SP, Bienal Rio e FLIP costumam ter programação especial para crianças, "
        "com contação de histórias e oficinas criativas. 🧒📖",
    ),
    (
        "posso comprar livros nas feiras literárias?",
        "Sim! As feiras literárias são ótimos locais para comprar livros, geralmente com descontos "
        "e promoções especiais. Muitas editoras oferecem preços diferenciados durante os eventos. 🛒",
    ),
    (
        "qual a diferença entre bienal e feira literária?",
        "A principal diferença é a frequência: 'bienal' significa que o evento ocorre a cada dois anos, "
        "enquanto 'feira' pode ser anual. No conteúdo, ambas vendem livros e promovem encontros culturais, "
        "mas as bienais costumam ser maiores em escala. 📅",
    ),
    (
        "tem alguma feira literária em julho?",
        "Sim! Julho é um mês cheio de feiras literárias. A FLIP (Paraty) e a Bienal do Livro SP "
        "costumam ocorrer nessa época. É uma ótima opção para as férias escolares! ☀️",
    ),
    (
        "me recomende uma feira para iniciantes em literatura",
        "Para quem está começando, a Bienal Internacional do Livro de São Paulo é excelente: "
        "tem uma enorme variedade de títulos, preços acessíveis e programação para todos os gostos. "
        "A Feira do Livro de Porto Alegre também é muito acolhedora! 💡",
    ),
    (
        "tem feira literária no nordeste?",
        "Sim! O Nordeste tem eventos literários de peso: a Bienal do Livro Bahia (Salvador) "
        "e a Bienal Internacional do Livro de Pernambuco (Recife) são os maiores. "
        "A cena literária nordestina é rica e crescente! 🌵",
    ),
    (
        "qual feira tem melhor programação musical?",
        "A FLIP de Paraty é famosa por combinar literatura com shows musicais e o charme da cidade histórica. "
        "É uma mistura incrível de cultura que vai além dos livros! 🎵",
    ),
    (
        "feiras literárias são apenas para adultos?",
        "Não! As principais feiras têm programação para todas as idades. "
        "Há sessões infantis, juvenis e adultas, tornando-as ótimas opções de passeio em família. 👨‍👩‍👧‍👦",
    ),
    (
        "como me inscrever em uma oficina de feira literária?",
        "As inscrições para oficinas costumam ser feitas pelo site oficial de cada feira, "
        "geralmente com vagas limitadas. Fique de olho nos sites com antecedência "
        "pois as oficinas têm alta demanda! ✏️",
    ),
    (
        "as feiras literárias são acessíveis para pessoas com deficiência?",
        "As grandes feiras, como a Bienal do Livro SP e a FLIP, têm se preocupado cada vez mais "
        "com acessibilidade, oferecendo rampas, intérpretes de Libras e materiais em Braille. "
        "Consulte os sites oficiais para detalhes de cada edição. ♿",
    ),
]

# ---------------------------------------------------------------------------
# Perguntas GENÉRICAS (sem especificar cidade/edição)
# → respostas conceituais + pedido de especificação
# ---------------------------------------------------------------------------

_RESP_BIENAL_GENERICA = (
    "A Bienal do Livro é um grande festival cultural e literário que reúne editoras, "
    "livrarias, autores e leitores para celebrar a leitura. "
    "No Brasil temos várias: Bienal de São Paulo, Bienal do Rio de Janeiro, "
    "Bienal Bahia (Salvador) e Bienal de Pernambuco (Recife). "
    "Sobre qual delas você gostaria de saber mais? 📚"
)

_RESP_BIENAL_DATA_GENERICA = (
    "Temos várias Bienais do Livro no Brasil, cada uma com seu calendário próprio: "
    "São Paulo (julho), Rio de Janeiro (setembro), Bahia (outubro) e Pernambuco (outubro). "
    "Sobre qual delas você quer saber a data exata? 📅"
)

_RESP_BIENAL_LOCAL_GENERICA = (
    "Existem Bienais do Livro em diferentes cidades brasileiras: "
    "São Paulo (Pavilhão do Anhembi – Av. Olavo Fontoura, 1209), "
    "Rio de Janeiro (Riocentro – Av. Salvador Allende, 6555), "
    "Salvador/BA (Centro de Convenções da Bahia – Av. ACM, s/n) e "
    "Recife/PE (Centro de Convenções de Pernambuco). Qual delas você quer conhecer? 📍"
)

GENERIC_TYPE_QA = [
    # --- "Bienal do livro" sem cidade ---
    ("o que é a bienal do livro?", _RESP_BIENAL_GENERICA),
    ("o que é bienal do livro?", _RESP_BIENAL_GENERICA),
    ("o que é bienal do livro", _RESP_BIENAL_GENERICA),
    ("me fala sobre a bienal do livro", _RESP_BIENAL_GENERICA),
    ("me conta sobre a bienal do livro", _RESP_BIENAL_GENERICA),
    ("fala sobre a bienal do livro", _RESP_BIENAL_GENERICA),
    ("quero saber sobre a bienal do livro", _RESP_BIENAL_GENERICA),
    ("o que é a bienal?", _RESP_BIENAL_GENERICA),
    ("o que é uma bienal literária?", _RESP_BIENAL_GENERICA),
    ("o que são as bienais do livro?", _RESP_BIENAL_GENERICA),
    ("quais são as bienais do livro no brasil?", _RESP_BIENAL_GENERICA),
    ("quantas bienais do livro existem no brasil?", _RESP_BIENAL_GENERICA),
    ("bienal do livro o que é?", _RESP_BIENAL_GENERICA),
    ("me explica o que é a bienal do livro", _RESP_BIENAL_GENERICA),

    # --- Data genérica ---
    ("quando é a bienal do livro?", _RESP_BIENAL_DATA_GENERICA),
    ("qual a data da bienal do livro?", _RESP_BIENAL_DATA_GENERICA),
    ("em que mês acontece a bienal do livro?", _RESP_BIENAL_DATA_GENERICA),
    ("quando vai ser a bienal do livro?", _RESP_BIENAL_DATA_GENERICA),

    # --- Local genérico ---
    ("onde acontece a bienal do livro?", _RESP_BIENAL_LOCAL_GENERICA),
    ("onde é a bienal do livro?", _RESP_BIENAL_LOCAL_GENERICA),
    ("em que cidade é a bienal do livro?", _RESP_BIENAL_LOCAL_GENERICA),

    # --- Conceito de festival literário ---
    (
        "o que é um festival literário?",
        "Um festival literário é um evento cultural dedicado à celebração da leitura e da literatura, "
        "reunindo autores, editoras, livreiros e leitores. Costumam incluir debates, lançamentos de livros, "
        "oficinas e atividades culturais. No Brasil se destacam: FLIP (Paraty), FLIC (BH), FLOR (SP), "
        "Flipoços (Poços de Caldas) e Festival Literário Catarinense. 🎭",
    ),
    (
        "o que é um festival literário brasileiro?",
        "Os festivais literários brasileiros são eventos culturais que celebram a leitura e reúnem "
        "autores, editoras e leitores. Vão desde grandes bienais (SP, Rio, Bahia, Pernambuco) até "
        "festivais intimistas como FLIP, FLIC e FLOR. Cada um tem sua identidade única! 🌟",
    ),

    # --- Conceito de feira literária ---
    (
        "o que é uma feira literária?",
        "Uma feira literária é um espaço de encontro entre leitores, autores e editoras "
        "para vender, lançar e debater livros. Podem durar dias ou semanas, com programação "
        "cultural variada. As mais famosas no Brasil: Bienal SP, FLIP, FLIC, FLOR, "
        "Bienal Bahia, Bienal PE e Feira do Livro de Porto Alegre. 📖",
    ),
    (
        "o que são feiras literárias?",
        "Feiras literárias são eventos culturais voltados para livros, leitura e literatura. "
        "Reúnem editoras, autores e leitores em um só lugar, com debates, lançamentos, oficinas e vendas. "
        "No Brasil há feiras em todas as regiões do país! 📚",
    ),
]

# Recomendações por gênero
GENRE_QA = [
    (
        f"você recomenda alguma feira para quem gosta de {genero}?",
        f"Para quem aprecia {genero}, a Bienal do Livro SP costuma ter a maior variedade de títulos "
        f"e lançamentos nesse estilo. A FLIP também tem mesas temáticas e debates sobre diferentes "
        f"correntes literárias. Vale conferir a programação antes de ir! 📚",
    )
    for genero in GENEROS
]

# Fora de escopo
OUT_OF_SCOPE_QA = [
    (
        "qual o resultado do jogo de ontem?",
        "Desculpe, meu foco são as feiras literárias brasileiras! "
        "Posso ajudar com datas, autores, ingressos e programação de eventos literários. 📚",
    ),
    (
        "quanto vale um dólar hoje?",
        "Isso foge do meu domínio! Sou especialista em feiras literárias do Brasil. "
        "Posso ajudar com informações sobre Bienal, FLIP, FLIC e outros eventos. 📚",
    ),
    (
        "me recomende um restaurante",
        "Restaurantes não são a minha especialidade, mas feiras literárias sim! "
        "Que tal saber mais sobre algum evento literário? 😄",
    ),
    (
        "como fazer um bolo de chocolate?",
        "Receitas estão fora do meu alcance, mas se você quiser, posso indicar "
        "livros de culinária presentes nas feiras literárias! 📖",
    ),
    (
        "qual o melhor time de futebol do brasil?",
        "Isso é muito controverso e foge do meu domínio! 😄 "
        "Mas posso dizer com certeza qual é o melhor evento literário para você visitar. O que acha?",
    ),
]

# Afunilamento
FUNNEL_QA = [
    (
        "me fala mais sobre feiras literárias",
        "Claro! Sobre qual aspecto você quer saber mais?\n"
        "📅 Datas e edições\n"
        "📍 Locais e cidades\n"
        "🎤 Autores participantes\n"
        "🎟️ Ingressos e preços\n"
        "📋 Programação e atividades",
    ),
    (
        "quero informações sobre feiras",
        "Posso ajudar! Você quer saber sobre qual feira especificamente? "
        "Temos: Bienal SP, Bienal Rio, FLIP, FLIC, Feira POA, FLOR, "
        "Bienal Bahia, Bienal PE, Feira Unesp, Flipoços e Festival Literário SC, entre outras.",
    ),
    (
        "preciso de ajuda",
        "Claro! Sou especialista em feiras literárias brasileiras. "
        "Posso informar sobre datas, locais, programação, ingressos e autores. O que deseja saber?",
    ),
]


# ---------------------------------------------------------------------------
# Variações coloquiais / aliases de feiras com nomes parecidos
# Garante que perguntas como "Bienal do Livro do Rio" e
# "Bienal do Livro do Rio de Janeiro" sejam respondidas corretamente.
# ---------------------------------------------------------------------------

_BIENAL_RIO = next(f for f in FEIRAS if f["sigla"] == "Bienal Rio")
_BIENAL_SP  = next(f for f in FEIRAS if f["sigla"] == "Bienal do Livro SP")

ALIAS_QA = [
    # --- Bienal do Livro do Rio (variações coloquiais) ---
    (
        "qual o endereço da Bienal do Livro do Rio?",
        f"O endereço da {_BIENAL_RIO['nome']} é: {_BIENAL_RIO['endereco']}. "
        f"Para informações de transporte e estacionamento, consulte {_BIENAL_RIO['site']}. 🗺️",
    ),
    (
        "qual o endereço da Bienal do Livro do Rio de Janeiro?",
        f"O endereço da {_BIENAL_RIO['nome']} é: {_BIENAL_RIO['endereco']}. "
        f"Para informações de transporte e estacionamento, consulte {_BIENAL_RIO['site']}. 🗺️",
    ),
    (
        "onde fica a Bienal do Livro do Rio?",
        f"A {_BIENAL_RIO['nome']} é realizada em {_BIENAL_RIO['local']}. "
        f"O endereço completo é: {_BIENAL_RIO['endereco']}. 📍",
    ),
    (
        "onde fica a Bienal do Livro do Rio de Janeiro?",
        f"A {_BIENAL_RIO['nome']} é realizada em {_BIENAL_RIO['local']}. "
        f"O endereço completo é: {_BIENAL_RIO['endereco']}. 📍",
    ),
    (
        "onde é a Bienal do Rio de Janeiro?",
        f"A {_BIENAL_RIO['nome']} acontece em {_BIENAL_RIO['local']} "
        f"({_BIENAL_RIO['endereco']}). 📍",
    ),
    (
        "onde fica a Bienal do Rio de Janeiro?",
        f"A {_BIENAL_RIO['nome']} é realizada em {_BIENAL_RIO['local']}. "
        f"Endereço: {_BIENAL_RIO['endereco']}. 📍",
    ),
    (
        "quando é a Bienal do Livro do Rio?",
        f"A {_BIENAL_RIO['nome']} geralmente acontece em {_BIENAL_RIO['mes']}. "
        f"Consulte {_BIENAL_RIO['site']} para as datas exatas. 📅",
    ),
    (
        "quando é a Bienal do Livro do Rio de Janeiro?",
        f"A {_BIENAL_RIO['nome']} geralmente acontece em {_BIENAL_RIO['mes']}. "
        f"Consulte {_BIENAL_RIO['site']} para as datas exatas. 📅",
    ),
    (
        "o que é a Bienal do Livro do Rio?",
        f"A {_BIENAL_RIO['nome']} é {_BIENAL_RIO['descricao']}. "
        f"Acontece em {_BIENAL_RIO['local']} no mês de {_BIENAL_RIO['mes']}. "
        f"Acesse {_BIENAL_RIO['site']} para mais informações. 📚",
    ),
    (
        "quais autores já foram convidados para a Bienal do Livro do Rio?",
        f"A {_BIENAL_RIO['nome']} já recebeu como convidados nomes como "
        f"{_BIENAL_RIO['convidados_exemplos'][0]}, {_BIENAL_RIO['convidados_exemplos'][1]} e "
        f"{_BIENAL_RIO['convidados_exemplos'][2]}, entre outros. "
        f"Os convidados de cada edição são anunciados em {_BIENAL_RIO['site']}. ✍️",
    ),
    (
        "quem já foi homenageado na Bienal do Livro do Rio?",
        f"A {_BIENAL_RIO['nome']} já prestou homenagem a autores como "
        f"{_BIENAL_RIO['homenageados'][0]}, {_BIENAL_RIO['homenageados'][1]} e "
        f"{_BIENAL_RIO['homenageados'][2]}. "
        f"O homenageado de cada edição é anunciado em {_BIENAL_RIO['site']}. 🏆",
    ),
    # --- Bienal do Livro de SP (variações com "de SP" / "São Paulo") ---
    (
        "onde fica a Bienal do Livro de São Paulo?",
        f"A {_BIENAL_SP['nome']} acontece no {_BIENAL_SP['local']}. "
        f"Endereço: {_BIENAL_SP['endereco']}. 📍",
    ),
    (
        "qual o endereço da Bienal do Livro de São Paulo?",
        f"O endereço da {_BIENAL_SP['nome']} é: {_BIENAL_SP['endereco']}. "
        f"Para informações de transporte e estacionamento, consulte {_BIENAL_SP['site']}. 🗺️",
    ),
    (
        "quando é a Bienal do Livro de São Paulo?",
        f"A {_BIENAL_SP['nome']} geralmente acontece em {_BIENAL_SP['mes']}. "
        f"Consulte {_BIENAL_SP['site']} para as datas exatas. 📅",
    ),
]


# ---------------------------------------------------------------------------
# Geração do CSV
# ---------------------------------------------------------------------------

def gerar_linhas() -> list:
    linhas = []

    # 1. Templates estáticos
    for inputs, response in TEMPLATES:
        for user_input in inputs:
            linhas.append((user_input, response))

    # 2. Templates dinâmicos por feira
    for feira in FEIRAS:
        for templates_input, template_resp in DYNAMIC_TEMPLATES:
            for tpl in templates_input:
                user_input = tpl.format(
                    sigla=feira["sigla"],
                    nome=feira["nome"],
                )
                # Escolhe homenageados e convidados aleatórios para cada pergunta
                hom = random.sample(feira["homenageados"], min(3, len(feira["homenageados"])))
                conv = random.sample(feira["convidados_exemplos"], min(3, len(feira["convidados_exemplos"])))
                response = template_resp.format(
                    nome=feira["nome"],
                    sigla=feira["sigla"],
                    local=feira["local"],
                    endereco=feira["endereco"],
                    mes=feira["mes"],
                    site=feira["site"],
                    descricao=feira["descricao"],
                    hom1=hom[0],
                    hom2=hom[1] if len(hom) > 1 else hom[0],
                    hom3=hom[2] if len(hom) > 2 else hom[0],
                    conv1=conv[0],
                    conv2=conv[1] if len(conv) > 1 else conv[0],
                    conv3=conv[2] if len(conv) > 2 else conv[0],
                )
                linhas.append((user_input, response))

    # 3. Perguntas gerais
    linhas.extend(GENERAL_QA)

    # 4. Perguntas genéricas sem especificação de feira (conceitos + disambiguação)
    linhas.extend(GENERIC_TYPE_QA)

    # 5. Recomendações por gênero
    linhas.extend(GENRE_QA)

    # 6. Fora de escopo
    linhas.extend(OUT_OF_SCOPE_QA)

    # 7. Afunilamento
    linhas.extend(FUNNEL_QA)

    # 8. Variações coloquiais / aliases (Rio vs SP vs nomes compostos)
    linhas.extend(ALIAS_QA)

    return linhas


def gerar_dataset(output_path: str = "data/feiras_literarias.csv", n_target: int = 1000):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    linhas = gerar_linhas()

    # Se gerou menos que n_target, completa com variações aleatórias
    while len(linhas) < n_target:
        feira = random.choice(FEIRAS)
        conv = random.sample(feira["convidados_exemplos"], min(2, len(feira["convidados_exemplos"])))
        variacao = random.choice([
            (
                f"tem como me informar sobre a {feira['sigla']}?",
                f"Claro! A {feira['nome']} acontece em {feira['mes']}, em {feira['local']}. "
                f"Para mais detalhes, acesse {feira['site']}. 📚",
            ),
            (
                f"quero saber tudo sobre a {feira['sigla']}",
                f"A {feira['nome']} é {feira['descricao']}. "
                f"Ocorre em {feira['mes']} em {feira['local']}. "
                f"Mais informações em {feira['site']}.",
            ),
            (
                f"vale a pena ir na {feira['sigla']}?",
                f"Com certeza! A {feira['nome']} é {feira['descricao']}. "
                f"Confira a programação em {feira['site']} e planeje sua visita! 🌟",
            ),
            (
                f"qual o endereço da {feira['sigla']}?",
                f"A {feira['nome']} acontece em: {feira['endereco']}. "
                f"Mais detalhes logísticos em {feira['site']}. 🗺️",
            ),
            (
                f"quais autores já foram convidados para a {feira['sigla']}?",
                f"A {feira['nome']} já recebeu como convidados nomes como {conv[0]} e {conv[1]}, "
                f"entre outros autores. Os convidados de cada nova edição são anunciados em {feira['site']}. ✍️",
            ),
        ])
        linhas.append(variacao)

    # Embaralha para distribuir os tipos uniformemente
    random.shuffle(linhas)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_input", "response"])
        writer.writerows(linhas)

    print(f"✅ Dataset gerado com {len(linhas)} linhas em '{output_path}'.")


if __name__ == "__main__":
    gerar_dataset()
