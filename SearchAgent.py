from langchain.agents import initialize_agent, AgentType, BaseSingleActionAgent
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
import os

class SearchAgent(BaseSingleActionAgent):
    def __init__(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.environ.get("OPENAI_API_KEY"), streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)

