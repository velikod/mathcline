from manim import (
    BLUE,
    BLUE_E,
    RED,
    RED_E,
    Circle,
    Create,
    Scene,
    Square,
    Text,
    Transform,
    Write,
)


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        square = Square()
        square.set_fill(RED, opacity=0.5)
        square.set_stroke(RED_E, width=4)

        self.play(Create(square))
        self.wait()
        self.play(Transform(square, circle))
        self.wait()

        text = Text("Manim is working!")
        self.play(Write(text))
        self.wait()


if __name__ == "__main__":
    print("Manim test script loaded successfully!")
    print("To render the animation, run:")
    print("manim -pql test_manim.py SquareToCircle")
