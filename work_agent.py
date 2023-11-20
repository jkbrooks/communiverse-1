import langchain
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)
from message_pull import MessagePuller
import pandas as pd
import requests

class Worker_Agent():
    def __init__(self, agent_name,\
                agent_id, agent_user,\
                agent_cls_ver_num, agent_cls_mod_num,\
                chat_model, current_concern):
        
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.agent_user = agent_user
        self.agent_cls_ver_num = agent_cls_ver_num
        self.agent_cls_mod_num = agent_cls_mod_num
        self.chat_model = chat_model
        self.current_task = None
        self.current_concern = current_concern
        self.message_history = []
        self.message_puller = None


    def register_with_filter(self, filter_agent):
        pass

    def pull_issues(self, repo_name, personal_token, issue_state, date_since = '2020-01-01T00:00:00Z', sort = 'updated'):
        """
        Pulls new messages from the GitHub ticket and updates the message history.
        """
        mp = MessagePuller(repo_name, personal_token, issue_state, date_since, sort)
        self.message_puller = mp
        mp.process_repo()
        dataframe_of_issues = pd.read_csv(f'{repo_name}.csv')
        return dataframe_of_issues


    def pull_comments(self, issue_id):
        issue_dict = self.mp.get_comments(issue_id)
        return issue_dict
    
    def curate_concerns_independently(self):
        pass

    def main_action_loop(self):
        pass

    def is_concern_is_relevant(self):
        pass

    def decide_action_based_on_concern(self):
        pass

    def take_action(self):
        pass

    def post_message_to_github_ticket(self, repo_name, personal_token, issue_num, user_name, response_title, response_content):
        owner = repo_name.split('/')[0]
        repo = repo_name.split('/')[1]
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_num}"
        payload = {
            "title": response_title,
            'body': response_content
        }

        r = requests.patch(url, auth=(user_name, personal_token), headers = {}, json=payload)

        print(r.json())
