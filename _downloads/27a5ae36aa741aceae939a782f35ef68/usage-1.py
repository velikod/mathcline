import matplotlib.pyplot as plt
from cline import Cline

# Create a cline using equation parameters
# c=1, alpha=-3-4j, d=16 represents a circle with center 3+4j and radius 5
cline = Cline(c=1.0, alpha=-3-4j, d=16)

# Create plot - the .plot() method now calculates appropriate limits automatically
fig, ax = plt.subplots(figsize=(8, 8))
cline.plot(ax=ax, color='blue', label='Circle from Parameters')
plt.legend()
plt.title('Circle Created from Equation Parameters')