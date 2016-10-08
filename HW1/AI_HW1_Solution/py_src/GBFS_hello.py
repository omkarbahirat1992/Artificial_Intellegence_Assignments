import sys

#cost_mat = []
#state_mat = []
player = ' '

def init_mat(filename, cost_mat, state_mat):
	count = 5
	fp = open(filename, "r")
	algo = int(fp.readline())
	player = fp.readline()
	cut_depth = int(fp.readline()) 
	for line in fp.readlines():
		if (count > 0):
			cost_mat.append([])
			for cost in line.split():
				cost_mat[-1].append(int(cost))
			count = count - 1
			continue

		state_mat.append([])
		for letter in line:
			state_mat[-1].append(letter)

def display_mat(mat):
	for i in range(len(mat)):
		string = ' '
		for j in range(len(mat)):
#			print i
			string = string + str(mat[i][j])
#			string = string + ' '
		print(string)
	print '\n'

def write_next_state(mat):
	o_file = open("next_state.txt", "w")
	for i in range(len(mat)):
		string = ' '
		for j in range(len(mat)):
#			print i
			string = string + str(mat[i][j])
#			string = string + ' '
#		print(string)
		string = '\n' + string
		o_file.write(string)
#	o_file.write('\n')
	o_file.close()
#	print '\n'

def read_file(filename):
	fp = open(filename, "r")
	for line in fp.readlines():
		print(line)
	fp.close

def get_value(cost_mat, state_mat, player):
	cost = 0
	for i in range(len(state_mat)):
		for j in range(len(state_mat)):
			if (state_mat[i][j] == player):
				cost = cost + cost_mat[i][j]
	return cost


def evaluate(cost_mat, state_mat, player):
	if (player == 'X'):
		return get_value(cost_mat, state_mat, 'X') - get_value(cost_mat, state_mat, 'O')
	elif (player == 'O'):
		return get_value(cost_mat, state_mat, 'O') - get_value(cost_mat, state_mat, 'X')


def chk_raid(state_mat, row, column, player):
	if (row > 0 and state_mat[row - 1][column] == player):
		return True
	if (row < 4 and state_mat[row + 1][column] == player):
		return True
	if (column > 0 and state_mat[row][column - 1] == player):
		return True
	if (column < 4 and state_mat[row][column + 1] == player):
		return True
	
	return False


def get_conquered_cost(cost_mat, state_mat, row, column, player):
	if (player == 'X'):
		opponent = 'O'
	if (player == 'O'):
		opponent = 'X'
	conq_cost = 0

	if (row > 0 and state_mat[row - 1][column] == opponent):
		conq_cost = conq_cost + (2 * cost_mat[row - 1][column])

	if (row < 4 and state_mat[row + 1][column] == opponent):
		conq_cost = conq_cost + (2 * cost_mat[row + 1][column])

	if (column > 0 and state_mat[row][column - 1] == opponent):
		conq_cost = conq_cost + (2 * cost_mat[row][column - 1])

	if (column < 4 and state_mat[row][column + 1] == opponent):
		conq_cost = conq_cost + (2 * cost_mat[row][column + 1])
	
	return conq_cost


def update_conquered_cell(state_mat, row, column, player):
	if (player == 'X'):
		opponent = 'O'
	if (player == 'O'):
		opponent = 'X'
	conq_cost = 0

	if (row > 0 and state_mat[row - 1][column] == opponent):
		state_mat[row - 1][column] = player

	if (row < 4 and state_mat[row + 1][column] == opponent):
		state_mat[row + 1][column] = player

	if (column > 0 and state_mat[row][column - 1] == opponent):
		state_mat[row][column - 1] = player

	if (column < 4 and state_mat[row][column + 1] == opponent):
		state_mat[row][column + 1] = player
	
	return conq_cost
	

#1 = X
#2 = O
def GBFS(cost_mat, state_mat, player):
	hn = evaluate(cost_mat, state_mat, player)

	print("hn is " ) +  str(hn)

	row = 0
	column = 0
	max_cost = -999999999
	raid = False
	temp_raid = False
	
	for i in range(len(cost_mat)):
		for j in range(len(cost_mat)):
			temp_raid = False

			if (state_mat[i][j] == '*'):
				temp_cost = hn + cost_mat[i][j]  
				temp_raid = chk_raid(state_mat, i, j, player)
				if (temp_raid == True ):
					temp_cost = temp_cost + get_conquered_cost(cost_mat, state_mat, i, j, player)
				if (temp_cost > max_cost):
					max_cost = temp_cost
					row = i
					column = j
					raid = temp_raid

	if (max_cost > -999999999):
		state_mat[row][column] = player
		if (raid == True):
			update_conquered_cell(state_mat, row, column, player)
	elif (hn == 0):
		print ("Match is draw")
	elif (hn > 0):
		printf ("player " + player + " has won the match")
	elif (hn < 0):
		printf ("player " + player + " has lost the match")


def min_max(state_mat, depth):
	if (depth == 0):
		print("\nDept = 0\n")
		display_mat(state_mat)
		return

	print ("\nin min_max \n")
	display_mat(state_mat)
	state_mat[0][2] = '*'
	state_mat[0][3] = '*'
	min_max(state_mat, depth - 1)
	print ("\nBack to original call \n")
	display_mat(state_mat)

def main(argv):
	cost_mat = []
	state_mat = []
	file = ' '
	try:
		if (argv[0] == '-i'):
			file = argv[1]
		else:
			sys.exit(2)	
	except:
		print 'hello.py -i <inputfile>'
		sys.exit(2)
	print "file name is:", file
#	read_file(file)
	init_mat(file, cost_mat, state_mat)
	
#	display_mat(cost_mat)
#	display_mat(state_mat)

	GBFS(cost_mat, state_mat, 'X')
	write_next_state(state_mat)
	display_mat(state_mat)


#	min_max(state_mat, 1)

if __name__ == "__main__":
	main(sys.argv[1:])
