import json
import os
import google.generativeai as genai
from datetime import datetime
from app.services.calendar_service import CalendarService

class AIGeminiService:
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY')
        model_name = os.environ.get('GEMINI_MODEL_NAME', 'gemini-pro')
        
        if api_key:
            genai.configure(api_key=api_key)
            
            # Refactored to use system_instruction for better JSON compliance
            system_instruction = (
                "Você é um assistente de agendamento profissional. "
                "Dada a entrada do usuário, extraia: title, description, start_time e end_time. "
                "Use o formato ISO 8601 para datas. "
                "Se o usuário não disser o ano, use 2026. "
                "Responda APENAS com um objeto JSON válido ou uma lista JSON de objetos."
            )
            
            self.model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
        else:
            self.model = None

    def process_annotation_prompt(self, user_prompt):
        """Processes a free-text prompt to extract structured event data."""
        if not self.model:
            return {"error": "API Key not configured"}

        # Get current date for context
        now = datetime.now()
        current_date_info = f"Hoje é {now.strftime('%A, %d de %B de %Y, %H:%M')}. "
        
        system_instruction = (
            "Você é um assistente de agendamento profissional. "
            f"{current_date_info}"
            "Dada a entrada do usuário, extraia: title, description, start_time e end_time. "
            "Se o usuário não especificar uma data ou disser apenas o horário, assuma que é para HOJE. "
            "Use o formato ISO 8601 para datas. Responda APENAS com um objeto JSON válido ou uma lista JSON de objetos."
        )

        try:
            print(f"DEBUG: Enviando prompt para IA: {user_prompt}")
            # Use specific system instruction for this call
            response = self.model.generate_content(f"{system_instruction}\n\nUsuário: {user_prompt}")
            content = response.text.strip()
            print(f"DEBUG: Resposta bruta da IA: {content}")
            
            # Clean possible markdown formatting
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            try:
                event_data = json.loads(content)
                print(f"DEBUG: JSON parseado com sucesso: {event_data}")
                
                # If IA returns a list, take the first element (common for single prompts)
                if isinstance(event_data, list) and len(event_data) > 0:
                    event_data = event_data[0]
                    print(f"DEBUG: Extraído primeiro item da lista: {event_data}")
                    
            except json.JSONDecodeError as e:
                print(f"DEBUG: Falha no JSONDecodeError: {str(e)}")
                return {"error": "Falha ao processar resposta da IA: JSON inválido", "raw_content": content}

            # Validate mandatory fields
            if not event_data.get('title') or not event_data.get('start_time'):
                print(f"DEBUG: Validação falhou. Campos ausentes em: {event_data}")
                return {"error": "IA retornou dados incompletos", "received": event_data}

            return event_data
        except Exception as e:
            print(f"DEBUG: Erro crítico na chamada Gemini: {str(e)}")
            return {"error": f"Erro na chamada à API Gemini: {str(e)}"}

    def generate_routine_and_save(self, user_id, routine_type, context, days, start_reference="hoje"):
        """Generates a complex routine for a specific number of days starting from a reference and saves it."""
        if not self.model:
            return False, "API Key not configured"

        prompt = (
            f"Gerar uma rotina de {routine_type} para {days} dias, começando a partir de: {start_reference}. "
            f"Contexto adicional: {context}. "
            "Retornar uma lista JSON de objetos com 'title', 'description', 'start_time' e 'end_time' (formato ISO 8601). "
            "Certifique-se de que os horários façam sentido para a rotina solicitada."
        )


        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            routine_events = json.loads(content)
            new_ids = []
            
            for event in routine_events:
                start_time = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(event['end_time'].replace('Z', '+00:00')) if event.get('end_time') else None
                
                new_event = CalendarService.add_event(
                    user_id=user_id,
                    title=event['title'],
                    description=event.get('description', ''),
                    start_time=start_time,
                    end_time=end_time,
                    is_ai_generated=True
                )
                new_ids.append(new_event.id)
            
            return True, new_ids
        except Exception as e:
            return False, f"Falha na geração da rotina pela IA: {str(e)}"
