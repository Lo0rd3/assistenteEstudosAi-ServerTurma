import os
_apiKey = None

def getApiKey():
    return os.getenv("GeminiApiKey") or _apiKey or input("Por favor, introduza a sua chave de API do Gemini: ").strip()