import os
import replicate
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Req(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"ok": True}

@app.post("/generate")
def generate(req: Req):
    model = os.getenv("MODEL_ID", "google/nano-banana-pro")
    output = replicate.run(
        model,
        input={"prompt": req.prompt}
    )
    return {"output": output}
