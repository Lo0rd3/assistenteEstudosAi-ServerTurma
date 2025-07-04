from utils import getApiKey
from resumo import generateSumary
from quiz import interactiveQuiz
from flashcards import interactFlashcards
from flashcards import genFlashcards
from cheatSheet import generateCheatSheet
from dotenv import load_dotenv
import os

load_dotenv()
api_key = getApiKey()
os.system('cls' if os.name == 'nt' else 'clear')


try:
    while True:
        print("\n==== Assistente de Estudos ====")
        print("[1] Gerar Resumos")
        print("[2] Gerar CheatSheets")
        print("[3] Fazer Quiz Interativo")
        print("[4] Gerar Flashcards")
        print("[5] Praticar Flashcards")
        print("[0] Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            generateSumary()
        elif choice == "2":
            generateCheatSheet()
        elif choice == "3":
          interactiveQuiz()
        elif choice == "4":
             genFlashcards()
        elif choice == "5":
            interactFlashcards()
        elif choice == "0":
            print("Até logo!")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opção inválida. Tente novamente.")
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo user.")

