from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage,ServiceContext,KeywordTableIndex
from llama_index.llms import OpenAI

from llama_index.llms.llama_api import LlamaAPI
import openai
from llama_index.memory import ChatMemoryBuffer
import os
from dotenv import dotenv_values

class Agent:
    def __init__(self):
        config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
        OPENAI_API_KEY = config.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY
        openai.api_key = OPENAI_API_KEY
        documents = SimpleDirectoryReader("rag").load_data()
        index = VectorStoreIndex.from_documents(documents)
        llm = OpenAI(model="gpt-3.5-turbo-1106", temperature=0)
        service_context = ServiceContext.from_defaults(llm=llm)
        memory = ChatMemoryBuffer.from_defaults(token_limit=15000)
        agent = "Sparky"
        organization = "Sparky Lab"
        
        # chat_engine = index.as_chat_engine(chat_mode="condense_question",service_context=service_context, memory=memory)
        self.chat_engine = index.as_chat_engine(
                chat_mode="context",
                service_context=service_context,
                memory=memory,
    system_prompt = [
        {
            "role": "system",
            "content": f"""[AGENT]:
I am {agent} a very kind and enthusiastic customer support agent who loves to help customers. I am working on the behalf of "{organization}"

Given the following document from "{organization}", I will answer the [USER] questions combining the [DOCUMENT] and following the [RULES].

[DOCUMENT]:
{documents}

[RULES]:
I will answer the user's questions trying to combine the [DOCUMENT] provided. I will abide by the following rules:
- I am a kind and helpful human, the best customer support agent in existence
- I will refer title of [DOCUMENT] when use it.
""",
        }
    ]
            )
