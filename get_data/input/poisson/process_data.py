import glob

files = glob.glob("*.txt")
files = sorted(files)

# print(files)

# 80% train, 20% test
train = 1700
test = train + 300

def join_scenario(files):
	path = "data/"
	train_file = open(path + "train.txt", "a")
	for file in files:
		name = file.split()[0].split("_")[1]
		test_file = open(path + "test_" + name, "a")
		filename = open(file, "r")
		cont = 0
		for step in filename:
			# print(step)
			if cont <= train:
				train_file.write(step.split()[0] + '\n')
				cont += 1
			elif cont > train and cont <= test:
				test_file.write(step.split()[0] + '\n')
				cont += 1
		test_file.close()

	train_file.close()

# # split_scenario(files)
join_scenario(files)