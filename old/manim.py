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

        # Define car data
        car_data = {
            1: {"path": ["City1", "A", "C", "City2"], "waiting": [0, 5, 0, 0], "travel": [10, 20, 30]},
            2: {"path": ["City1", "B", "C", "D", "City2"], "waiting": [0, 3, 0, 2, 0], "travel": [12, 18, 15, 25]},
            3: {"path": ["City1", "A", "C", "E", "City2"], "waiting": [0, 0, 4, 0, 0], "travel": [11, 22, 19, 28]},
            4: {"path": ["City1", "B", "C", "E", "City2"], "waiting": [0, 2, 0, 0, 0], "travel": [13, 17, 21, 29]},
            5: {"path": ["City1", "A", "C", "D", "City2"], "waiting": [0, 6, 0, 0, 0], "travel": [10, 25, 18, 30]},
        }

        # Create and position cars
        vehicles = {}
        for car_id, data in car_data.items():
            start_position = graph.vertices[data["path"][0]].get_center()
            vehicle = Dot(start_position, color=YELLOW)
            self.add(vehicle)
            vehicles[car_id] = {
                "dot": vehicle,
                "path": data["path"],
                "waiting": data["waiting"],
                "travel": data["travel"],
                "current_edge_index": 0,
                "remaining_travel_time": 0,
                "waiting_time_at_node": data["waiting"][0]
            }

        # Simulation step-by-step
        max_steps = max(len(data["path"]) for data in car_data.values())
        for step in range(max_steps):
            for car_id, vehicle_data in vehicles.items():
                dot = vehicle_data["dot"]
                path = vehicle_data["path"]
                waiting_times = vehicle_data["waiting"]
                travel_times = vehicle_data["travel"]
                current_index = vehicle_data["current_edge_index"]
                
                # Update waiting time
                if vehicle_data["waiting_time_at_node"] > 0:
                    vehicle_data["waiting_time_at_node"] -= 1
                    continue
                
                # Move to the next edge if at a vertex and waiting time is 0
                if current_index < len(path) - 1:
                    current_node = path[current_index]
                    next_node = path[current_index + 1]
                    
                    if (current_node, next_node) in graph.edges:
                        edge = graph.edges[(current_node, next_node)]
                        travel_time = travel_times[current_index]
                        # Animate movement
                        self.play(MoveAlongPath(dot, edge), run_time=travel_time)
                        
                        # Update car data
                        vehicle_data["current_edge_index"] += 1
                        vehicle_data["waiting_time_at_node"] = waiting_times[current_index + 1]
            
            self.wait(1)  # Wait a bit before moving to the next step

        self.wait(2)  # Pause at the end of the animation

# 2nd try
from manim import *

class CustomAnimation(Animation):
    def __init__(self, mobject, start_point, end_point, duration=2, **kwargs):
        # Pass the duration as run_time to the Animation class
        super().__init__(mobject, run_time=duration, **kwargs)
        self.start_point = start_point
        self.end_point = end_point
    
    def interpolate_mobject(self, alpha: float) -> None:
        # Interpolate between start_point and end_point based on alpha
        new_point = self.start_point + alpha * (self.end_point - self.start_point)
        self.mobject.move_to(new_point)

class TimerExample(Scene):
    def construct(self):
        # Create two dots
        dot1 = Dot().shift(UP)
        dot2 = Dot().shift(DOWN)

        # Add dots to the scene
        self.add(dot1, dot2)

        # Define start and end points for each animation
        start_point1 = dot1.get_center()
        end_point = RIGHT * 2

        start_point2 = dot2.get_center()
        middle_point = RIGHT
        end_point2 = RIGHT * 2

        # Create custom animations with different durations
        custom_anim1 = CustomAnimation(dot1, start_point=start_point1, end_point=end_point, duration=3)

        # For dot2, build a sequence of animations:
        move_to_middle = CustomAnimation(dot2, start_point=start_point2, end_point=middle_point, duration=1)
        pause_at_middle = CustomAnimation(dot2, start_point=middle_point, end_point=middle_point, duration=1)
        move_to_end = CustomAnimation(dot2, start_point=middle_point, end_point=end_point2, duration=1)

        # Combine the sequence for dot2
        dot2_animation = AnimationGroup(move_to_middle, pause_at_middle, move_to_end)

        # Play animations simultaneously
        self.play(AnimationGroup(dot2_animation, lag_ratio=0))

# 3rd try

from manim import *

class MovingPoints(Scene):
    def construct(self):
        # Create two points
        point1 = Dot().set_color(BLUE)
        point2 = Dot().set_color(RED).shift(LEFT*2)

        # Animate the first point to move continuously
        move_point1 = point1.animate.shift(UP*2)

        # Animate the second point to stay still and then move
        move_point2 = Succession(
            point2.animate.shift(RIGHT*2),
            Wait(2),  # Point stays still for 2 seconds
            point2.animate.shift(UP*2)
        )

        # Play both animations simultaneously
        self.play(AnimationGroup(move_point1, move_point2, lag_ratio=0))
