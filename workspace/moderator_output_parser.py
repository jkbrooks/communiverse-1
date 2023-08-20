from langchain.output_parsers import RegexParser


class ModeratorOutputParser(RegexParser):
    def __init__(self, regex_pattern=r"<(\d+)>"):
        super().__init__(regex=regex_pattern, output_keys=["agent"], 
                         default_output_key="agent")
    
    def get_format_instructions(self) -> str:
        return """Your response should be an integer or list of ints delimited by angled brackets, 
        like this: <int>."""
    
    def generate_agent_moderator_template(self, agent_header:str)->str:
            
        moderator_template = f"""{agent_header}
            ```
            {{message_history}}
            ```
            ```
            {{recent_message}}
            ```
            You need to precisely analize the message_history and the recent message and pick a number between 0 and 2 that correspond to the name of the agent who should communicate next. It can be a sequence of indexes.
            {self.get_format_instructions()}
            Do nothing else.
        """
        return moderator_template
