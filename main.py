from fastapi import FastAPI
import microwave.router
import auth.router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router.router, tags=["Authentication"])
app.include_router(microwave.router.router, prefix="/microwave", tags=["Microwave"])
