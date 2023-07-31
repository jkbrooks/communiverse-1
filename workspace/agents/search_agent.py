import os
from typing import Any
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

from langchain.tools import DuckDuckGoSearchRun


# This class represents a search agent
class SearchAgent:
    def __init__(self, tool: Any, llm: Any):
        self.search_agent = initialize_agent([tool], llm,
                                             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                                             handle_parsing_errors=True)
        
    def search(self, query) -> str:
        # Perform a search based on the given query
        response = self.search_agent.run(input=query)
        return response

    def get_results(self):
        # Retrieve the results of the last search
        pass
