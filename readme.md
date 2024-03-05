# Sparky Chatbot

## Overview

Sparky chatbot is a LLM-based chatbot built on top of [LlamaIndex](https://www.llamaindex.ai/) and [Rasa ](https://github.com/RasaHQ/rasa)utilizing LLM library for indexing, retrieval and context injection. A conversational-ai model is implemented to understand domain specific language in web3 and blockchain before processing to RAG.

![intro](/Users/aolin/Projects/sparky/chatbot/intro.svg)

## Install

Create a `.env` file and fill following configuration.

```
CMC_KEY=
OPENAI_API_KEY=
```

## Train Your model

Train your conversational-ai model with your nlu assets under `data` file.

```
rasa train
```

## Get started

Enable actions for indexing and querying LLM.

```
rasa run actions
```

Start Restful server and listen on the port.

```
rasa run --enable-api
```

