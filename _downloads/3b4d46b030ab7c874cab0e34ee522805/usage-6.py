import matplotlib.pyplot as plt
from cline import Cline

# Create a figure
fig, ax = plt.subplots(figsize=(8, 8))

# Plot a circle
circle = Cline.from_circle(center=1+2j, radius=3)
circle.plot(ax=ax, color='blue', label='Circle')

# Plot a line
line = Cline.from_line(z0=-3-2j, z1=3+4j)
line.plot(ax=ax, color='red', label='Line')

# The plot automatically adjusts to show both the circle and line
plt.legend()
plt.title('Combined Circle and Line Plot')