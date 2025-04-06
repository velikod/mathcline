import matplotlib.pyplot as plt
from cline import Cline

# Create a cline directly by specifying c, alpha, and d parameters
# c=1, d=1, alpha=2+1j
cline = Cline(c=1, alpha=2+1j, d=1)

# Print cline information
print(cline)

# Create plot
fig, ax = plt.subplots(figsize=(8, 8))
cline.plot(ax=ax, color='purple', label='Cline from Parameters')

ax.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.title('Cline with c=1, d=1, alpha=2+1j')