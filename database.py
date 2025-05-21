from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///chat_memory.db"  # change to postgres URL if needed

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ChatMemory(Base):
    __tablename__ = "chat_memory"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=False)
    message = Column(Text)

def init_db():
    Base.metadata.create_all(engine)

def store_chat(email, message):
    with Session() as session:
        entry = ChatMemory(email=email, message=message)
        session.add(entry)
        session.commit()

def get_history(email):
    with Session() as session:
        rows = session.query(ChatMemory).filter_by(email=email).all()
        return [{"role": "user", "content": r.message} for r in rows]
