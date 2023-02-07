import glob

files = glob.glob("*.txt")
files = sorted(files)

# 80% train, 20% test
time = 1003110 - 400

train = time
test = train + 400 + 500

def split_scenario(files):
	path = "split_scenario/"
	for file in files:
		name = file.split()[0].split("_")[1].split(".")[0]
		train_file = open(path + "train_" + name + ".txt", "a")
		test_file = open(path + "test_" + name + ".txt", "a")
		filename = open(file, "r")
		for step in filename:
			if int(step.split()[0]) <= train:
				train_file.write(step.split()[0] + '\t' + step.split()[1] + '\n')
			elif int(step.split()[0]) > train and int(step.split()[0]) <= test:
				test_file.write(step.split()[0] + '\t' + step.split()[1] + '\n')
		train_file.close()
		test_file.close()

def join_scenario(files):
	path = "joint_scenario/"
	train_file = open(path + "train.txt", "a")
	
	for file in files:
		name = file.split()[0].split("_")[1].split(".")[0]
		test_file = open(path + "test_" + name + ".txt", "a")
		filename = open(file, "r")
		for step in filename:
			if int(step.split()[0]) <= train:
				train_file.write(step.split()[0] + '\t' + step.split()[1] + '\n')
			elif int(step.split()[0]) > train and int(step.split()[0]) <= test:
				test_file.write(step.split()[0] + '\t' + step.split()[1] + '\n')
		test_file.close()

	train_file.close()

# split_scenario(files)
join_scenario(files)