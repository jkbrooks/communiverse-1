CHARACTER_DESCRIPTION_TEMPLATE = """
Please reply with a creative description of the conversation member, {character_name}, 
in {word_limit} words or less.
This character has a professional relationship with the proposer of the action plan 
and will need to participate in helping accomplish it. Please ensure this character
has some tension with the action plan and a proposed modification so we can demonstrate 
them proposing changes to the action plan to address their viewpoint.
Speak directly to {character_name}.
Do not add anything else."""


CHARACTER_HEADER_TEMPLATE = """
{game_description}
Your name is {character_name}.
You are a conversation member
Your description is as follows: {character_description}
Your goal is to improve the action plan so that it best meets everyone's needs.
"""

SYSTEM_MESSAGE_TEMPLATE = """{character_header}
Speak in the first person from the perspective of {character_name}
Do not change roles!
Do not speak from the perspective of anyone else.
Speak only from the perspective of {character_name}.
Try your best to suggest improvements to the action plan and get others to agree with your improvements.  Be open to changes from other conversation members and understand that you may not be able to get every change you want implemented in the action plan updates
Never forget to keep your response to {word_limit} words!
Do not add anything else.
"""  # noqa: E501

PLAYER_DESCRIPTOR_TEMPLATE = """
You can add detail to the description of each conversation member."""

GAME_DESCRIPTION_TEMPLATE = """
The conversation members are: {character_names}."""


TOPIC_TEMPLATE = """
"""