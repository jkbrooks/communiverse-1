from langchain.output_parsers import RegexParser


class BidOutputParser(RegexParser):
    def __init__(self, regex_pattern=r"<(\d+)>"):
        super().__init__(regex=regex_pattern, output_keys=["bid"], 
                         default_output_key="bid")
    
    def get_format_instructions(self) -> str:
        return """Your response should be an integer delimited by angled brackets, 
        like this: <int>."""
    
    def generate_character_bidding_template(self, character_header:list)->list:
        bidding_templates = []

        for header in character_header:
            
            bidding_templates.append(
                f"""{header}
                ```
                {{message_history}}
                ```
                ```
                {{recent_message}}
                ```
                Pick a random number between 1 and 10
                {self.get_format_instructions()}
                Do nothing else.
            """)
        return bidding_templates
