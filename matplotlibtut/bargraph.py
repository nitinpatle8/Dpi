from matplotlib import pyplot as plt
# compare things between groups 


plt.bar([1,3,5,7,9], [5,2,7,8,2], label="Example One")

plt.bar([2,4,6,7,9],[8,6,2,5,6], label="example two", color = 'g')

plt.legend()

plt.xlabel('bar number')
plt.ylabel('bar height')

plt.title('bar graph')

plt.show()