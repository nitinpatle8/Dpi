# mainly used for correlation between two variables

import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8]
y = [5,2,4,2,1,4,2, 6]

plt.scatter(x,y,label='skitscat', color='k')

plt.xlabel('x')
plt.ylabel('y')
plt.title('scatter')
plt.legend()
plt.show()