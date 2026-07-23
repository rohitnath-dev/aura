import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import (
    CORSMiddleware
)
from core.user_manager import (
    create_user,
    save_profile
)
from core.faiss_manager import (
    build_user_faiss
)
from rag import app

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OnboardRequest(BaseModel):
    username: str
    profile_data: dict

class ChatRequest(BaseModel):
    username: str
    message: str

@server.get("/")
def root():
    return {
        "status": "online",
        "message": "AURA backend running"
    }

@server.post("/onboard")
def onboard(req: OnboardRequest):

    try:
        username = req.username.strip()
        if not username:
            return {
                "success": False,
                "message": "Username missing"
            }

        # create user structure
        create_user(username)

        # save raw profile
        save_profile(
            username,
            req.profile_data
        )

        # preprocess user data
        subprocess.run(
            [
                "python",
                "preprocess.py",
                username
            ],
            check=True
        )

        # build faiss
        build_user_faiss(username)
        return {
            "success": True,
            "message": (
                f"{username} clone created successfully"
            )
        }

    except Exception as e:
        print(e)
        return {
            "success": False,
            "message": str(e)
        }

@server.post("/chat")
def chat(req: ChatRequest):

    try:
        result = app.invoke({
            "username": req.username,
            "question": req.message
        })

        return {
            "response": result["answer"]
        }

    except Exception as e:
        print(e)
        return {

            "response": "Something went wrong."
        }
