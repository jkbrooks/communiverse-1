from langchain.output_parsers import RegexParser


class ModeratorOutputParser(RegexParser):
    def __init__(self, regex_pattern=r"<(\d+)>"):
        super().__init__(regex=regex_pattern, output_keys=["agent"], 
                         default_output_key="agent")
    
    def get_format_instructions(self) -> str:
        return """Your response should be an integer delimited by angled brackets, 
        like this: <int>."""
    
    def generate_agent_moderator_template(self, agent_header:list)->list:
        moderator_templates = []

        for header in agent_header:
            
            moderator_templates.append(
                f"""{header}
                ```
                {{message_history}}
                ```
                ```
                {{recent_message}}
                ```
                Pick a number between 0 and 2.
                {self.get_format_instructions()}
                Do nothing else.
            """)
        return moderator_templates
