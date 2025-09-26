from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

class QAInput(BaseModel):
    question: str
    context: str

@app.post("/predict")
def predict(data: QAInput):
    result = qa_pipeline(question=data.question, context=data.context)
    return {"answer": result["answer"], "score": result["score"]}
