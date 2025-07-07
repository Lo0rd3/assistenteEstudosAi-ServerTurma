from utils import getApiKey
import os
import google.generativeai as genai

def user_folder(folder_name):
    return os.path.join(os.path.expanduser("~"), folder_name)


def generateSummary():
    os.system('cls' if os.name == 'nt' else 'clear') 

    genai.configure(api_key=getApiKey())
    model = genai.GenerativeModel('gemini-2.5-flash')

    while True:
        theme = input("Tema do resumo: ").strip()
        if not theme:
            print("Tema não pode estar vazio.")
        else:
            break
    while True:
        print("\nEm que formato deseja guardar o resumo?")
        print("[1] Markdown (.md, para Obsidian)")
        print("[2] Texto Simples (.txt)")
        choice = input("Escolha: ").strip()
    
        if choice == "1":
            summaryFormat = "Markdown para Obsidian, com sintaxe adequada."
            extension = ".md"
            break
        elif choice == "2":
            summaryFormat = ".txt, texto simples."
            extension = ".txt"
            break
        else:
            print("Opção inválida.")
            
    promptBase = readPrompt()
    if promptBase is None: return

    prompt = promptBase.replace("{theme}", theme).replace("{summaryFormat}", summaryFormat)

    while True:
        print("\nConsultando Gemini...\n")
        try:
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            print(f"Erro a gerar o conteudo com o gemini: {e}")
            return
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal

        print("\n=== RESUMO GERADO ===\n")
        print(summary)
        print("\nO que deseja fazer?")
        print("[1] Guardar este resumo")
        print("[2] Pedir alteraçoes ao Gemini")
        print("[0] Voltar ao menu")
        op = input("Escolha: ").strip()

        if op == "1":
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
            resumos_dir = user_folder("resumos")
            os.makedirs(resumos_dir, exist_ok=True)
            outputPath = os.path.join(resumos_dir,f"resumos"+ theme.replace(" ", "_") + extension)



            with open(outputPath, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"Resumo guardado em: {outputPath}")
            print("Os ficheiros serão eleminados do servidor em 3 dias.")
            break
        elif op == "2":
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
            while True:
                newQuestion = input("Digite o seu comentário: ").strip()
                if newQuestion:
                    prompt += "\n\n" + newQuestion
                    break
                else:
                    print("Entrada vazia — voltando ao menu.")
        elif op == "0":
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o terminal
            break
        else:
            print("Opção inválida.")

def readPrompt():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(scriptDir, "SummaryPrompt.txt")
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            if os.stat(filePath).st_size == 0:
                print(f"Arquivo SummaryPrompt.txt está vazio em {filePath}!")
                return None
            return f.read()
    except FileNotFoundError:
        print(f"Arquivo SummaryPrompt.txt não encontrado em {filePath}!")
        return None
