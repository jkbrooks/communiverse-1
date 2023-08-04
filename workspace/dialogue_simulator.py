
from typing import Callable, List
from workspace.dialogue_agent import DialogueAgent


class DialogueSimulator:
    def __init__(
        self,
        agents: List[DialogueAgent],
        selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function
     
    def reset(self):
        for agent in self.agents:
            agent.reset()


    def inject_history(self, history: list):
        for agent in self.agents:
            agent.set_history(history)
    
    
    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._step += 1

    def step(self):
        # 1. choose the next speaker
        # speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker_idx = [0]
        messages = []
        speakers = []
        for idx in speaker_idx:
            speaker = self.agents[idx]

            # 2. next speaker sends message
            message = speaker.send()

            messages.append(message)
            speakers.append(speaker.name)

            # 3. everyone receives message
            for receiver in self.agents:
                receiver.receive(speaker.name, message)
            
            # 4. increment time
            self._step += 1
        
        return speakers, messages