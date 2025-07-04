import os
import csv
import google.generativeai as genai
from utils import getApiKey
from datetime import datetime
import random

def genFlashcards():
    genai.configure(api_key=getApiKey())
    model = genai.GenerativeModel('gemini-2.5-flash')

    os.system('cls' if os.name == 'nt' else 'clear') 

    # Pergunta o tema
    while True:
        Theme = input("Tema dos flashcards: ").strip()
        if Theme and len(Theme) >= 3:
            break
        print("\nO tema deve ter pelo menos 3 caracteres.")

    # Pergunta quantos flashcards
    while True:
        Num = input("\nQuantos flashcards quer gerar? ").strip()
        if Num.isdigit() and int(Num) > 0:
            NumCards = int(Num)
            break
        print("\nPor favor, insira um número válido.")

    # Gera os flashcards
    genPrompt = (
            "Você é um especialista em educação e técnicas de estudo, altamente capacitado em criar flashcards perfeitos que facilitam a memorização ativa e a recuperação eficiente da informação. "
            "Seu objetivo é elaborar flashcards claros, diretos, e altamente eficazes, que sigam rigorosamente estas instruções:\n\n"
            f"Tema: {Theme}\n"
            f"Quantidade: {NumCards}\n\n"
            "Melhores Práticas para os Flashcards:\n"
            "1. Clareza e objetividade: Cada flashcard deve conter apenas uma ideia ou conceito central claramente formulado.\n"
            "2. Perguntas diretas: As perguntas devem estimular ativamente o raciocínio ou a recuperação ativa do conhecimento.\n"
            "3. Respostas concisas: As respostas devem ser diretas, precisas, curtas e fáceis de memorizar.\n"
            "4. Variedade e Relevância: Distribua diferentes níveis de dificuldade e aborde aspectos essenciais, importantes e interessantes sobre o tema.\n"
            "5. Exemplos práticos: Sempre que possível, inclua exemplos, casos práticos, ou informações complementares curtas que facilitem a compreensão.\n"
            "6. Facilidade de memorização: Use técnicas como associação, analogias ou mnemônicos breves nas respostas para auxiliar a retenção sempre que aplicável.\n\n"
            "Gere APENAS flashcards no seguinte formato:\n\n"
            "Pergunta: <pergunta>\n"
            "Resposta: <resposta>\n\n"
            "Observações importantes:\n"
            "- Não adicione nenhum texto introdutório ou explicações adicionais além dos flashcards.\n"
            "- Não repita ideias semelhantes entre os flashcards; cada um deve ser único e independente.\n"
            "- Os flashcards devem estar perfeitamente adaptados para estudo eficaz e otimizado.\n\n"
            "Agora, crie os flashcards solicitados!"
            )
    print("\nA gerar flashcards... aguarde!\n")
    try:
        response = model.generate_content(genPrompt)
        FlashText = response.text
    except Exception as e:
        print(f"Erro ao gerar os flashcards com o Gemini: {e}")
        return
    os.system('cls' if os.name == 'nt' else 'clear') 

    # Parsing para pares pergunta-resposta
    Flashcards = []
    bloc = [l.strip() for l in FlashText.splitlines() if l.strip()]
    q = None
    for line in bloc:
        if line.lower().startswith("pergunta:"):
            q = line.split(":", 1)[1].strip()
        elif line.lower().startswith("resposta:") and q:
            a = line.split(":", 1)[1].strip()
            Flashcards.append((q, a))
            q = None

    if not Flashcards:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Não foi possível gerar flashcards válidos.")
        return
    width = os.get_terminal_size().columns
    print(f"Gerados {len(Flashcards)} flashcards:")
    for idx, (q, a) in enumerate(Flashcards, start=1):
        print(f"{idx}. P: {q}\n   R: {a}")
    print("-" * width)
    # Pergunta se quer guardar
    SaveChoice = ""
    while SaveChoice not in ("1", "2"):
        print("\nDeseja guardar estes flashcards?")
        print("[1] Sim")
        print("[2] Não")
        SaveChoice = input("Escolha: ").strip()
        if SaveChoice not in ("1", "2"):
            print("Opção inválida! Tente novamente.")
    if SaveChoice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Flashcards não guardados.")
        return 
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal após confirmação
    # Salvar em CSV 
    if not os.path.exists("flashcards"):
        os.makedirs("flashcards")
    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"flashcards/{Theme.replace(' ', '_')}_flashcards_{now}.csv"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Pergunta;Resposta\n")
        for q, a in Flashcards:
            f.write(f"{q};{a}\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Flashcards guardados em: {filename}")
    print("\nPara importar no Anki, Quizlet ou RemNote, escolha importar CSV, separador ponto e vírgula.")
    return 













