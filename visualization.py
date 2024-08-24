from manim import *

class TrafficGraph(Scene):
    def construct(self):
        # Define nodes and edges
        nodes = ["City1", "A", "B", "C", "D", "E", "City2"]
        edges = [
            ("City1", "A"),
            ("City1", "B"),
            ("A", "C"),
            ("B", "C"),
            ("C", "D"),
            ("C", "E"),
            ("C", "City2"),
            ("D", "City2"),
            ("E", "City2"),
        ]
        
        # Define vertex configurations with different colors for start/end and middle nodes
        vertex_config = {
            "City1": {"radius": 0.7, "color": ORANGE},
            "City2": {"radius": 0.7, "color": ORANGE},
            "A": {"radius": 0.3, "color": LIGHT_PINK},
            "B": {"radius": 0.3, "color": LIGHT_PINK},
            "C": {"radius": 0.3, "color": LIGHT_PINK},
            "D": {"radius": 0.3, "color": LIGHT_PINK},
            "E": {"radius": 0.3, "color": LIGHT_PINK},
        }
        
        # Define custom positions for each node
        layout = {
            "City1": [-5, 0, 0],  # Leftmost
            "A": [-2.5, 2, 0],
            "B": [-2.5, -2, 0],
            "C": [0, 0, 0],
            "D": [2.5, 2, 0],
            "E": [2.5, -2, 0],
            "City2": [5, 0, 0],  # Rightmost
        }
        
        # Create the graph with labels and custom vertex configurations
        graph = Graph(
            vertices=nodes,
            edges=edges,
            layout=layout,  # Use the custom layout
            labels=True,  # Show labels on the nodes
            vertex_config=vertex_config,  # Apply custom vertex configurations
            edge_config={"stroke_width": 2}  # Customize the appearance of edges
        )

        # Add the graph to the scene
        self.play(Create(graph))
        self.wait()

        # Example: Move a "vehicle" (dot) along an edge
        vehicle = Dot(graph.vertices["City1"].get_center(), color=YELLOW)
        self.add(vehicle)
        self.play(MoveAlongPath(vehicle, graph.edges[("City1", "A")]))
        self.wait()
