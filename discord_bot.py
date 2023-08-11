import os
import random
import discord
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



load_dotenv()
os.environ['DISCORD_TOKEN'] = 'MTEzOTIyMjYzODUzNTkwMTMwNg.GUKLcz.nUq9mFzcmtrCyvEPlahQ0___V5WstR-KX1N7vw'
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True
#_________________________LOAD AGENT PART ___________________

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
        
    # if message.content == '99!':
        # response = random.choice(brooklyn_99_quotes)
        # await message.channel.send(response)

client.run(TOKEN)
