import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import SecretStr
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms.base import LangchainLLMWrapper
from ragas.testset import TestsetGenerator
import nltk

from conftest import config

PPX_KEY = config[""]
OPENAPI_KEY = config[""]

base_dir = Path(__file__).resolve().parent
directory = base_dir / "documents"
print(f"Path for documents --->>{directory}")
print(f"Path for nltk --->>{base_dir.parent /"nltk_data"}")
nltk.data.path.append(base_dir.parent /"nltk_data")

client = ChatOpenAI(
    api_key=SecretStr(OPENAPI_KEY),
    model="gpt-4o-mini",
    temperature=0,
)
llm_langchain = LangchainLLMWrapper(client)
embeddings = OpenAIEmbeddings(api_key=SecretStr(OPENAPI_KEY), model="text-embedding-3-small")
loader = DirectoryLoader(
    path=str(directory),
    glob="**/*.docx",
    loader_cls=UnstructuredWordDocumentLoader
)
docs = loader.load()
generate_embeddings = LangchainEmbeddingsWrapper(embeddings)
generator = TestsetGenerator(llm=llm_langchain, embedding_model=generate_embeddings)
data_set = generator.generate_with_langchain_docs(docs, testset_size=20)
print(data_set.to_list())
