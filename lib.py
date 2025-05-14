import syslib
from prompts import *

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain_gigachat import GigaChat
from langchain_gigachat.embeddings import GigaChatEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import load_prompt
# from langchain_community.document_loaders.parsers.language.java import

def get_zephyr(file_path, encoding='windows-1251'):
    __loader = CSVLoader(
        file_path=file_path,
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
        },
        encoding=encoding
    )
    data = __loader.load()
    print(f'loaded {len(data)} tests.')

    return data

def get_doc(file_path, encoding='utf-8'):
    return TextLoader(file_path=file_path, encoding=encoding).load()

def get_splitted_doc(file_path, chuck_size = 1000, chuck_overlap=200, separator="\n", encoding='utf-8'):
    data = TextLoader(file_path=file_path, encoding=encoding).load()
    return (CharacterTextSplitter(chunk_size=chuck_size, chunk_overlap=chuck_overlap, separator=separator)
            .split_documents(data))

def split_data(data, chuck_size = 1000, chuck_overlap=200, separator="\n"):
    return (CharacterTextSplitter(chunk_size=chuck_size, chunk_overlap=chuck_overlap, separator=separator)
            .split_documents(data))

def get_docs(file_path, glob="**/[!.]*", encoding='utf-8'):
    return DirectoryLoader(path=file_path, glob=glob, loader_cls=TextLoader, loader_kwargs={'encoding': encoding}, recursive=True).load()

def get_llm(model='GigaChat-2-Pro', temperature = 0.5):
    return GigaChat(
        base_url="https://gigachat-ift.sberdevices.delta.sbrf.ru/v1",
        cert_file="certs/published.pem",
        key_file="certs/client.key",
        key_file_password="giga12",
        verify_ssl_certs=False,
        temperature=temperature,
        profanity_check=False,
        model=model,
        # top_p=0.0,
        # repetition_penalty=1.0,
    )

def get_emb():
    return GigaChatEmbeddings(
        base_url='https://gigachat-ift.sberdevices.delta.sbrf.ru/v1',
        cert_file="certs/published.pem",
        key_file="certs/client.key",
        key_file_password="giga12",
        verify_ssl_certs=False,
        model="EmbeddingsGigaR"
    )

def format_docs(__docs):
    return "\n\n".join(__doc.page_content for __doc in __docs).replace('"', '')


def llm_get_objects(request, llm):
    __prompt = load_prompt('./prompts/objects_selecting.yaml')
    __chain = __prompt | llm | StrOutputParser()
    return __chain.invoke(
        {"request": request}
    )

def llm_get_step_objects(request, llm):
    __prompt = load_prompt('./prompts/step_objects_selecting.yaml')
    __chain = __prompt | llm | StrOutputParser()
    return __chain.invoke(
        {"request": request}
    )

def llm_get_verification_questions_chain(llm):
    __prompt = PromptTemplate.from_template(VERIFICATION_QUESTION_PROMPT)
    return __prompt | llm | StrOutputParser()

def llm_get_verification_answers_chain(llm):
    __prompt = PromptTemplate.from_template(VERIFICATION_ANSWERS_PROMPT)
    return __prompt | llm | StrOutputParser()
