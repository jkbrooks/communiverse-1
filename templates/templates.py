CHAT_DESCRIPTION_TEMPLATE  = """
The conversation members are: {agent_names}.
"""


WORK_AGENT_TEMPLATE = """
______________________________
You are a working agent that helps people to do their tasks.
You will be assigned with a task, and during the Execution Phase you will have to do it.
______________________________
"""

ACTION_GRAPH_MANAGER_TEMPLATE = """
You are helpful assistant that creates action plan for tasks provided by people.
You have to create a list of tasks and corresponding subtasks for task which was provided by the user, in following format:
_______________
List of tasks: list_of_tasks = [*generated list of tasks*]
Dictionary of subtasks: subtasks = {*main task*:*list of corresponding subtasks*}
_______________
"""

WORK_AGENT_SYSTEM_MESSAGE_TEMPLATE = """{agent_header}
Speak in the first person from the perspective of {agent_name}. Do not change roles!
Do not speak from the perspective of anyone else. Speak only from the perspective of {agent_name}.
Start to engage in conversation if you got the invitation. 
Do not engage in parts of the conversation to which you are not entitled.
Do not add anything else.
"""

#DRFAT VERSION MIGHT BE CHANGED