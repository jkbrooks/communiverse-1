import os
import random
import discord
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time
from workspace.user import User
from AgentHandler import load_agents
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






os.environ['DISCORD_TOKEN'] = 'MTEzOTIyMjYzODUzNTkwMTMwNg.G9H4hR.aMI8_dovZgYjxfp0sveZM11gR41OvoytlChUzY'
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True
#_________________________LOAD AGENT PART ___________________

simulator = load_agents()
# simulator.reset()


agent_memory = ['Here is the conversation so far.']
ag_messages = []

#___________________________END _____________________________


client = discord.Client(intents = intents)

test_variable = 'test'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global agent_memory
    if message.author == client.user:
        return

    if message.content == 'agent_reset_memory':
        
        simulator.reset()
        agent_memory = ['Here is the conversation so far.']
        await message.channel.send('Memory of the agent was reseted.')
    if 'ask_agent' in message.content:
       
        print(agent_memory)
        message_splitted = message.content.split(' ')
        user_message = ' '.join(message_splitted[1:])
        simulator.inject_history(agent_memory)
        ag_messages.append({'role':'user', 'content': user_message})
        simulator.inject(f'{message.author}', user_message)

        names, assistant_responses = simulator.step()
        for name, assistant_response in zip(names, assistant_responses):
            full_responce = ''
            for chunk in assistant_response.split():
                full_responce += chunk + ' '
        print(len(full_responce))
        await message.channel.send(full_responce)
    

client.run(TOKEN)
