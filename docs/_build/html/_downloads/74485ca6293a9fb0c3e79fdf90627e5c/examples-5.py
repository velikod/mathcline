import matplotlib.pyplot as plt

from cline import Cline

# Create three collinear points (these all lie on the line y = 2x)
z0 = 1 + 2j  # (1,2)
z1 = 2 + 4j  # (2,4)
z2 = 3 + 6j  # (3,6)

# Create a cline passing through these three points
# Because the points are collinear, this will create a line
cline = Cline.from_three_points(z0, z1, z2)

# Print information about the cline (not shown in output)
print(cline)
print(f"Is circle: {cline.is_circle}")
print(f"Is line: {cline.is_line}")

# Create plot with automatic limits
fig, ax = plt.subplots(figsize=(8, 8))
cline.plot(ax=ax, color="orange", label="Line through 3 collinear points", show_points=True)

# Add a grid to visualize the collinearity
ax.grid(True, linestyle="-", alpha=0.3)

# Add text annotation
ax.text(
    0.5,
    0.05,
    "The points (1,2), (2,4), and (3,6) are collinear\nand lie on the line y = 2x",
    transform=ax.transAxes,
    fontsize=12,
    horizontalalignment="center",
    verticalalignment="bottom",
)

plt.legend()
plt.title("Line Through Three Collinear Points")
