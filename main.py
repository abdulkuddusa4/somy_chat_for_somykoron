import types

import streamlit
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
import streamlit as st
from steram_response_bot import MyCustomAsyncHandler, MyCustomSyncHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

# w = WebSocket()

# from fastapi.requests import R

app = FastAPI()

# @types.coroutine
# async def ff():
#     for i in range(10):
#         print(i)
#         yield

system_prompt = "Your are given a text_document_data enclosed in ``` ```." \
                "Your job is to answer the user question based on the text_document_data enclosed in ```` ```." \
                "the user's question is enclosed in  <|start|>  <|end|>\n." \
                "text_document_data: ``` {document} ```" \
                "users question: <|start|> {query} <|end|>" \
                "Note: Plz do not answer to the question's not related to the document"


def get_file_data(file):
    with open(f'uploaded_files/{file}') as file:
        text = ''.join(file.readlines())
    return text


@app.websocket("/talk/{document_id}")
async def home(websocket: WebSocket, document_id):
    print(await websocket.accept())
    if not document_id in os.listdir('uploaded_files'):
        await websocket.send_text(f"the document {document_id} not found")
        await websocket.close()

    document_data = get_file_data(document_id)
    chat = ChatOpenAI(
        max_tokens=1000,
        streaming=True,
        callbacks=[MyCustomAsyncHandler(websocket)],
    )
    while True:
        data = await websocket.receive_text()
        print(f"user_msg---{data}")
        # prompt = system_prompt.format()
        print(await chat.agenerate(
            [[HumanMessage(content=system_prompt.format(document=document_data, query=data))]]
        ))


@app.post('/upload/')
async def upload_file(uploadedfile: UploadFile):
    print(f"---> {uploadedfile.filename}")
    with open(f"uploaded_files/{uploadedfile.filename}", 'wb') as w_file:
        contents = await uploadedfile.read()
        w_file.write(contents)
    return "file saved"
    # return await get_async_response(system_prompt.format(document=text_, query=user_query), st)
    # print(await request.json())

    # return f"hellow"


# with st.chat_message("user"):
#     msg = st.chat_input('say something')
#     st.write(f"your msg was {msg}")
import time

# msg = st.chat_input('say_something')
# from steram_response_bot import get_async_response
# text_ = ""
# with open('query_context', 'r') as file:
#     text_ = "".join(file.readlines())
#     # print(text_)
#
# if msg:
#     print("agent called")
#     get_async_response(system_prompt.format(document=text_, query=msg), st)
