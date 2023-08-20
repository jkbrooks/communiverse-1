
from typing import Callable, List
from .dialogue_agent import DialogueAgent
from .bid_system.bidding_dialogue_agent import BiddingDialogueAgent


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
        # self._step += 1


    def step(self):
        # 1. choose the next speaker
        # speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker_idx = self.select_next_speaker(self._step, self.agents)
        print(speaker_idx)
        print(f' OUTPUT SPEAKER IND: {speaker_idx}')
        # speaker_idx = [0]
        messages = []
        speakers = []

        speaker = self.agents[speaker_idx]
        message = speaker.send()
        messages.append(message)
        speakers.append(speaker.name)

        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        self._step += 1
        print(f'SELF STEP: {self._step} ')
        return speakers, messages