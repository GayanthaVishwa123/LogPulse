from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth Service")

# React (Vite) සහ Next.js frontend ports වලට access දෙන්න:
origins = [
    "http://localhost:5173",  # 💡 Vite React App (CORS Fix)
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # Next.js / Standard React
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
