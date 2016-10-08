#from sys import argv
import sys

cost_mat = []
state_mat = []

def prepare_mat(filename):
	count = 5 
	i = 1
	fp = open(filename, "r")
	for line in fp.readlines():
		if (count > 0):
			cost_mat.append([])
			for cost in line.split():
				cost_mat[-1].append({"cost":int(cost), "status":'*'})
			count = count - 1
			continue

#		print(line)
#		print('aaaaaaaaaaaaaaaaa')
		j = 1
		for letter in line:
			print(letter)
			cost_mat[i][j]["status"] = letter
			j = j + 1 
		i = i + 1
		if (i > 5):
			break;
	print "End of init_mat"

def init_mat(filename):
	count = 5
	fp = open(filename, "r")
	for line in fp.readlines():
		if (count > 0):
			cost_mat.append([])
			for cost in line.split():
				cost_mat[-1].append(int(cost))
			count = count - 1
			continue

		print(line)
#		print('aaaaaaaaaaaaaaaaa')
		state_mat.append([])
		for letter in line:
#			print(letter)
			state_mat[-1].append(letter)
	print "End of init_mat"

def display_mat(mat):
	for i in range(len(mat)):
		string = ' '
#		print '\n'
		for j in range(len(mat)):
			string = string + str(mat[i][j])
			string = string + ' '
		print(string)
	print '\n'

def read_file(filename):
	fp = open(filename, "r")
	for line in fp.readlines():
		print(line)
	fp.close

def main(argv):
	file = ' '
	try:
		file = argv[0]
	except:
		print 'hello.py -i <inputfile>'
		sys.exit(2)
	print "file name is:", file
#	read_file(file)
	init_mat(file)
	
	display_mat(cost_mat)
	display_mat(state_mat)



if __name__ == "__main__":
	main(sys.argv[1:])



#file = open("output.txt", "w") 

#file.write("This is first file operation using python\n") 
#file.close

#print "Hello World"

