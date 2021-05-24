# basically area plot

# tracks changes over time for 1 or more groups 
# tracking changes over 2 or more groups

import matplotlib.pyplot as plt

days = [1,2,3,4,5]

sleeping = [7, 8, 6, 11, 7]
eating = [2, 3, 4, 3, 2]
working = [7, 8, 7, 2, 2]
playing = [8, 5, 7, 8, 13]

plt.plot([], [], color='m', label='Sleeping', linewidth=5)
plt.plot([], [], color='c', label='Eating', linewidth=5)
plt.plot([], [], 'r', label='working', linewidth=5)

plt.stackplot(days, sleeping, eating, working, playing, colors=['m','c','r', 'k'])

plt.xlabel('x')
plt.ylabel('y')
plt.title('Stc Plot')
plt.legend()
plt.show()