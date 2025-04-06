import matplotlib.pyplot as plt
from cline import Cline

# Create a circle with center at 1+2j and radius 2
circle = Cline.from_circle(center=1+2j, radius=2)

# Print circle information (only shown in code, not in output)
print(circle)

# Create plot
fig, ax = plt.subplots(figsize=(8, 8))
circle.plot(ax=ax, color='blue', label='Circle')

# Set limits and add legend
ax.set_xlim(-3, 5)
ax.set_ylim(-1, 5)
ax.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.title('Circle with Center at 1+2j and Radius 2')