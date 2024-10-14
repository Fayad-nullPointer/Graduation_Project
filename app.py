from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import joblib
pipe=joblib.load('chatbot_model.pkl')
app = FastAPI()

# Template directory
templates = Jinja2Templates(directory="template")

# Dummy chatbot model function (for now)
def chatbot_model(text: str) -> str:
    prediction = pipe.run(
        query=text, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
        )
    chatbot_response =prediction['answers'][0].context
    return chatbot_response
        
   

# Request body model for the API
class ChatInput(BaseModel):
    text: str

@app.post("/api/chat")
async def chat(input: ChatInput):
    response = chatbot_model(input.text)
    return {"response": response}

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
