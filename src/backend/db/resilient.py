from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.backend.core.resilience import db_resilience

class ResilientSession:
    """Wrapper for SQLAlchemy session with resilience patterns"""
    
    def __init__(self, session: Session):
        self.session = session
    
    @db_resilience
    def execute(self, *args, **kwargs):
        return self.session.execute(*args, **kwargs)
    
    @db_resilience
    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)
    
    @db_resilience
    def commit(self):
        return self.session.commit()

def resilient_db_operation(func):
    """Decorator to make database operations resilient."""
    @db_resilience
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
