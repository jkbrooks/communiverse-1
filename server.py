import streamlit as st

from langchain.schema import (
    HumanMessage,
    SystemMessage)

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time

from workspace.dialogue_simulator import DialogueSimulator
from workspace.character_generator import CharacterGenerator
from workspace.bidding_dialogue_agent import BiddingDialogueAgent
from workspace.speaker import Speaker
from workspace.settings import TOPIC_TEMPLATE, PLAYER_DESCRIPTOR_TEMPLATE, GAME_DESCRIPTION_TEMPLATE


def main():
    load_dotenv()

    character_names = ["Willie Dustice", "Kevin Nogilny", "Ray McScriff"]
    topic = TOPIC_TEMPLATE
    word_limit = 50

    formatted_character_names = ', '.join(character_names)
    game_description = GAME_DESCRIPTION_TEMPLATE.format(
                        character_names=formatted_character_names)
    
    player_descriptor_system_message = SystemMessage(
        content=PLAYER_DESCRIPTOR_TEMPLATE
    )

    character_generator = CharacterGenerator(character_names, topic, word_limit, 
                                             player_descriptor_system_message, 
                                             game_description)
    
    character_generator.generate_character_description()
    character_generator.generate_character_header()
    character_generator.generate_character_system_message()
    
    speaker = Speaker()
    character_bidding_templates = speaker\
                        .generate_character_bidding_template(character_generator.character_headers)

    characters = []
    for character_name, character_system_message, bidding_template in zip(
        character_names, character_generator.character_system_messages, 
        character_bidding_templates
    ):
        characters.append(
            BiddingDialogueAgent(
                name=character_name,
                system_message=character_system_message,
                model=ChatOpenAI(temperature=0.2),
                bidding_template=bidding_template
            )
        )
    
    simulator = DialogueSimulator(agents=characters,
                                    selection_function=speaker.select_next_speaker)
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