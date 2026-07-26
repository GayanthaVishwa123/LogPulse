from fastapi import FastAPI

app = FastAPI(title="Processor Service")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
