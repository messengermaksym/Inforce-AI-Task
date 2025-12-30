from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, services
from database import engine, get_db, Base

# Створення таблиць при запуску
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Inforce AI Task - Gemini 2.5 SDK")


@app.post("/sessions")
def create_session(db: Session = Depends(get_db)):
    new_session = models.ChatSession(total_cost=0.0)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id}


@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: int, message_text: str, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Отримання історії для контексту
    history_records = db.query(models.Message).filter(models.Message.session_id == session_id).all()

    # Форматування історії під вимоги SDK
    chat_history = []
    for msg in history_records:
        # Відповідність ролей: 'user' та 'model'
        role = "user" if msg.role == "user" else "model"
        chat_history.append({"role": role, "parts": [{"text": msg.content}]})

    # Збереження вхідного повідомлення в базу
    user_msg = models.Message(session_id=session_id, role="user", content=message_text, tokens=0, cost=0.0)
    db.add(user_msg)
    db.commit()

    try:
        # Ініціалізація чату з історією
        chat = services.client.chats.create(
            model=services.MODEL_ID,
            history=chat_history
        )

        # Запит до моделі
        response = chat.send_message(message_text)

        # Розрахунок вартості на основі токенів
        usage = response.usage_metadata
        msg_cost = services.calculate_gemini_cost(usage.prompt_token_count, usage.candidates_token_count)

        # Фіксація відповіді та оновлення вартості сесії
        bot_msg = models.Message(
            session_id=session_id, role="assistant", content=response.text,
            tokens=usage.candidates_token_count, cost=msg_cost
        )
        db.add(bot_msg)

        session.total_cost += msg_cost
        db.commit()
        db.refresh(session)

        return {"answer": response.text, "total_cost": round(session.total_cost, 8)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}/history")
def get_history(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if not session: raise HTTPException(status_code=404, detail="Session not found")

    return {
        "total_accumulated_cost": round(session.total_cost, 8),
        "history": [{"role": m.role, "content": m.content, "cost": m.cost} for m in session.messages]
    }


@app.get("/", response_class=HTMLResponse)
async def get_ui():
    # Тестовий інтерфейс
    return """
    <!DOCTYPE html><html><head><title>Gemini 2.5 Chat</title>
    <style>body{font-family:sans-serif;max-width:600px;margin:auto;padding:20px;}#chat{border:1px solid #ccc;height:300px;overflow-y:auto;padding:10px;margin-bottom:10px;}</style></head>
    <body><h2>🚀 Gemini 2.5 Flash Chat</h2><div id="chat"></div>
    <input type="text" id="m" style="width:70%"><button onclick="send()">Send</button>
    <p>Cost: $<span id="c">0.00000000</span></p>
    <script>
        let sid = null;
        async function init(){ const r = await fetch('/sessions',{method:'POST'}); const d = await r.json(); sid = d.session_id; }
        init();
        async function send(){
            const i = document.getElementById('m'); const t = i.value; if(!t || !sid) return;
            document.getElementById('chat').innerHTML += `<div><b>Ви:</b> ${t}</div>`; i.value = '';
            const r = await fetch(`/sessions/${sid}/messages?message_text=${encodeURIComponent(t)}`,{method:'POST'});
            const d = await r.json();
            document.getElementById('chat').innerHTML += `<div><b>AI:</b> ${d.answer}</div>`;
            document.getElementById('c').innerText = d.total_cost.toFixed(8);
        }
    </script></body></html>
    """