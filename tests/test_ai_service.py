import pytest
import json
from datetime import datetime
from app.services.ai_gemini_service import AIGeminiService
from unittest.mock import MagicMock

@pytest.fixture
def ai_service(mocker):
    # Mock genai.configure and genai.GenerativeModel
    mocker.patch('google.generativeai.configure')
    mock_model = mocker.patch('google.generativeai.GenerativeModel')
    
    service = AIGeminiService()
    service.model = mock_model.return_value
    return service

def test_process_annotation_prompt_success(ai_service):
    # Mock API response
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "title": "Meeting",
        "description": "Discuss project",
        "start_time": "2024-05-20T10:00:00",
        "end_time": "2024-05-20T11:00:00"
    })
    ai_service.model.generate_content.return_value = mock_response

    result = ai_service.process_annotation_prompt("Reunião amanhã às 10h")
    
    assert result['title'] == "Meeting"
    assert result['start_time'] == "2024-05-20T10:00:00"

def test_process_annotation_prompt_malformed_json(ai_service):
    # Mock AI returning non-json content
    mock_response = MagicMock()
    mock_response.text = "Desculpe, não consegui entender."
    ai_service.model.generate_content.return_value = mock_response

    result = ai_service.process_annotation_prompt("Ir ao médico amanhã")
    
    assert "error" in result
    assert "JSON" in result['error'] or "Não foi possível" in result['error']

def test_process_annotation_prompt_missing_fields(ai_service):
    # Mock AI returning partial JSON (missing start_time)
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "title": "Meeting"
    })
    ai_service.model.generate_content.return_value = mock_response

    result = ai_service.process_annotation_prompt("Reunião")
    
    # The service should handle missing mandatory fields from AI
    assert "error" in result

def test_generate_routine_and_save_success(ai_service, app, mocker):
    from app.services.user_service import UserService
    from app.models import db
    
    # Mock API response with a list of events
    mock_response = MagicMock()
    mock_response.text = json.dumps([
        {
            "title": "Exercise Day 1",
            "description": "Run",
            "start_time": "2024-05-20T08:00:00",
            "end_time": "2024-05-20T09:00:00"
        },
        {
            "title": "Exercise Day 2",
            "description": "Gym",
            "start_time": "2024-05-21T08:00:00",
            "end_time": "2024-05-21T09:00:00"
        }
    ])
    ai_service.model.generate_content.return_value = mock_response

    with app.app_context():
        _, user = UserService.register_user('routine@test.com', 'password')
        
        # In test mode, we might want to call the internal method directly or join the thread
        success, message = ai_service.generate_routine_and_save(user.id, "exercício", "foco em cardio", 2, "amanhã")
        
        assert success is True
        
        # Wait for the background task to complete for testing purposes
        import time
        time.sleep(1) 
        
        from app.services.calendar_service import CalendarService
        events = CalendarService.get_user_events(user.id)
        assert len(events) == 2
