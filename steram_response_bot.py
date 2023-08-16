import asyncio
from typing import Any, Dict, List
import time
from langchain.chat_models import ChatOpenAI
from langchain.schema import LLMResult, HumanMessage
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
from dotenv import load_dotenv
from fastapi import WebSocket
import openai
import streamlit

_ = load_dotenv()


class MyCustomSyncHandler(BaseCallbackHandler):

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        pass
        # if (self.response__.split('\n')[-1]+token).__len__() > 80:
        #     self.response__ += '\n'
        #     pass
        # self.response__ += token
        # with self.container:
        #     self.container.empty()
        #
        #     # streamlit.empty()
        #     # streamlit.text(token)
        #     self.container.text(self.response__)
        #     streamlit.text(">abc")
        # time.sleep(3)


class MyCustomAsyncHandler(AsyncCallbackHandler):
    """Async callback handler that can be used to handle callbacks from langchain."""

    def __init__(self, client: WebSocket, *args, **kwargs):
        self.client_socket = client

    async def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when chain starts running."""
        print("zzzz....")
        await asyncio.sleep(0.3)
        # class_name = serialized["name"]
        # print(serialized, prompts)
        # print("Hi! I just woke up. Your llm is starting")

    async def on_llm_new_token(
        self,
        token: str,
        *,
        run_id,
        parent_run_id = None,
        tags = None,
        **kwargs: Any,
    ) -> None:
        await self.client_socket.send_text(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when chain ends running."""
        print("zzzz....")
        await asyncio.sleep(0.3)
        # print("Hi! I just woke up. Your llm is ending")


# To enable streaming, we pass in `streaming=True` to the ChatModel constructor
# Additionally, we pass in a list with our custom handler

def get_async_response(user_query, client_socket: WebSocket):
    chat = ChatOpenAI(
        max_tokens=1000,
        streaming=True,
        callbacks=[MyCustomAsyncHandler(client_socket)],
    )
    return chat.agenerate([[HumanMessage(content=user_query)]])
