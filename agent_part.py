from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time
from workspace.user import User
from langchain.schema import (
    SystemMessage)
from workspace.dialogue_simulator import DialogueSimulator
from workspace.bid_system.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.dialogue_agent import DialogueAgent
from workspace.prompts.action_plan_prompt import ACTION_PLAN_PROPOSER_HEADER_TEMPLATE, ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE
import os
from workspace.moderator_speaker import ModeratorSpeaker
from workspace.prompts.moderator_prompt import AGENT_MODERATOR_HEADER_TEMPLATE,\
                    AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE


os.environ['OPENAI_API_KEY'] = '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'



def main():

    load_dotenv()
    agent_names = ['Action Plan Proposer']
    word_limit = 500
    user = User("user_name", "user_email", "user_password")


    moderator_speaker = ModeratorSpeaker()
    bidding_template = moderator_speaker.generate_agent_moderator_template(
                                        ACTION_PLAN_PROPOSER_HEADER_TEMPLATE)
    action_system_message = SystemMessage(
        content= ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE.format(
                                                agent_name = agent_names[0],
                                                agent_header = ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,
                                                word_limit = word_limit) 
                                                )
    
    moderator_system_message = SystemMessage(
        content= AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE)
    
    agent = DialogueAgent(name = agent_names[0], 
                        system_message = action_system_message,
                        model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k"),
                        user = user,
                        version = 1.0,
                        id = 1
                        )
    
    moderator = BiddingDialogueAgent(name = "Moderator",
                                    system_message = moderator_system_message,
                                    bidding_template = bidding_template,
                                    model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k"),
                                    user = user,
                                    version = 1.0,
                                    id = 1
                                    )
    agents = [agent,]
    simulator = DialogueSimulator(agents= agents, 
                                    selection_function=moderator_speaker.ask_for_agent,
                                    moderator = moderator)
    simulator.reset()

    agent_memory = ['Here is the conversation so far.']
    messages = []
    first_intro_of_the_agent = True
    while True:
        # if first_intro_of_the_agent == False: #HAS TO BE REMOVED
        #     with open('chat.txt','r') as file:
        #         data = file.readlines()
        #         for line in data:
        #             line = line.replace('\n','')
        #             agent_memory.append(f'user: {line}')
        #     first_intro_of_the_agent = True


        # print(agent_memory)
        if first_intro_of_the_agent == True:
            with open('chat.txt', 'r') as file:
                data = file.readlines()
            for line in data:
                line = line.replace('\n','')
                if ':' not in line:
                    mod_line = f'user: {line}'
                else:
                    name = line[0:line.index(':')]
                    if name not in agent_names:
                        value = line[line.index(':')+2:]
                        mod_line = line
                    elif name in agent_names:
                        value = line[line.index(':')+2:]
                        mod_line = line
                if mod_line not in agent_memory and name not in agent_names:
                    # print(f'MOD LINE : {[mod_line]}')
                    # print(f'AGENT MEMORY: {agent_memory}')
                    simulator.inject_history(agent_memory)
                   
                    messages.append({'role':'user', 'content':line})

                    simulator.inject(f'{name}', value)
                
                    names, assistant_responses = simulator.step()
                    iteration = 0
                    for name, assistant_response in zip(names, assistant_responses):
                        full_responce = ''
                        for chunk in assistant_response.split():
                            full_responce += chunk + ' '
                        iteration+=1

                        with open('chat.txt', 'a') as file:
                            if '\n' in full_responce:
                                full_responce_list = full_responce.split('\n')
                                full_responce = ' '.join(full_responce_list)
                                value_to_write = f'{name}:{full_responce}\n'
                            elif '\n' not in full_responce:
                                value_to_write = f'{name}: {full_responce}\n'

                            file.write(value_to_write)
                    
                    print(f'Agent memory in the end: {agent_memory}')



                        
                      
                        



                        
main()