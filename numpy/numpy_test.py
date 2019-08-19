import numpy as np
eye_mat = np.eye(4)
print(eye_mat)

array1 = np.array([1, 2, 3])
print(array1)

array2 = np.array([[1, 2, 3], [4, 5, 6]], ndmin=2)
print(array2)
print(array2.shape)

array3 = np.zeros((3, 2), order="C")
print(array3)

array4 = np.arange(1, 11, 2, dtype=float)
print(array4)

array5 = array4[2:5:2]
print(array5)

a = np.array([[1, 2, 3], [3, 4, 5], [4, 5, 6]])
print(a[..., 1])  # 第2列元素
print(a[1, ...])  # 第2行元素
print(a[..., 1:])  # 第2列及剩下的所有元素
