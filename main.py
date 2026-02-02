import os
import replicate
from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
    try:
        output = replicate.run(model, input={"prompt": req.prompt})
        return {"output": output}
    except Exception as e:
        msg = str(e)

        # Если нет кредитов (Replicate обычно пишет Insufficient credit / status 402)
        if "Insufficient credit" in msg or "status: 402" in msg or "402" in msg:
            return JSONResponse(
                status_code=402,
                content={
                    "error": "insufficient_credit",
                    "message": "На Replicate недостаточно кредитов. Пополни Billing и повтори запрос.",
                },
            )

        return JSONResponse(
            status_code=500,
            content={"error": "replicate_error", "message": msg},
        )
