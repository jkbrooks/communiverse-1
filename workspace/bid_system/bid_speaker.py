import tenacity
import numpy as np
from typing import List
from workspace.bid_system.bidding_dialogue_agent import DialogueAgent
from workspace.bid_system.bid_output_parser import BidOutputParser

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
        bid = int(self.parse(bid_string)["bid"])
        return bid
    
    def select_next_speaker(self, step: int, agents: List[DialogueAgent]) -> list:
        bids = []
        for agent in agents:
            bid = self.ask_for_bid(agent)
            bids.append(bid)
        
        max_value = np.max(bids)

        max_indices = [index for index, num in enumerate(bids) if num == max_value]

        return max_indices
    
