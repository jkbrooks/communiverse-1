
from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import shutil
from langchain.embeddings import HuggingFaceEmbeddings

dict_with_target_languages = {
    'Python' : Language.PYTHON,
    'PHP' : Language.PHP,
    'Proto' : Language.PROTO,
    'Java': Language.JAVA,
    'Javascript' : Language.JS,
    'JS': Language.JS,
    'Cobol':Language.COBOL,
    'C++':Language.CPP,
    'HTML':Language.HTML,
    'GO':Language.GO,
    'C#':Language.CSHARP,
    'Kotlin':Language.KOTLIN,
    'Rust':Language.RUST,
    'Swift':Language.SWIFT,
    'TypeScript':Language.TS
}


def clone_repo(path_to_save, url_to_repo):
    if os.path.isdir(path_to_save) == False:
            os.mkdir(path_to_save)
    else:
        if len(list(os.listdir(path_to_save))) > 0:
            shutil.rmtree(path_to_save)
    Repo.clone_from(url=url_to_repo, to_path=path_to_save)


def load_doc_and_process(path_to_the_specific_part, file_formats, target_language):
    try:
        language_for_parser = dict_with_target_languages[target_language]
    except:
        print(f'The {target_language} is not available.\
               List of available languages: {list(dict_with_target_languages.keys())},\
               switched to default option: Python.')
        language_for_parser = dict_with_target_languages['Python']

    loader = GenericLoader.from_filesystem(path = path_to_the_specific_part,
                                           glob = "**/*",
                                           suffixes= file_formats,
                                           parser = LanguageParser(language=language_for_parser, parser_threshold=400))
    
    documents = loader.load()
    documents_splitter = RecursiveCharacterTextSplitter.from_language(language = language_for_parser,
                                                             chunk_size = 2000,
                                                             chunk_overlap = 200)
    texts = documents_splitter.split_documents(documents)

    return texts


def get_embeddings(path_to_src_file, key, embedding_type = 'OpenAI', model_name = None):
    if path_to_src_file is not None:
        load_dotenv(path_to_src_file)
    if key is not None:
        os.environ["OPENAI_API_KEY"] = key

    if embedding_type == 'OpenAI':
            embeddings=OpenAIEmbeddings(disallowed_special=())
    elif embedding_type == 'HuggingFace':
        #just an example
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs)
    else:
        #other types of embeddings might be implemented.
        pass

    return embeddings

def create_vectordb(texts, embedding, persist_dir, db_type = 'Chroma'):
    if db_type == 'Chroma':
        vectordb = Chroma.from_documents(texts, embedding = embedding, persist_directory = persist_dir)
        vectordb.persist()
    else:
        #Other types of vector databases might be implemented
        pass
    return vectordb

def set_model_memory_and_qa(model_name, vectordb):
    llm = ChatOpenAI(model_name = model_name)
    memory = ConversationSummaryMemory(llm=llm, memory_key = "chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8}), memory=memory)

    return qa



def main(path_to_save, path_to_spec_part, url_to_repo,
        key, path_to_src_file, persist_dir,
        file_formats = ['.py'], target_language = 'Python', model_name = 'gpt-3.5-turbo'):
    clone_repo(path_to_save, url_to_repo)
    texts = load_doc_and_process(path_to_spec_part, file_formats, target_language)
    print(len(texts))
    embeddings = get_embeddings(path_to_src_file, key)
    vector_db = create_vectordb(texts, embeddings, persist_dir)
    qa = set_model_memory_and_qa(model_name, vector_db)
    while True:
        question = input(f'Enter your question: \nEnter <done> to stop.\n')
        if question == 'done':
            exit()
        result = qa(question)
        print(result['answer'])
        print('\n-------------------------------------\n')


if __name__ == '__main__':
    main('./test_repo', './test_repo/easynmt/', 'https://github.com/UKPLab/EasyNMT.git',
        key = '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', path_to_src_file=None, persist_dir='./data',
        )



