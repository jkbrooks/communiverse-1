from typing import Any

class Tool:
    def __init__(self, search: Any, name: str, description: str = ""):
        search = search
        self.tool = [
            Tool(
                name = name,
                func=search.run,
                description= description
            ),
        ]