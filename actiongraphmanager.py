import time
import langchain
from templates.templates import ACTION_GRAPH_MANAGER_TEMPLATE
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
import networkx as nx
import threading


class ActionGraphManager():
    def __init__(self, chat_model):
        self.action_graph = None
        self.current_phase = None
        self.chat_model = chat_model


    def create_initial_action_graph(self, task_description):
        self.current_phase = 'Initial Planning'


    def parse_task_description(self, description):
        """
        Parses the task description to create a basic action graph.
        """
        action_graph = nx.DiGraph()
        action_gr_manager_system_message = SystemMessage(content=ACTION_GRAPH_MANAGER_TEMPLATE)
        action_gr_manager_human_message = HumanMessage(content=f'Generate a list of tasks and dictionary of corresponding\
                                                         subtasks for the following task description: {description}')
        response = self.chat_model.invoke([action_gr_manager_system_message, action_gr_manager_human_message])



        return action_graph
    

    def open_discussion_state(self):
        """
        Opens the floor for discussion to other agents.
        This could involve messaging systems, database updates, etc.
        """
        self.current_phase = "Discussion"
        # Implementation to notify other agents and invite comments


    def update_action_graph(self, new_graph):
        """
        Updates the action graph based on input from the discussion phase.
        """
        # This could involve complex logic to merge the new graph with the existing one
        self.action_graph = new_graph

    def assign_tasks(self):
        """
        Assigns tasks from the action graph to AI agents, human workers, or customers.
        """
        self.current_phase = "Assignment"
        # Implementation of task assignment logic

    def execute_tasks(self):
        """
        Executes the tasks assigned in the ActionGraph.
        In practice, this would involve coordinating with various agents and tracking progress.
        """
        self.current_phase = "Execution"
        # Task execution logic



    def open_discussion_phase(self, duration, update_interval_minutes, update_interval_messages):
        """
        Opens the floor for discussion to other agents for a specified duration.
        Updates the action graph at specified intervals based on messages from the Github Issue.
        """
        self.current_phase = "Discussion"
        self.notify_worker_agents()  # Notify WorkerAgents that the discussion phase is open
        self.start_time = time.time()
        self.duration = duration
        self.update_interval_minutes = update_interval_minutes
        self.update_interval_messages = update_interval_messages
        self.message_count = 0

        # Start a background thread to update the action graph at regular intervals
        threading.Thread(target=self.update_action_graph_periodically).start()


    def update_action_graph_periodically(self):
        """
        Periodically checks if the action graph should be updated based on time or message count from Github Issue.
        """
        while time.time() - self.start_time < self.duration:
            time.sleep(60)  # Wait for 1 minute before checking again

            # Check if update is needed based on time or message count
            if time.time() - self.last_update_time >= self.update_interval_minutes * 60 or \
               self.message_count >= self.update_interval_messages:
                self.update_action_graph_based_on_github_issue()
                self.last_update_time = time.time()
                self.message_count = 0



    def update_action_graph_based_on_github_issue(self):
        """
        Updates the action graph based on the current discussion in the Github Issue.
        """
        # Placeholder for the logic to update the action graph.
        # This would involve querying the Github Issue for new messages and processing them.
        # Example: self.action_graph = updated_graph_based_on_github_discussion()



    def poll_github_issue(self):
        """
        Polls the Github Issue for new messages.
        This method would be responsible for incrementing the message count
        and possibly storing the content of new messages for processing.
        """
        # Implementation to poll Github Issue for new messages
        # Increment message count and store messages for processing
        new_messages = self.get_new_messages_from_github_issue()
        self.message_count += len(new_messages)
        # Store or process new messages as needed