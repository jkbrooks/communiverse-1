from langchain.schema import (
    HumanMessage,
    SystemMessage)
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

from workspace.dialogue_simulator import DialogueSimulator
from workspace.agent_generator import AgentGenerator
from workspace.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.speaker import Speaker
from workspace.settings import TOPIC_TEMPLATE, AGENT_DESCRIPTOR_TEMPLATE, CHAT_DESCRIPTION_TEMPLATE


def main():
    load_dotenv()

    agent_names = ["Willie Dustice", "Kevin Nogilny", "Ray McScriff"]
    topic = TOPIC_TEMPLATE
    word_limit = 50

    formatted_agent_names = ', '.join(agent_names)
    chat_description = CHAT_DESCRIPTION_TEMPLATE.format(
                        agent_names=formatted_agent_names)
    
    agent_descriptor_system_message = SystemMessage(
        content=AGENT_DESCRIPTOR_TEMPLATE
    )

    agent_generator = AgentGenerator(agent_names, topic, word_limit, 
                                             agent_descriptor_system_message, 
                                             chat_description)
    
    agent_generator.generate_agent_description()
    agent_generator.generate_agent_header()
    agent_generator.generate_agent_system_message()
    
    speaker = Speaker()
    agent_bidding_templates = speaker\
                        .generate_agent_bidding_template(agent_generator.agent_headers)

    agents = []
    for agent_name, agent_system_message, bidding_template in zip(
        agent_names, agent_generator.agent_system_messages, 
        agent_bidding_templates
    ):
        agents.append(
            BiddingDialogueAgent(
                name=agent_name,
                system_message=agent_system_message,
                model=ChatOpenAI(temperature=0.2),
                bidding_template=bidding_template,
            )
        )
    
    max_iters = 3
    n = 0

    simulator = DialogueSimulator(agents=agents, 
                                    selection_function=speaker.select_next_speaker)
    simulator.reset()

    prompts = ['hello, my name is Slava, could you tell me your names', 
               'How are you doing guys?',
               'Could you tell me my name']

    while n < max_iters:
        simulator.inject("user", prompts[n])
        name, message = simulator.step()
        print(f"({name}): {message}")
        print("\n")
        n += 1


if __name__ == "__main__":
    main()
