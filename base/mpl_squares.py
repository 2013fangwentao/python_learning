import matplotlib.pyplot as plt
from random_walk import RandomWalk

rw = RandomWalk()
rw.fill_walk()

plt.figure(dpi=128, figsize=(10, 6))
plt.scatter(rw.x_values, rw.y_values, c='red', edgecolors='none', s=40)
plt.title("squares numbers", fontsize=24)
plt.xlabel('Value', fontsize=14)
plt.ylabel('Squares of Value', fontsize=14)
plt.tick_params(axis='both', labelsize=14)
plt.savefig('mypic.png', bbox_inches='tight')
plt.show()
