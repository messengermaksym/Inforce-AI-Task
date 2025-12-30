from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    total_cost = Column(Float, default=0.0) # [cite: 7, 12]
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String) # 'user' або 'assistant'
    content = Column(Text)
    tokens = Column(Integer) # [cite: 7, 11]
    cost = Column(Float)     # [cite: 7, 11]
    session = relationship("ChatSession", back_populates="messages")