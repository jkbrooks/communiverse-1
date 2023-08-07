import tenacity
from workspace.moderator_output_parser import ModeratorOutputParser

class ModeratorSpeaker(ModeratorOutputParser):

    @tenacity.retry(
    stop=tenacity.stop_after_attempt(2),
    wait=tenacity.wait_none(),  # No waiting time between retries
    retry=tenacity.retry_if_exception_type(ValueError),
    before_sleep=lambda retry_state: print(
        f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
    ),
    retry_error_callback=lambda retry_state: 0,
    )
    
    def ask_for_agent(self, agent) -> str:

        bid_string = agent.bid()
        bid = int(self.parse(bid_string)["agent"])
        return bid

    
