CHARACTER_DESCRIPTION_TEMPLATE = """
Please reply with a creative description of the conversation member, {character_name}, 
in {word_limit} words or less.
Speak directly to {character_name}.
Do not add anything else."""


CHARACTER_HEADER_TEMPLATE = """
{game_description}
Your name is {character_name}.
You are a conversation member
Your description is as follows: {character_description}
"""

SYSTEM_MESSAGE_TEMPLATE = """{character_header}
Speak in the first person from the perspective of {character_name}
Do not change roles!
Do not speak from the perspective of anyone else.
Speak only from the perspective of {character_name}.
You check the conversation history before speaking and your response is based on the conversation history.
Never forget to keep your response to {word_limit} words!
"""  # noqa: E501

PLAYER_DESCRIPTOR_TEMPLATE = """
You can add detail to the description of each conversation member."""

GAME_DESCRIPTION_TEMPLATE = """
The conversation members are: {character_names}."""


TOPIC_TEMPLATE = """
"""