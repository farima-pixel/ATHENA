#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

data = np.random.binomial(n = 10, p = .2, size = 98000)

print(data)

test_file = open('binomial.txt', 'w')

for i in data:
	test_file.write(str(i) + '\n')

test_file.close()

plt.plot(data)
plt.show()


# randomlist = []
# limit = 20000

# PATH = "normal/"

# for i in range(1,50):
	
# 	if i < 10:
# 		task_file = open(PATH + 'requests_0' + str(i) + '.txt','w')
# 	else:
# 		task_file = open(PATH + 'requests_' + str(i) + '.txt','w')

# 	for i in range(0,limit):
# 		n = random.randint(1,5)
# 		task_file.write(str(n) + "\n")

# 	task_file.close()

# print("Done")