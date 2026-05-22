import pytest
import os

def test_dockerfile_exists():
    assert os.path.exists('Dockerfile')

def test_requirements_contains_test_deps():
    with open('requirements.txt', 'r') as f:
        content = f.read()
        assert 'pytest' in content
        assert 'pytest-mock' in content

# UserService Tests
def test_register_user(app):
    from app.services.user_service import UserService
    success, user = UserService.register_user('test@example.com', 'password123', name='Tester')
    assert success is True
    assert user.email == 'test@example.com'
    assert user.name == 'Tester'

def test_register_duplicate_user(app):
    from app.services.user_service import UserService
    UserService.register_user('test@example.com', 'password123')
    success, message = UserService.register_user('test@example.com', 'newpassword')
    assert success is False
    assert message == "Usuário já cadastrado"

def test_authenticate_user(app):
    from app.services.user_service import UserService
    UserService.register_user('test@example.com', 'password123')
    success, user = UserService.authenticate_user('test@example.com', 'password123')
    assert success is True
    assert user.email == 'test@example.com'

# Route Tests
def test_index_redirects(client):
    response = client.get('/')
    assert response.status_code == 302 # Redirects to login

def test_agenda_unauthorized(client):
    response = client.get('/agenda')
    assert response.status_code == 302 # Redirects to login

def test_login_api(client, app):
    from app.services.user_service import UserService
    with app.app_context():
        UserService.register_user('api@test.com', 'pass')
    
    response = client.post('/login', json={'email': 'api@test.com', 'senha': 'pass'})
    assert response.status_code == 200
    assert response.get_json()['message'] == "Login realizado com sucesso"

def test_register_invalid_email(client):
    response = client.post('/cadastro', json={'email': 'invalid-email', 'senha': 'pass'})
    assert response.status_code == 400
    assert "email inválido" in response.get_json()['error']

def test_update_password_api(client, app):
    from app.services.user_service import UserService
    with app.app_context():
        UserService.register_user('update@test.com', 'old-pass')
    
    # Login
    client.post('/login', json={'email': 'update@test.com', 'senha': 'old-pass'})
    
    # Update password
    response = client.put('/api/user/password', json={'new_password': 'new-pass'})
    assert response.status_code == 200
    
    # Verify new password works
    client.get('/logout')
    response = client.post('/login', json={'email': 'update@test.com', 'senha': 'new-pass'})
    assert response.status_code == 200

def test_delete_user_cascade_api(client, app):
    from app.services.user_service import UserService
    from app.services.calendar_service import CalendarService
    from app.models import CalendarEvent, User
    from datetime import datetime
    
    with app.app_context():
        _, user = UserService.register_user('delete@test.com', 'pass')
        user_id = user.id
        CalendarService.add_event(user_id, 'Bye', 'Desc', datetime.now())
    
    # Login
    client.post('/login', json={'email': 'delete@test.com', 'senha': 'pass'})
    
    # Delete account
    response = client.delete('/api/user')
    assert response.status_code == 200
    
    # Verify user and events are gone
    with app.app_context():
        assert User.query.filter_by(email='delete@test.com').first() is None
        assert CalendarEvent.query.filter_by(user_id=user_id).count() == 0
