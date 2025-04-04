import matplotlib.pyplot as plt

from cline import Cline

# Create a circle with center at 1+2j and radius 3
circle = Cline.from_circle(center=1 + 2j, radius=3)

# Create plot with automatic limits based on circle center and radius
fig, ax = plt.subplots(figsize=(8, 8))
circle.plot(ax=ax, color="green", label="Circle")
plt.legend()
plt.title("Circle with Center at 1+2j and Radius 3")
