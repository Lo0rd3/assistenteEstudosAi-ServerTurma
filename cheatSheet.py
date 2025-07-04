# cheatsheet.py
from utils import getApiKey
import os
import google.generativeai as genai

def readPrompt():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(scriptDir, "CheatsheetPrompt.txt")
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            if os.stat(filePath).st_size == 0:
                print(f"Arquivo CheatsheetPrompt.txt está vazio em {filePath}!")
                return None
            return f.read()
    except FileNotFoundError:
        print(f"Arquivo CheatsheetPrompt.txt não encontrado em {filePath}!")
        return None

def generateCheatSheet():
    os.system('cls' if os.name == 'nt' else 'clear')  

    genai.configure(api_key=getApiKey())
    model = genai.GenerativeModel('gemini-2.5-flash')

    while True:
        theme = input("Tema do cheatsheet: ").strip()
        if not theme:
            print("Tema não pode estar vazio.")
        else:
            break
    while True:
        print("\nEm que formato deseja guardar o cheatsheet?")
        print("[1] Markdown (.md)")
        print("[2] Texto Simples (.txt)")
        choice = input("Escolha: ").strip()
        if choice == "1":
            cheatsheetFormat = (
                "Markdown limpo e bem estruturado para uso em Obsidian.\n\n"
                "Para cada item do cheatsheet, siga exatamente esta estrutura:\n\n"
                "## <Tarefa ou Ação>\n\n"
                "**Comando:**\n"
                "```\n"
                "<comando real, exemplo de uso>\n"
                "```\n\n"
                "**Explicação:**\n"
                "<explicação clara e objetiva do comando, incluindo opções, flags, e contexto de uso>\n\n"
                "Regras de Formatação:\n"
                "- Use `##` como título da tarefa/comando (não use `#` nem `###`)\n"
                "- Use blocos de código apenas para os comandos (crase tripla: ```)\n"
                "- Evite listas numeradas — use apenas listas com hífen (`-`) quando necessário\n"
                "- Separe cada item com **duas linhas em branco** para clareza\n"
                "- Seja consistente na estrutura, para manter o cheatsheet limpo e útil como referência\n"
            )

            extension = ".md"
            break
        elif choice == "2":
            cheatsheetFormat = "texto simples (.txt) sem qualquer formatação markdown."
            extension = ".txt"
            break
        else:
            print("Opção inválida. Tenta novamente.")
    promptBase = readPrompt()
    if promptBase is None:
        return
    prompt = promptBase.replace("{theme}", theme).replace("{cheatsheetFormat}", cheatsheetFormat)

    while True:
        print("\nConsultando Gemini...\n")
        try:
            response = model.generate_content(prompt)
            cheatsheet = response.text
        except Exception as e:
            print(f"Erro ao gerar cheatsheet com o Gemini: {e}")
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n=== CHEATSHEET GERADO ===\n")
        print(cheatsheet)
        print("\nO que deseja fazer?")
        print("[1] Guardar este cheatsheet")
        print("[2] Pedir alterações ao Gemini")
        print("[0] Voltar ao menu")
        op = input("Escolha: ").strip()

        if op == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            if not os.path.exists("cheatsheets"):
                os.makedirs("cheatsheets")
            outputPath = os.path.join("cheatsheets", theme.replace(" ", "_") + extension)
            with open(outputPath, "w", encoding="utf-8") as f:
                f.write(cheatsheet)
            print(f"Cheatsheet guardado em: {outputPath}")
            break
        elif op == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            newComment = input("Digite o seu comentário: ").strip()
            if newComment:
                prompt += "\n\n" + newComment
            else:
                print("Entrada vazia — voltando ao menu.")
        elif op == "0":
            break
        else:
            print("Opção inválida.")
  