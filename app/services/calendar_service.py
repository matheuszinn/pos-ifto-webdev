from app.models import db, CalendarEvent

class CalendarService:
    @staticmethod
    def add_event(user_id, title, description, start_time, end_time=None, is_ai_generated=False):
        """Creates a new calendar event."""
        if end_time and end_time < start_time:
            raise ValueError("O horário de término deve ser posterior ao horário de início.")

        new_event = CalendarEvent(
            user_id=user_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            is_ai_generated=is_ai_generated
        )
        db.session.add(new_event)
        db.session.commit()
        
        return new_event

    @staticmethod
    def get_user_events(user_id, start_date=None, end_date=None):
        """Retrieves events for a specific user, optionally filtered by date range."""
        query = CalendarEvent.query.filter_by(user_id=user_id)
        
        if start_date and end_date:
            query = query.filter(CalendarEvent.start_time.between(start_date, end_date))
            
        return query.order_by(CalendarEvent.start_time).all()

    @staticmethod
    def delete_event(event_id, user_id):
        """Deletes a calendar event if it belongs to the user."""
        event = CalendarEvent.query.filter_by(id=event_id, user_id=user_id).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_event(event_id, user_id, title=None, description=None, start_time=None, end_time=None):
        """Updates an existing calendar event."""
        event = CalendarEvent.query.filter_by(id=event_id, user_id=user_id).first()
        if not event:
            return False, "Evento não encontrado"
        
        # Determine effective times for validation
        new_start = start_time or event.start_time
        new_end = end_time or event.end_time
        
        if new_end and new_end < new_start:
            return False, "O horário de término deve ser posterior ao horário de início."
        
        if title: event.title = title
        if description is not None: event.description = description
        if start_time: event.start_time = start_time
        if end_time: event.end_time = end_time
        
        db.session.commit()
        return True, event
