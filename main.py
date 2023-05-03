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

openai.api_key = ""

prompt_prefix_1 = "Given type object: \nchair_type = {\n  '1': 'chair'}\ntable_type = {\n  '2': 'desk'}\plant_type = {\n  '3': 'plant'}\ndecoration_type = {\n  '4': 'decoration'}\ncabinet_type = {\n  '5': 'cabinet'}\nbath_type = {\n  '6': 'bath'}\n"
prompt_prefix_2 = "Given list of uuids, must use this uuid corresponding to the object uuid: \n'desk-d61cf1db-b68e-4e4e-9bbd-797962b63dbf': Accent Table\n'plant-10680d63-f2cf-4f30-ae45-3d309f4e4464': Apple Tree\n'decoration-b186a8a9-9e0e-483e-9779-18abfe477fa3': Art Board\n'bath-2c419d45-c99e-45d6-8554-f0dbcaf4a6cd': Bath\n'chair-868c1619-2cdf-4249-bb74-2c9309def2a2': Bean Bag Chair Coffee\n'chair-908ea24b-1e9f-47b2-973b-a6c4128b3f7f': Bean Bag Chair\n'cabinet-41223ee1-e7fd-48a0-ab74-677eae6a78b2': Bed Cabinet\n'decoration-308b504b-d99a-4005-a265-503b2de768e5': Book shelf\n'decoration-4781c552-af73-4d69-bbab-33b21bfcb77a': Bubble Lamp\n'cabinet-a99b7fbf-37f3-49a1-8657-d0bcc2997d98': Cabinet Bathroom\n'cabinet-29524f5b-0486-446e-a01f-181c4b7e5402': Cabinet Book\n'cabinet-28f52db2-46da-4bb1-86da-ef5d256099ff': Cabinet\n'decoration-26e29954-007d-408f-9243-86c518bfc035': Carpet\n'chair-bf76df41-9c51-4ae4-8d26-6a54e0e2265d': Chair\n'desk-68eccc2e-9d7b-4c66-972e-9aca69b76505': Circle Table\n'desk-58d0bc2c-871f-45ae-a73d-178c0ad41f31': Computer Table\n'chair-5b879d1e-ca56-49e2-8af8-f348dc043f03': Dinning Chair\n'desk-bb79046f-20c9-4eb3-b527-5470bfe8e967': Dinning Table\n'decoration-1510441a-f8e8-444e-aea8-cc530a0fedb6': Double Bed\n'decoration-3e35cb45-7d05-474d-8529-663638698841': Fan\n'cabinet-d6ad2e25-e3ef-407f-aeda-496c067b3762': Kitchen Cabinet\n'decoration-52dfe16a-b978-43bb-b90b-1981b8be5d6e': Kitchen Rug\n'decoration-3fca352a-ef32-42af-ac04-fa045253c5d2': Kitchen Shelf\n'decoration-792e50e3-5999-4589-a9cc-e3a1a0a3b5c7': Leaf Plant\n'chair-312d6ba3-6e09-42c6-af59-6d4a7d9325d5': Leather Sofa\n'decoration-a956af13-de12-4bf7-8871-04db2b847402': One Leg Lamp\n'chair-73a25ea2-3079-4c49-9673-6675cfaa32a2': Park Bench\n'decoration-d414bcda-2df6-48c3-9ba6-8017925e733f': Pattern Rug\n'decoration-56fb707b-8b61-4feb-af13-f90544fc4a15': Pear Tree\n'decoration-628e56c5-095b-4e55-9989-d4a3696afec6': Refrigerator\n'chair-c266dcd6-0dfe-49a1-be25-cf5c9161ae52': Relax Chair\n'decoration-4504276e-81f1-4882-97af-7b86d604c36d': Shiba\n'chair-0b9eb21c-5a3f-4e71-b914-e817cc5ecd0e': Sofa\n'decoration-1776bb75-87b3-4cad-ac68-1105e4a4ceb3': Triangle Pattern Rug\n'decoration-fd9ee033-e41c-4210-8e6b-de57e90bf23a': TV Stand\n"
prompt_surfix = "object follow this format: \n object_name = { 'name': '<object_capitalize_name>',  'color': '<object_color_based_on_propmt_in_hex>',  'type': '<object_type_based_on_object_name_in_lowercase_string>',  'uuid': '<object_id_from_object_type_and_list_of_uuid>'}"


@app.get("/")
def get_root():
    return {"message": "✌️"}


@app.post("/generate")
async def generate_object(body: PromptBody):
    complete_prompt = prompt_prefix_1 + prompt_prefix_2 + body.prompt + prompt_surfix
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
