import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
action_graph = nx.DiGraph()

# Define nodes (tasks)
tasks = [
    "Define Purpose and Requirements",
    "Research and Design",
    "Secure Funding and Resources",
    "Legal and Regulatory Compliance",
    "Prototype Development",
    "Full-Scale Construction",
    "Integration of Systems",
    "Testing and Quality Assurance",
    "Launch and Mission Operations",
    "Continuous Improvement",
]

# Define subtasks for each task
subtasks = {
    "Define Purpose and Requirements": ["Define purpose and goals", "Identify key requirements"],
    "Research and Design": ["Research existing designs", "Collaborate with engineers", "Consider materials"],
    "Secure Funding and Resources": ["Estimate project budget", "Seek funding", "Assemble a skilled team"],
    "Legal and Regulatory Compliance": ["Understand and comply with regulations", "Obtain permits"],
    "Prototype Development": ["Develop scaled-down prototype", "Test key systems", "Address testing issues"],
    "Full-Scale Construction": ["Begin full-scale construction", "Collaborate with manufacturers"],
    "Integration of Systems": ["Integrate propulsion, navigation, communication", "Ensure subsystem cooperation"],
    "Testing and Quality Assurance": ["Conduct comprehensive testing", "Implement quality assurance", "Rectify defects"],
    "Launch and Mission Operations": ["Plan and execute starship launch", "Monitor and control starship"],
    "Continuous Improvement": ["Gather data from the mission", "Use data for improvement", "Iterate on the design"],
}

# Add nodes and edges to the graph
for task in tasks:
    action_graph.add_node(task)
    if task in subtasks:
        for subtask in subtasks[task]:
            action_graph.add_node(subtask)
            action_graph.add_edge(task, subtask)

print(action_graph)
# Visualize the graph
pos = nx.spring_layout(action_graph)
nx.draw(action_graph, pos, with_labels=True, font_weight='bold', node_size=200, node_color='skyblue', font_size=6)
plt.show()
