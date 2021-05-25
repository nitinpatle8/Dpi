import numpy as np
from numpy.core.function_base import linspace

myarr = np.array([3, 6, 32, 7])

print(myarr)


rng = np.arange(15)

# equally spaced 10 elements 
# means 9 elements
lspace = np.linspace(0, 50, 10)
# equally spaced 11 elements
# means equal 10 spaces 
lspace2 = np.linspace(0, 50, 11)
print(lspace)

# array of 4,6 but random values
# can be float int
emp = np.empty((4,6))

emp_like = np.empty_like(lspace)

print(emp_like)


ide = np.identity(45) # 45*45 identity matrix

arr = np.arange(99)

# arr.reshape 
# arr.reshape(3, 31)

# becomes 1 d array
arr.ravel()

# numpy axis 

# [1,3,3,4,5,6] -> 1 axis
# [[], []] -> 2 axis 

# coordinate 
x = [[1,2,3], [4,5,6], [7,1,0]]
ar = np.array(x)
print(ar)

print(ar.sum(axis=0))

# whole 2 d array 
for item in ar.flat:
    print(item)

# ar.size
print(ar.size)

print(ar.nbytes)

one = np.array([1,4,2,4,5])
print(one.argmax())

# gives index of sorted array
one.argsort()

ar.argmin()


ar.argmax()

ar.argmax(axis=0)

ar.argmax(axis=1)