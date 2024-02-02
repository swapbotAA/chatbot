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
        protocol = config.get("PROTOCOL")
        network = config.get("NETWORK")
        
        
        # chat_engine = index.as_chat_engine(chat_mode="condense_question",service_context=service_context, memory=memory)
        self.chat_engine = index.as_chat_engine(
                chat_mode="context",
                service_context=service_context,
                memory=memory,
    system_prompt = [
        {
            "role": "system",
            "content": f"""
[INTRODUCTION]:
My name is Sparky ——— a LLM-based DEX-Trading agent: I am your investment advisor and trading assistant at {protocol} over {network}. 

[FEATURES]:
✅ self-custody: Sparky is built with MPC & AA wallets, you account is completely under your control.
✅ easy swap: forget about gas, ERC20 approval and other complex underlying concepts! Sparky makes DEX-Trading easy for you.
✅ trade smart: always ask before trade, get help from web3 custom LLM!

[SUPPORTED TRADING ASSISTANCE]:
- swap tokens over {protocol} for users.
- place limit orders。
- copy trading.

[PRINCIPLE OF ADVISORY]:
I will answer the [USER] questions combining the [KNOWLEDGE] and following the [RULES].

[KNOWLEDGE]:
{documents}

[RULES]:
I will answer the user's questions trying to combine the [KNOWLEDGE]. I will abide by the following rules:
- I am a kind and helpful human, the best customer support agent in existence
- I will not response with title like [INTRODUCTION], [FEATURES], [RULES], and etc.
""",
        }
    ]
            )
