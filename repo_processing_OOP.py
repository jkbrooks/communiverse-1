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
import openai

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
# openai.organization = 'org-xT7Rl1SPFD8rooH2zEY7jrcO'

class RepoProcessor():
    def __init__(self, key_or_path_to_bash_file):
        if key_or_path_to_bash_file[:2] == 'sk':
            self.key = key_or_path_to_bash_file
            os.environ["OPENAI_API_KEY"] = self.key
            self.path_to_env_file = None
        else:
            self.key = None
            self.path_to_env_file = key_or_path_to_bash_file
            load_dotenv()

    def set_llm(self, model_name):
        if 'gpt' in model_name:
            self.llm = ChatOpenAI(model_name = model_name)
        else: 
            self.llm = None
        
    def clone_repo(self, repo_url, path_to_save):
        if os.path.isdir(path_to_save) == False:
            os.mkdir(path_to_save)
        else:
            if len(list(os.listdir(path_to_save))) > 0:
                shutil.rmtree(path_to_save)
                os.mkdir(path_to_save)
        
        self.path_to_save = path_to_save

        Repo.clone_from(url = repo_url, to_path=path_to_save)
    

    def load_doc_and_process(self, path_to_part_of_repo, file_formats, target_language):
        try:
            language_for_parser = dict_with_target_languages[target_language]
        except:
            print(f'The {target_language} is not available.\
                List of available languages: {list(dict_with_target_languages.keys())},\
                switched to default option: Python.')
            language_for_parser = dict_with_target_languages['Python']
        loader = GenericLoader.from_filesystem(path = os.path.join(self.path_to_save,path_to_part_of_repo),
                                           glob = "**/*",
                                           suffixes= file_formats,
                                           parser = LanguageParser(language=language_for_parser, parser_threshold=400))
    
        documents = loader.load()
        documents_splitter = RecursiveCharacterTextSplitter.from_language(language = language_for_parser,
                                                             chunk_size = 2000,
                                                             chunk_overlap = 200)
        texts = documents_splitter.split_documents(documents)

        self.texts = texts
    

    def set_embeddings(self, embedding_type = 'OpenAI', model_name = None):
        
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
        
        self.embeddings = embeddings

    def set_vector_db(self, save_dir, db_type = 'Chroma'):
        if db_type == 'Chroma':
            vectordb = Chroma.from_documents(self.texts,
                                            embedding = self.embeddings,
                                            persist_directory = save_dir)
            vectordb.persist()
            
        else:
            #Other types of vector databases might be implemented
            pass
        
        self.vectordb = vectordb

    def set_memory_and_qa(self):
        self.memory = ConversationSummaryMemory(llm = self.llm,
                                                memory_key='chat_history',
                                                return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(self.llm,
                                                        retriever=self.vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8}),
                                                        memory=self.memory)
        
    def qa_step(self, input_question):
        result = self.qa(input_question)
        return result
    




if __name__ == '__main__':
    RP = RepoProcessor('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')
    RP.clone_repo(repo_url='https://github.com/neonbjb/tortoise-tts.git', path_to_save='test_repo')
    RP.load_doc_and_process('scripts', file_formats=['.py'], target_language='Python')
    RP.set_llm('gpt-3.5-turbo')
    RP.set_embeddings()
    RP.set_vector_db('./data')
    RP.set_memory_and_qa()
    while True:
        question = input(f'Enter your question: \nEnter <done> to stop.\n')
        if question == 'done':
            exit()
        result = RP.qa_step(question)
        print(result['answer'])
        print('\n-------------------------------------\n')


        
        