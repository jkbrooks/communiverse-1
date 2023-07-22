# Import the SearchAgent class from SearchAgent.py
from SearchAgent import SearchAgent

def main():
    # Create an instance of SearchAgent
    search_agent = SearchAgent()

    # Use the search agent to perform a search
    search_agent.search("example query")

    # Get the results of the search
    results = search_agent.get_results()

    # Do something with the results
    print(results)

# Call the main function
if __name__ == "__main__":
    main()
