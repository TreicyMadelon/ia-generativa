import sys
import os

# Garante que o diretório raiz do projeto esteja no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.chatbot import ChatLitera


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "feiras_literarias.csv")

    if not os.path.exists(csv_path):
        print("⚠️  Arquivo de dados não encontrado.")
        print("   Execute primeiro o gerador de dataset:")
        print("   python src/generate_dataset.py\n")
        sys.exit(1)

    bot = ChatLitera(csv_path, similarity_threshold=0.2)

    print("\n" + "=" * 60)
    print("  📚 ChatLitera – Feiras Literárias Brasileiras 📚")
    print("=" * 60)
    print("  Pergunte sobre datas, locais, programação,")
    print("  ingressos e autores das principais feiras do Brasil.")
    print("  Digite 'sair' para encerrar.")
    print()
    print('  💡 Experimente começar com:')
    print('     "O que é a bienal do livro?"')
    print()

    while True:
        try:
            user_input = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nChatLitera: Até logo! 📖")
            break

        if not user_input:
            continue

        if user_input.lower() in ("sair", "exit", "quit", "q"):
            print("ChatLitera: Até logo! Continue participando das feiras literárias! 📖\n")
            break

        response = bot.get_response(user_input)
        print(f"ChatLitera: {response}\n")


if __name__ == "__main__":
    main()
