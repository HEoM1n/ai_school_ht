from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class PhishingPhone(Base):
    __tablename__ = "phishing_phones"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    reported_date = Column(DateTime, default=func.now())
    is_confirmed = Column(Boolean, default=True)
    reporter_name = Column(String(100))
    description = Column(String(500))
    
    def __repr__(self):
        return f"<PhishingPhone(phone_number='{self.phone_number}', is_confirmed={self.is_confirmed})>"
