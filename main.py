import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class PromptBody(BaseModel):
    prompt: str


app = FastAPI()


origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_surfix = "{ name: '<object_name>', color: '<object_color_in_hex>', position: [0,0,0], rotation: [0,0,0] }"


@app.get("/")
def get_root():
    return {"message": "✌️"}


@app.post("/generate")
async def generate_object(body: PromptBody):
    complete_prompt = body.prompt + prompt_surfix
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=complete_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return {"choise": response}
