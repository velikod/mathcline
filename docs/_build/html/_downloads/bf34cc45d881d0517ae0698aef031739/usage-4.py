import matplotlib.pyplot as plt

from cline import Cline

# Create three points in the complex plane
z0 = 0
z1 = 1
z2 = 1j

# Create a cline passing through these three points
cline = Cline.from_three_points(z0, z1, z2)

# Create plot with automatic limits
fig, ax = plt.subplots(figsize=(8, 8))
cline.plot(ax=ax, color="purple", label="Circle through 3 points", show_points=True)
plt.legend()
plt.title("Circle Through Three Points")
