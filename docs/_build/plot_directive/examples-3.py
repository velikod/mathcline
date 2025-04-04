import matplotlib.pyplot as plt

from cline import Cline

# Create multiple clines
circle = Cline.from_circle(center=1 + 1j, radius=2)
line1 = Cline.from_line(z0=-2 - 2j, z1=2 + 2j)
line2 = Cline.from_line(z0=-2 + 2j, z1=2 - 2j)

# Create plot
fig, ax = plt.subplots(figsize=(8, 8))

# Plot the clines
circle.plot(ax=ax, color="blue", label="Circle")
line1.plot(ax=ax, color="red", label="Line 1")
line2.plot(ax=ax, color="green", label="Line 2")

# Set limits and add legend
ax.set_xlim(-3, 5)
ax.set_ylim(-3, 5)
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_aspect("equal")
plt.legend()
plt.title("Multiple Clines")
