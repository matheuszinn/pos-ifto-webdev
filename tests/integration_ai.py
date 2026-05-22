import os
from dotenv import load_dotenv
from app.services.ai_gemini_service import AIGeminiService

load_dotenv()

def test_real_ai_connection():
    print("Iniciando teste de conexão real com Gemini...")
    service = AIGeminiService()
    
    if not service.model:
        print("ERRO: GEMINI_API_KEY não encontrada no ambiente!")
        return

    prompt = "Marcar dentista para amanhã às 14h"
    print(f"Enviando prompt: '{prompt}'")
    
    result = service.process_annotation_prompt(prompt)
    
    if "error" in result:
        print(f"FALHA: {result['error']}")
        if "raw_content" in result:
            print(f"Conteúdo bruto: {result['raw_content']}")
    else:
        print("SUCESSO! Resposta da IA:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import json
    test_real_ai_connection()
