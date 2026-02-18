import numpy as np
import matplotlib.pyplot as plt

# Time steps
t = np.linspace(0, 10, 200)

# Simulated energy decay (damped system)
energy = np.exp(-0.4*t) + 0.05*np.random.randn(len(t))

# Plot
plt.figure()
plt.plot(t, energy)
plt.title("QVDE Demo: Energy Convergence Over Time")
plt.xlabel("Time")
plt.ylabel("Energy")
plt.savefig("output.png")
print("Graph saved as output.png")

