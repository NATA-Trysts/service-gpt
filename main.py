import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class PromptBody(BaseModel):
    prompt: str


app = FastAPI()


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_prefix = "Given type object: \nchair_type = {\n  '1': 'chair'}\ntable_type = {\n  '2': 'chair'}\n"
prompt_surfix = "object follow this format: \n object_name = { 'name': '<object_capitalize_name>',  'color': '<object_color_based_on_propmt_in_hex>',  'type': '<object_type_based_on_object_name_in_lowercase_string>',  'id': '<object_id_based_on_object_type>'}"


@app.get("/")
def get_root():
    return {"message": "✌️"}


@app.post("/generate")
async def generate_object(body: PromptBody):
    complete_prompt = prompt_prefix + body.prompt + prompt_surfix
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=complete_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return {"completion": response}
