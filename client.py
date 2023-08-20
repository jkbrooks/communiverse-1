import streamlit as st

import time


if 'user_name' not in st.session_state.keys():
    
    st.session_state.user_name = None
    st.session_state.conformation  = False
    st.session_state.name_written = False
    st.session_state.replica = ''
    st.session_state.break_point = False

if "messages" not in st.session_state:
        st.session_state.messages = []

if 'agent_memory' not in st.session_state:
    st.session_state['agent_memory'] = ["Here is the conversation so far."]

if st.session_state.name_written  == False:
    st.session_state.user_name = st.text_input('Enter your user name.')

    st.session_state.conformation = st.button('Enter the chat.')
    if st.session_state.conformation == True:
        st.session_state.name_written  = True

if st.session_state.conformation:
    
    st.title('Chat')
    
    chat_container = st.empty()
    prompt = st.chat_input('Enter your message here.')
    while True:
        if prompt is not None:
            with open('chat.txt','r+') as file:
                old_data = file.readlines()
                if '\n' not in prompt:    
                    value_to_write = f'{st.session_state.user_name}: {prompt} \n'
                    if value_to_write not in old_data:
                        file.write(value_to_write)
                elif '\n' in prompt:
                    prompt_list = prompt.split('\n')
                    transformed_value = ' '.join(prompt_list)
                    value_to_write = f'{st.session_state.user_name}: {transformed_value} \n'
                    if value_to_write not in old_data:
                        file.write(value_to_write)
            
        with open('chat.txt', 'r') as file:
            data = file.readlines()
        
        basic_str = ''
        for line in data:
            line_splitted = line.split(':')
            name = line_splitted[0]
            value = ' '.join(line_splitted[1:])
            if st.session_state.user_name != name:
                value_to_write = f'<b>{name}</b>: {value}</br>'
            elif st.session_state.user_name == name:
                value_to_write = f'<b>{name}</b>:{value}</br>'
            
            basic_str+=value_to_write

        chat_container.markdown(f'***CHAT***: {basic_str}', True)
            

            
                    
