from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.sql import func
from database import Base

class PhoneReport(Base):
    __tablename__ = "PHONE_REPORTS"
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), nullable=False)
    is_phishing = Column(Boolean, nullable=False)
    spam_type = Column(String(100))
    description = Column(String(500))
    report_count = Column(Integer, default=1, nullable=False)

    __table_args__ = (
        CheckConstraint(
            '(is_phishing = 1 AND spam_type IS NULL) OR (is_phishing = 0 AND description IS NULL)',
            name='chk_report_type_logic'
        ),
    )
    
    def __repr__(self):
        return f"<PhoneReport(phone_number='{self.phone_number}', is_confirmed={self.is_confirmed})>"