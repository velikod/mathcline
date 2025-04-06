import matplotlib.pyplot as plt
from cline import Cline

# Create a line passing through points 0 and 1+1j
line = Cline.from_line(z0=0, z1=1+1j)

# Create plot - the limits are now automatically calculated
# based on the points used to create the line
fig, ax = plt.subplots(figsize=(8, 8))
line.plot(ax=ax, color='red', label='Line', show_points=True)
plt.legend()
plt.title('Line Through Points 0 and 1+1j')