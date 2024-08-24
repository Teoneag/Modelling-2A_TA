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
        dot1 = Dot()
        dot2 = Dot()

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
        self.play(AnimationGroup(custom_anim1, dot2_animation, lag_ratio=0))
