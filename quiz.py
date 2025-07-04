import os
import google.generativeai as genai
from utils import getApiKey
from datetime import datetime



def interactiveQuiz():
    os.system('cls' if os.name == 'nt' else 'clear')

    genai.configure(api_key=getApiKey())
    model = genai.GenerativeModel('gemini-1.5-flash')

    while True:
        Topic = input("Tema do quiz: ").strip()
        if Topic:
            break
        print("O tema não pode estar vazio.")

    
    while True:
        Num = input("\nQuantas perguntas quer no quiz? ").strip()
        if Num.isdigit() and int(Num) > 0:
            NumQuestions = int(Num)
            break
        print("\nPor favor, insira um número válido.")

    
    while True:
        print("\nEscolha o nível de dificuldade:")
        print("[1] Fácil")
        print("[2] Médio")
        print("[3] Difícil")
        DifficultyChoice = input("Escolha: ").strip()
        if DifficultyChoice == "1":
            Difficulty = "fácil"
            break
        elif DifficultyChoice == "2":
            Difficulty = "médio"
            break
        elif DifficultyChoice == "3":
            Difficulty = "difícil"
            break
        else:
            print("Opção inválida, tente novamente.")
    


    genPrompt = (
        f"Crie um quiz com {NumQuestions} perguntas de múltipla escolha sobre '{Topic}'. Nível de dificuldade: {Difficulty}.\n"
        "Não faça perguntas repetidas.\n"
        "NÃO escreva explicações, comentários ou qualquer texto fora do formato.\n"
        "Use EXATAMENTE este formato para cada pergunta, SEM NENHUMA VARIAÇÃO:\n"
        "------\n"
        "a) Pergunta.\n"
        "1- opção\n2- opção\n3- opção\n4- opção\n"
        "Resposta correta: (número da opção (ex: 2))\n"
        "------\n"
        "As perguntas devem respeitar o nível de dificuldade:\n"
        "- fácil: conceitos básicos e diretos\n"
        "- médio: envolve raciocínio ou detalhes mais específicos\n"
        "- difícil: exige conhecimento aprofundado ou análise crítica\n"
        "As opções devem ser plausíveis e distintas. Evite respostas óbvias ou absurdas.\n"
        "Apenas envie os blocos no formato acima, um após o outro, sem mais nada."
    )

    print("\nA gerar quiz... aguarde!\n")
    try:    
        response = model.generate_content(genPrompt)
        QuizText = response.text
    except Exception as e:
        print(f"Erro ao gerar o conteudo com o Gemini: {e}")
        return






    Blocks = [b.strip() for b in QuizText.split("------") if b.strip()]
    UserAnswers = {}
    CorrectAnswers = {}
    QuestionsAsked = []

    for idQuestion, Block in enumerate(Blocks, start=1):
        os.system('cls' if os.name == 'nt' else 'clear')

        Lines = [l.strip() for l in Block.splitlines() if l.strip()]
        if len(Lines) < 6:
            print("\nBloco mal formatado, ignorado.")
            continue
        Question = Lines[0]
        Options = Lines[1:5]
        CorrectLine = next((l for l in Lines if l.lower().startswith("resposta correta")), None)
        if not CorrectLine:
            print("Não encontrei resposta correta, bloco ignorado.")
            print('\n'.join(Lines))
            continue
        CorrectPart = CorrectLine.split(":")[1].strip()
        if CorrectPart.startswith("(") and CorrectPart.endswith(")"):
            CorrectNum = CorrectPart[1:-1].strip()
        else:
            CorrectNum = CorrectPart
        width = os.get_terminal_size().columns
        
        print(f"\nPergunta {idQuestion}: {Question}\n")
        print("=" * width)
        for opt in Options:
            print(opt)
            print( "-" * width)
        while True:
            Answer = input("A sua resposta (1/2/3/4): ").strip()
            if Answer in ("1", "2", "3", "4"):
                break
            print("Por favor, escolha apenas 1, 2, 3 ou 4.")
        UserAnswers[str(idQuestion)] = Answer
        CorrectAnswers[str(idQuestion)] = CorrectNum
        QuestionsAsked.append({'QNum': str(idQuestion), 'Question': Question, 'Options': Options, 'Correct': CorrectNum, 'User': Answer})

    if not UserAnswers:
        print("Não foi possível realizar o quiz devido a erro de formatação das perguntas.")
        return
   
    Score = sum(1 for q in CorrectAnswers if UserAnswers.get(q) == CorrectAnswers[q])
    print(f"\nQuiz concluído. Score: {Score}/{len(UserAnswers)}")
    print("\nA gerar correção... aguarde!\n")







    CorrectionPrompt = (
        "Faça uma correção do quiz abaixo, pergunta a pergunta. Para cada, indique a resposta correta e forneça uma breve explicação sobre o conceito abordado na pergunta.\n"
        "Nas perguntas que o aluno errou, seja mais detalhado na explicação.\n"
        "No final, sugira tópicos para rever com base nos erros.\n\n"
        "Use um formato sem qualquer markdown ou formatação especial, apenas texto simples.\n"
        "Quiz (no mesmo formato que enviado):\n" + QuizText +
        "\n\nRespostas do aluno:\n" +
        "\n".join(
            f"{item['QNum']}. Respondeu {item['User']}, correta é {item['Correct']}"
            for item in QuestionsAsked
        )
    )
    try:
        corr_response = model.generate_content(CorrectionPrompt)
        CorrectionText = corr_response.text
    except Exception as e:
        print(f"Erro ao gerar a correção com o Gemini: {e}")
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Correção e Explicações ===\n")
    print(CorrectionText)

    




    print("-" * width)
    SaveChoice = ""
    while SaveChoice not in ("1", "2"):
        print("Deseja guardar esta correção?")
        print("[1] Sim")
        print("[2] Não")
        SaveChoice = input("Escolha: ").strip()
        if SaveChoice not in ("1", "2"):
            print("Opção inválida! Tente novamente.")

    if SaveChoice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Correção não guardada.")
        return 

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nEm que formato deseja guardar o resumo?")
        print("[1] Markdown (.md)")
        print("[2] Texto simples (.txt)")
        print("[3] Cancelar")
        FormatChoice = input("Escolha: ").strip()
        if FormatChoice == "1":
            Ext = ".md"
            break
        elif FormatChoice == "2":
            Ext = ".txt"
            break
        elif FormatChoice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Gravação cancelada.")
            return
        else:
            print("Opção inválida, tente novamente.")
        os.system('cls' if os.name == 'nt' else 'clear')












    if not os.path.exists("quizzes"):
        os.makedirs("quizzes")
    
    now = datetime.now().strftime("%Y%m%d_%H%M")
    Filename = f"quizzes/{Topic.replace(' ', '_')}_correction_{Difficulty}_{now}{Ext}"
    with open(Filename, "w", encoding="utf-8") as f:
        f.write(CorrectionText)
    print(f"Correção guardada em: {Filename}")