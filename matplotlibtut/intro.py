from matplotlib import pyplot as plt
# x on left side 
# y on right side 
# plt.plot simply draws continues line
# between points
from matplotlib import style

# style.use("ggplot")

x = [5, 8, 10]
y = [12, 16, 6]

# plt.plot([1,2,3], [4,5,1])

# add title/ labes plotting variables

# plt.title("info")
# plt.ylabel('y-axis')
# plt.xlabel('x-axis');

# plt.show()

# plt.plot(x, y)

x = [6, 9, 11]
y = [6, 15, 7]

# plt.show()
# x, y, colour of  line, label to line, linewidth
plt.plot(x, y, 'g', label="line one", linewidth=5)

# add legend to graph

plt.legend()

plt.grid(True, color='k')

plt.show()

print(plt);