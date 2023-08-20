from langchain.schema import (
    SystemMessage)
import numpy as np

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time

from workspace.user import User

from workspace.dialogue_simulator import DialogueSimulator

from workspace.moderator_speaker import ModeratorSpeaker
from workspace.bid_system.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.bid_system.bid_output_parser import BidOutputParser
from workspace.bid_system.bid_speaker import Speaker
from workspace.dialogue_agent import DialogueAgent

from workspace.prompts.action_plan_prompt import ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,\
                    ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE

from workspace.prompts.moderator_prompt import AGENT_MODERATOR_HEADER_TEMPLATE,\
                    AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE
from workspace.prompts.commander_prompt import COMMANDER_SYSTEM_MESSAGE_TEMPLATE,\
                    AGENT_COMMANDER_TEMPLATE
from workspace.prompts.discussant_prompt import DISCUSSANT_SYSTEM_MESSAGE_TEMPLATE,\
                    AGENT_DISCUSSANT_TEMPLATE

def select_next_speaker(step, agents) -> int:
        print(f"STEP: {step}")
        bid_speaker = Speaker()
        for agent in agents:
            if agent.name == "Action Plan Proposer":
                stage_string = bid_speaker.parse(agent.get_stage())['bid']
                print(stage_string)

        print(f'Estimated stage: {stage_string}')
        if step > 0 and int(stage_string) == 4:
            
            
            bids = []
            for agent in agents:
                if agent.name == 'Action Plan Proposer':
                    continue
                bid = int(bid_speaker.parse(agent.bid())['bid'])
                print(f'{agent.name} - {bid}')
                bids.append(bid)

            # randomly select among multiple agents with the same bid
            print(bids)
            
            max_value = np.max(bids)
            max_indices = np.where(bids == max_value)[0]
            idx = np.random.choice(max_indices)+1

            print("Bids:")
            for i, (bid, agent) in enumerate(zip(bids, agents)):
                if agent.name == 'Action Plan Proposer':
                    continue
                print(f"\t{agent.name} bid: {bid}")
                if i == idx:
                    selected_name = agent.name
            print(f"Selected: {selected_name}")
            print("\n")

            return idx
        elif step == 0 or int(stage_string) < 4 or int(stage_string) == 5:
            idx = 0
            return idx

def load_agents():
    
    load_dotenv('~/.zshrc')

    agent_names = ["Action Plan Proposer", "Commander Bob", "Discussant Jack"]




    word_limit = 500

    action_system_message = SystemMessage(
        content= ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE.format(
                                                agent_name = agent_names[0],
                                                agent_header = ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,
                                                word_limit = word_limit) 
                                                )

    formatted_agent_names = ', '.join(agent_names)
    chat_description = f"The members of conversation are {formatted_agent_names}"

    commander_system_message = SystemMessage(
        content= COMMANDER_SYSTEM_MESSAGE_TEMPLATE.format(
                                                agent_name = agent_names[1],
                                                agent_header = 
                                                    AGENT_COMMANDER_TEMPLATE.format(
                                                        chat_description = chat_description),
                                                word_limit = word_limit) 
                                                )

    disscusant_system_message = SystemMessage(
        content= DISCUSSANT_SYSTEM_MESSAGE_TEMPLATE.format(
                                                agent_name = agent_names[2],
                                                agent_header = 
                                                    AGENT_DISCUSSANT_TEMPLATE.format(
                                                        chat_description = chat_description),
                                                word_limit = word_limit) 
                                                )

    moderator_system_message = SystemMessage(
        content= AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE)

    moderator_speaker = ModeratorSpeaker()
    bid_parser_object = BidOutputParser()
    bidding_template_action_plan_proposer = bid_parser_object.generate_agent_bidding_template(agent_header =[ACTION_PLAN_PROPOSER_HEADER_TEMPLATE])
    bidding_template_action_commander = bid_parser_object.generate_agent_bidding_template(AGENT_COMMANDER_TEMPLATE.format(
                                                        chat_description = chat_description))
    bidding_template_action_plan_discussant = bid_parser_object.generate_agent_bidding_template(AGENT_DISCUSSANT_TEMPLATE.format(
                                                        chat_description = chat_description))

    stage_template_action_plan_proposer = bid_parser_object.generate_stage_template(ACTION_PLAN_PROPOSER_HEADER_TEMPLATE)


    # bidding_template = moderator_speaker.generate_agent_moderator_template(
    #                                     AGENT_MODERATOR_HEADER_TEMPLATE)

    # bidding_template_commander = moderator_speaker.generate_agent_moderator_template()

    # bidding_template_disscusant = moderator_speaker

    user = User("user_name", "user_email", "user_password")
        
    agent = DialogueAgent(name = agent_names[0], 
                        system_message = action_system_message,
                        model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k"),
                        user = user,
                        version = 1.0,
                        id = 1,
                        bidding_template=bidding_template_action_plan_proposer,
                        stage_template=stage_template_action_plan_proposer
                        )

    agent_commander = DialogueAgent(name = agent_names[1], 
                    system_message = commander_system_message,
                    model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k"),
                    user = user,
                    version = 1.0,
                    id = 1,
                    bidding_template=bidding_template_action_commander
                    )

    agent_disscusant = DialogueAgent(name = agent_names[2], 
                system_message = disscusant_system_message,
                model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k"),
                user = user,
                version = 1.0,
                id = 1,
                bidding_template =bidding_template_action_plan_discussant
                )


    agents = [agent, agent_commander, agent_disscusant]
    simulator = DialogueSimulator(agents= agents, 
                                    selection_function=select_next_speaker)
    
    return simulator