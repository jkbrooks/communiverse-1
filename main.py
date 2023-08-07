from langchain.schema import (
    SystemMessage)

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

from workspace.user import User

from workspace.dialogue_simulator import DialogueSimulator

from workspace.moderator_speaker import ModeratorSpeaker
from workspace.bid_system.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.dialogue_agent import DialogueAgent

from workspace.prompts.action_plan_prompt import ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,\
                    ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE

from workspace.prompts.moderator_prompt import AGENT_MODERATOR_HEADER_TEMPLATE,\
                    AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE


def main():
    load_dotenv()

    agent_names = ["Action Plan Proposer"]

    word_limit = 500
    
    action_system_message = SystemMessage(
        content= ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE.format(
                                                agent_name = agent_names[0],
                                                agent_header = ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,
                                                word_limit = word_limit) 
                                                ) 
    
    moderator_system_message = SystemMessage(
        content= AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE)
    
    moderator_speaker = ModeratorSpeaker()
    bidding_template = moderator_speaker.generate_agent_moderator_template(
                                        ACTION_PLAN_PROPOSER_HEADER_TEMPLATE)
    
    user = User("user_name", "user_email", "user_password")
     
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
    
    simulator = DialogueSimulator(agents= [agent], 
                                    selection_function=moderator_speaker.ask_for_agent,
                                    moderator = moderator)
    
    simulator.reset()
    

    prompts = ['hello, my name is Slava, could you tell me your names', 
            'How are you doing guys?',
            'Could you tell me my name']
    n = 0 

    while n < 3:
        simulator.inject("user", prompts[n])
        name, message = simulator.step()
        print(f"({name}): {message}")
        print("\n")
        n += 1
 
 
if __name__ == "__main__":
    main()