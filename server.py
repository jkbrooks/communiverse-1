import streamlit as st

from langchain.schema import (
    SystemMessage)

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time

from workspace.user import User

from workspace.dialogue_simulator import DialogueSimulator

from workspace.moderator_speaker import ModeratorSpeaker
from workspace.bid_system.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.dialogue_agent import DialogueAgent

from workspace.prompts.action_plan_prompt import ACTION_PLAN_PROPOSER_HEADER_TEMPLATE,\
                    ACTION_PLAN_PROPOSER_SYSTEM_MESSAGE_TEMPLATE

from workspace.prompts.moderator_prompt import AGENT_MODERATOR_HEADER_TEMPLATE,\
                    AGENT_MODERATOR_SYSTEM_MESSAGE_TEMPLATE
from workspace.prompts.commander_prompt import COMMANDER_SYSTEM_MESSAGE_TEMPLATE,\
                    AGENT_COMMANDER_TEMPLATE
from workspace.prompts.discussant_prompt import DISCUSSANT_SYSTEM_MESSAGE_TEMPLATE,\
                    AGENT_DISCUSSANT_TEMPLATE


def main():
    load_dotenv()

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
    
    agent_commander = DialogueAgent(name = agent_names[1], 
                    system_message = commander_system_message,
                    model = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k"),
                    user = user,
                    version = 1.0,
                    id = 1
                    )
    
    agent_disscusant = DialogueAgent(name = agent_names[2], 
                system_message = disscusant_system_message,
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
    
    agents = [agent, agent_commander, agent_disscusant]
    simulator = DialogueSimulator(agents= agents, 
                                    selection_function=moderator_speaker.ask_for_agent,
                                    moderator = moderator)
    
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