def interactFlashcards():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal    
    # Listar ficheiros disponíveis
    if not os.path.exists("flashcards"):
        os.makedirs("flashcards")

    files = [f for f in os.listdir("flashcards") if f.endswith(".csv")]
        
    if not files:
        while True:
            print("Nenhum ficheiro de flashcards (.csv) encontrado.\n")
            createChoice = input("Pretende criar novos flashcards?\nEscolha [s/n]: ").strip().lower()
            
            if createChoice == "s":
                genFlashcards()
                praticar = input("\nDeseja praticar os flashcards criados? [s/n]: ").strip().lower()
                if praticar == "s":
                    return interactFlashcards()
                else:
                    print("A voltar ao menu principal.")
                    return
            elif createChoice == "n":
                print("A voltar ao menu principal.")
                return
            else:
                print("Opção invalida. Tente Novamente.")
                   

    print("\nFicheiros de flashcards disponíveis:")
    for idx, name in enumerate(files, start=1):
        print(f"[{idx}] {name}")
    
    print("\n[Q] Voltar ao menu principal")
    print("[N] Criar novos flashcards")
    while True:
        choice = input("\nEscolhe o número do ficheiro para praticar: ").strip().lower()
        if choice== "q":
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
            print("\nA voltar ao menu principal.")
            return
        elif choice == "n":
            genFlashcards()
            os.system('cls' if os.name == 'nt' else 'clear')  #
            praticar = input("\nDeseja praticar os flashcards criados? [s/n]: ").strip().lower()
            if praticar == "s":
                return interactFlashcards()
            else:
                print("A voltar ao menu principal.")
                return
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            fileToRun = files[int(choice)-1]
            break
        print("Opção inválida. Tenta novamente.")
    
    


    
    path = os.path.join("flashcards", fileToRun)
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Salta o cabeçalho
            cards = list(reader)

    except Exception as e:
        print(f"\nErro ao ler o ficheiro: {e}")
        return
    
    if not cards:
        print("\nO ficheiro selecionado está vazio.")
        return

    random.shuffle(cards)  # Baralhar os cartões

    while True:
        print("\nPretende contar as respostas corretas durante a prática?")
        print("\n[1] Sim")
        print("[2] Não")
        countChoice = input("Escolha: ").strip()
        if countChoice == "1":
            countCorrect = True
            break
        elif countChoice == "2":
            countCorrect = False
            break
        else:
            print("\nOpção inválida. Tente novamente.")




    print(f"\nA praticar flashcards de: {fileToRun}\n")
    correct = 0
    answered= 0
    width = os.get_terminal_size().columns
    for idx, (question, answer) in enumerate(cards, start=1):
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("=" * width)
        print(f"Cartão {idx}:\n\n\n{question}\n\n\n")
        print("=" * width)
        userInput = input("Carregue ENTER para ver a resposta\n[Q]-sair").strip().lower()
        if userInput == 'q':
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
            print("A sair da prática de flashcards.")
            break
        answered += 1 
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
        print("=" * width)
        print(f"Resposta:\n\n\n{answer}\n\n\n")
        print("=" * width)
              
        if countCorrect:
            while True:
                gotIt = input("Resposta correta? (s/n): ").strip().lower()
                if gotIt in ("s", "n"):
                    if gotIt == "s":
                        correct += 1
                    break
                print("Entrada inválida. Responde com 's' ou 'n'.")
        input("Pressiona ENTER para continuar para o proximo flashcard.\n[Q]-sair")




    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
    print("Prática de flashcards concluída!")
    print(f"\nCartões praticados: {answered}/{len(cards)}")
    if countCorrect and answered > 0:
        print(f"Respostas corretas: {correct}/{answered}")
        percentage = (correct / answered) * 100
        print(f"Taxa de acerto: {percentage:.1f}%")
    
        if correct == answered:
            print("\nExcelente! Acertaste todos os cartões!")
        elif percentage >= 70:
            print("\nBom trabalho! Estás no bom caminho.")
        elif percentage >= 50:
            print("\nContinuas a aprender! Revê os cartões que falhaste.")
        else:
            print("\nNão desanimes! Praticar é a chave para aprender.")
    width = os.get_terminal_size().columns
    print("-" * width)
    #ask if user wants to practice more flashcards
    while True:
        createChoice = input("\nDeseja praticar mais flashcards? [s/n]: ").strip().lower()
        if createChoice == "s":
            return interactFlashcards()
        elif createChoice == "n":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("A voltar ao menu principal.")
            return
        else:
            print("Opção inválida. Tente novamente.")
