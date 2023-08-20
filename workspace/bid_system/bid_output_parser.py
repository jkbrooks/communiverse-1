from langchain.output_parsers import RegexParser


class BidOutputParser(RegexParser):
    def __init__(self, regex_pattern=r"<(\d+)>"):
        super().__init__(regex=regex_pattern, output_keys=["bid"], 
                         default_output_key="bid")
    
    def get_format_instructions(self) -> str:
        return """Your response should be an integer delimited by angled brackets, 
        like this: <int>."""
    
    def generate_agent_bidding_template(self, agent_header:list)->list:
        bidding_templates = []

        for header in agent_header:
            
            bidding_templates.append(
                f"""{header}
                ```
                {{message_history}}
                ```
                On a scale of 1 to 10, where 1 signifies when it is not your part of the conversation and 10 indicates when it is definitely your part of the conversation, rate the 
                optimal time for you to start engaging based on the provided conversation and according to your role.
                ```
                {{recent_message}}
                ```                
                {self.get_format_instructions()}
                Do nothing else.
            """) 
        return bidding_templates[0]
    
    def generate_stage_template(self, agent_header):
        stage_template = f"""{agent_header} 
        ```
        {{message_history}}
        ```
        You should return your current step of the conversation, according to the conversation and your role.
        ```
        {self.get_format_instructions()}
        Do nothing else. 
        """
        return stage_template