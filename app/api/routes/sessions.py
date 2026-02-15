"""
Ендпоінти для сесій чату та повідомлень.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChatSession, Message
from app.services import get_client, calculate_gemini_cost, get_model_id

router = APIRouter()


@router.post("")
def create_session(db: Session = Depends(get_db)):
    new_session = ChatSession(total_cost=0.0)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id}


@router.post("/{session_id}/messages")
async def send_message(session_id: int, message_text: str, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    history_records = db.query(Message).filter(Message.session_id == session_id).all()
    chat_history = []
    for msg in history_records:
        role = "user" if msg.role == "user" else "model"
        chat_history.append({"role": role, "parts": [{"text": msg.content}]})

    user_msg = Message(
        session_id=session_id, role="user", content=message_text, tokens=0, cost=0.0
    )
    db.add(user_msg)
    db.commit()

    try:
        client = get_client()
        chat = client.chats.create(model=get_model_id(), history=chat_history)
        response = chat.send_message(message_text)

        usage = response.usage_metadata
        msg_cost = calculate_gemini_cost(
            usage.prompt_token_count, usage.candidates_token_count
        )

        bot_msg = Message(
            session_id=session_id,
            role="assistant",
            content=response.text,
            tokens=usage.candidates_token_count,
            cost=msg_cost,
        )
        db.add(bot_msg)
        session.total_cost += msg_cost
        db.commit()
        db.refresh(session)

        return {"answer": response.text, "total_cost": round(session.total_cost, 8)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/history")
def get_history(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "total_accumulated_cost": round(session.total_cost, 8),
        "history": [
            {"role": m.role, "content": m.content, "cost": m.cost}
            for m in session.messages
        ],
    }
