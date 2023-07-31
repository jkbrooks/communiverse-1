import tenacity
import numpy as np
from typing import List
from bidding_dialogue_agent import DialogueAgent
from bid_output_parser import BidOutputParser

class Speaker(BidOutputParser):

    @tenacity.retry(
    stop=tenacity.stop_after_attempt(2),
    wait=tenacity.wait_none(),  # No waiting time between retries
    retry=tenacity.retry_if_exception_type(ValueError),
    before_sleep=lambda retry_state: print(
        f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
    ),
    retry_error_callback=lambda retry_state: 0,
    )
    
    def ask_for_bid(self, agent) -> str:
        """
        Ask for agent bid and parses the bid into the correct format.
        """
        bid_string = agent.bid()
        bid = int(self.bid_parser.parse(bid_string)["bid"])
        return bid
    
    def select_next_speaker(self, step: int, agents: List[DialogueAgent]) -> int:
        bids = []
        for agent in agents:
            bid = self.ask_for_bid(agent)
            bids.append(bid)

        max_value = np.max(bids)
        max_indices = np.where(bids == max_value)[0]
        idx = np.random.choice(max_indices)

        return idx
    
