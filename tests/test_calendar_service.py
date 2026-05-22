import pytest
from datetime import datetime, timedelta
from app.services.calendar_service import CalendarService
from app.services.user_service import UserService

def test_get_user_events_filtering(app):
    with app.app_context():
        _, user = UserService.register_user('filter@test.com', 'pass')
        
        now = datetime.now()
        CalendarService.add_event(user.id, 'Today', 'Desc', now)
        CalendarService.add_event(user.id, 'Tomorrow', 'Desc', now + timedelta(days=1))
        CalendarService.add_event(user.id, 'Next Week', 'Desc', now + timedelta(days=7))
        
        # Filter for the next 2 days
        start = now - timedelta(hours=1)
        end = now + timedelta(days=2)
        events = CalendarService.get_user_events(user.id, start_date=start, end_date=end)
        
        assert len(events) == 2
        titles = [e.title for e in events]
        assert 'Today' in titles
        assert 'Tomorrow' in titles
        assert 'Next Week' not in titles

def test_get_user_events_only_own(app):
    with app.app_context():
        _, user1 = UserService.register_user('u1@test.com', 'pass')
        _, user2 = UserService.register_user('u2@test.com', 'pass')
        
        CalendarService.add_event(user1.id, 'U1 Event', 'Desc', datetime.now())
        CalendarService.add_event(user2.id, 'U2 Event', 'Desc', datetime.now())
        
        u1_events = CalendarService.get_user_events(user1.id)
        assert len(u1_events) == 1
        assert u1_events[0].title == 'U1 Event'

def test_update_event(app):
    with app.app_context():
        _, user = UserService.register_user('update_svc@test.com', 'pass')
        event = CalendarService.add_event(user.id, 'Old Title', 'Old Desc', datetime.now())
        
        success, updated_event = CalendarService.update_event(event.id, user.id, title='New Title')
        assert success is True
        assert updated_event.title == 'New Title'

def test_delete_event(app):
    with app.app_context():
        _, user = UserService.register_user('delete_svc@test.com', 'pass')
        event = CalendarService.add_event(user.id, 'Bye', 'Desc', datetime.now())
        
        success = CalendarService.delete_event(event.id, user.id)
        assert success is True
        assert CalendarService.delete_event(event.id, user.id) is False # Already gone
