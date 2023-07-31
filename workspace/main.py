from langchain.schema import (
    HumanMessage,
    SystemMessage)
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

from dialogue_simulator import DialogueSimulator
from character_generator import CharacterGenerator
from bidding_dialogue_agent import BiddingDialogueAgent
from speaker import Speaker
from settings import TOPIC_TEMPLATE, PLAYER_DESCRIPTOR_TEMPLATE, GAME_DESCRIPTION_TEMPLATE


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
                bidding_template=bidding_template,
            )
        )

    max_iters = 10
    n = 0

    simulator = DialogueSimulator(agents=characters, 
                                    selection_function=speaker.select_next_speaker)
    simulator.reset()

    while n < max_iters:
        name, message = simulator.step()
        print(f"({name}): {message}")
        print("\n")
        n += 1


if __name__ == "__main__":
    main()
