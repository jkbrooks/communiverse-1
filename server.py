import streamlit as st

from langchain.schema import (
    HumanMessage,
    SystemMessage)
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time


from workspace.dialogue_simulator import DialogueSimulator
from workspace.agent_generator import AgentGenerator
from workspace.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.speaker import Speaker
from workspace.settings import TOPIC_TEMPLATE, AGENT_DESCRIPTOR_TEMPLATE, CHAT_DESCRIPTION_TEMPLATE, ACTION_PLAN_PROPOSER_AGENT_DESCRIPTION_TEMPLATE


def main():
    load_dotenv()

    agent_names = ["Action Plan Proposer", "Commander Bob", "Commander Alice", "Discussant Emmanuel", "Discussant Peterson"]
    topic = TOPIC_TEMPLATE
    word_limit = 1000

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
                bidding_template=bidding_template
            )
        )

    action_plan_proposer = BiddingDialogueAgent(
        name = "Action Plan Proposer Frank",
        system_message = action_plan_proposer_system_message,
        model=ChatOpenAI(temperature=0.2),
        bidding_template=bidding_template)

    agents.append(action_plan_proposer)

    simulator = DialogueSimulator(agents=agents,
                                    selection_function=speaker.select_next_speaker)
    simulator.reset()
    
    st.title("Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your message here"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

            simulator.inject("user", prompt)

        names, assistant_responses = simulator.step()

        for name, assistant_response in zip(names, assistant_responses):
            with st.chat_message(name):
                message_placeholder = st.empty()
                full_response = ""
                
                
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": name,
                                            "content": full_response})
        

if __name__ == "__main__":
    main()