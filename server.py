import streamlit as st

from langchain.schema import (
    SystemMessage)

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time

from workspace.dialogue_simulator import DialogueSimulator
from workspace.agent_generator import AgentGenerator
from workspace.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.speaker import Speaker
from workspace.dialogue_agent import DialogueAgent
from workspace.settings import TOPIC_TEMPLATE, AGENT_DESCRIPTOR_TEMPLATE
from workspace.prompts.action_plan_prompt import ACTION_PLAN_PROPOSER_HEADER_TEMPLATE, ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE


def main():
    load_dotenv()

    agent_names = ["Action Plan Proposer"]

    word_limit = 500
    
    system_message = SystemMessage(
        content= ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE.format(
                                                agent_name = agent_names[0],
                                                agent_header = ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,
                                                word_limit = word_limit) 
                                                ) 
    
    # agent_description -> agent_header -> agent_system
    
    agent = DialogueAgent(name = agent_names[0], 
                            system_message = system_message,
                            model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k")
                            )

    simulator = DialogueSimulator(agents= [agent], 
                                    selection_function=None)
    simulator.reset()
    
    st.title("Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'agent_memory' not in st.session_state:
        st.session_state['agent_memory'] = ["Here is the conversation so far."]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your message here"):
        simulator.inject_history(st.session_state['agent_memory'])

        st.session_state['agent_memory'].append(f"user: {prompt}")
        
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
            
            st.session_state['agent_memory'].append(f"{name}: {full_response}")


    if st.button('Run conversation'):
        simulator.inject_history(st.session_state['agent_memory'])

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
            
            st.session_state['agent_memory'].append(f"{name}: {full_response}")
 
if __name__ == "__main__":
    main()