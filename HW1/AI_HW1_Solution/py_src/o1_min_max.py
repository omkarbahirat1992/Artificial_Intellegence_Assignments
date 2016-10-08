import sys

#cost_mat = []
#state_mat = []
player = ' '
given_depth = 0
row = -1
column = -1

column_name = ['A', 'B', 'C', 'D', 'E']

def init_mat(filename, cost_mat, state_mat):
	global given_depth
	count = 5
	fp = open(filename, "r")
	algo = int(fp.readline())
	player = fp.readline()
	given_depth = int(fp.readline())
	#print "\nGiven depth = "
	#print given_depth
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
		string = '\n' + string
		o_file.write(string)
		print(string)
	o_file.close()
	print '\n'

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
		print ("player " + player + " has won the match")
	elif (hn < 0):
		print ("player " + player + " has lost the match")


def get_copy(state_mat):
	temp_mat = []
	for each_row in state_mat:
		if isinstance(each_row,list):
			temp_mat.append(get_copy(each_row))
		else:
			temp_mat.append(each_row)
	return temp_mat



def reset_output_files():
	o_file = open("next_step.txt", "w")
	o_file.close()

	o_file = open("traverse_log.txt", "w")
	o_file.write("Node" + "," + "Depth" + "," + "Value" + "\n")
	o_file.close()

def write_traverse_log_file(row, column, depth, value):
	node = column_name[column] + str(row + 1)
	o_file = open("traverse_log.txt", "a")
	value_str = str(value)
	if (depth == 0):
		node = "root"
	if (value == 2000):
		value_str = "Infinity"
	elif (value == -2000):
		value_str = "-Infinity"

	string = node + ',' + str(depth) + ',' + value_str + '\n'
	o_file.write(string)
	o_file.close()

def min_max(cost_mat, state_mat, cur_depth, player, opponent, flag):
	#print "cur_depth"
	#print cur_depth
	#print given_depth
	#print "\n"
	global row
	global column
	if (cur_depth == given_depth):
		#display_mat(state_mat)
		return (evaluate(cost_mat, state_mat, 'X'))

	if (flag == 'MAX'):
		key = -2000
		for i in range(len(state_mat)):
			for j in range(len(state_mat)):
				if (state_mat[i][j] == '*'):
					temp_mat = get_copy(state_mat)
					temp_mat[i][j] = player
					#display_mat(temp_mat)
					write_traverse_log_file(i, j, cur_depth, key)
					#exit(0)

					#temp_cost = cost_mat[i][j]
					#print temp_cost

					if (chk_raid(state_mat, i, j, player) == True):
						#temp_cost = temp_cost + get_conquered_cost(cost_mat, temp_mat, i, j, player)
						update_conquered_cell(temp_mat, i, j, player)
						#print "it is a raid"
					#exit(0)

					temp_cost = min_max(cost_mat, temp_mat, cur_depth + 1, opponent, player, 'MIN')
					#print "current_dept1"
					#print temp_cost
					if (temp_cost > key):
						key = temp_cost
						#write_traverse_log_file(i, j, cur_depth, key)

						row = i
						column = j
					write_traverse_log_file(i, j, cur_depth + 1, temp_cost)

		return key
		
	elif (flag == 'MIN'):
		key = 2000
		for i1 in range(len(state_mat)):
			for j1 in range(len(state_mat)):
				if (state_mat[i1][j1] == '*'):
					temp_mat = get_copy(state_mat)
					temp_mat[i1][j1] = player

					write_traverse_log_file(i1, j1, cur_depth, key)

					#temp_cost = cost_mat[i][j]
					if (chk_raid(state_mat, i1, j1, player) == True):
						#temp_cost = temp_cost + get_conquered_cost(cost_mat, temp_mat, i, j, player)
						update_conquered_cell(temp_mat, i1, j1, player)

					temp_cost = min_max(cost_mat, temp_mat, cur_depth + 1, opponent, player, 'MAX')
					if (temp_cost < key):
						key = temp_cost
 						#write_traverse_log_file(i, j, cur_depth, key)
						row = i1
						column = j1
					#print cur_depth

					write_traverse_log_file(i1, j1, cur_depth + 1, temp_cost)

		return key

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
	reset_output_files()
#	read_file(file)
	init_mat(file, cost_mat, state_mat)
#	print "\ngiven depth = \n" + str(given_depth)

#TODO: Make "player" input driven
	min_max(cost_mat, state_mat, 0, 'X', 'O', 'MAX')
	
#	display_mat(cost_mat)
#	display_mat(state_mat)

#	GBFS(cost_mat, state_mat, 'X')
#	display_mat(state_mat)
#	write_next_state(state_mat)


if __name__ == "__main__":
	main(sys.argv[1:])
