import sys

#cost_mat = []	
#state_mat = []
player = ' '
given_depth = 0
row = -1
column = -1
algo = -1

column_name = ['A', 'B', 'C', 'D', 'E']

def init_mat(filename, cost_mat, state_mat):
	global given_depth
	global algo
	count = 5
	fp = open(filename, "r")
	algo = int(fp.readline())


	print "\nalgo = " + str(algo)
	
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
#		print(string)
	o_file.close()

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
	o_file = open("next_state.txt", "w")
	o_file.close()

	if (algo > 1):
		print "algo1 = " + str(algo) + "\n"

		o_file = open("traverse_log.txt", "w")
		if (algo == 2):
			o_file.write("Node" + "," + "Depth" + "," + "Value" + "\n")
		else:
			o_file.write("Node" + "," + "Depth" + "," + "Value" + ',' + "Alpha" + ',' + "Beta" + "\n")
		o_file.close()

def get_node(row, column):
	return (column_name[column] + str(row + 1))

	
def write_ab_traverse_log_file(node, depth, value, alpha, beta):
	#node = get_node(row, column)
	o_file = open("traverse_log.txt", "a")
	value_str = str(value)
	alpha_str = str(alpha)
	beta_str = str(beta)
	if (depth == 0):
		node = "root"
	if (value == 2000):
		value_str = "Infinity"
	elif (value == -2000):
		value_str = "-Infinity"
		
	if (alpha == 2000):
		alpha_str = "Infinity"
	elif (alpha == -2000):
		alpha_str = "-Infinity"
		
	if (beta == 2000):
		beta_str = "Infinity"
	elif (beta == -2000):
		beta_str = "Infinity"

	string = node + ',' + str(depth) + ',' + value_str + ',' + alpha_str + ',' + beta_str + '\n'
	o_file.write(string)
	o_file.close()
	
def write_traverse_log_file(node, depth, value):
	#node = get_node(row, column)
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



def min_max(node, cost_mat, state_mat, cur_depth, player, opponent, flag):
	global row
	global column
	final_state_mat = []
	max_key = -2000
	min_key = 2000

	if (cur_depth == given_depth):
#TODO: player passed over here should be dynamic
		return (evaluate(cost_mat, state_mat, 'X'))
	
	for i in range(len(state_mat)):
		for j in range(len(state_mat)):
			if (state_mat[i][j] == '*'):
				temp_mat = get_copy(state_mat)
				temp_mat[i][j] = player

				if (chk_raid(state_mat, i, j, player) == True):
					update_conquered_cell(temp_mat, i, j, player)

				if (flag == 'MAX'):
					write_traverse_log_flile(node, cur_depth, max_key)
					temp_cost = min_max(get_node(i, j), cost_mat, temp_mat, cur_depth + 1, opponent, player, 'MIN')
					write_traverse_log_file(get_node(i, j), cur_depth + 1, temp_cost)
					if (temp_cost > max_key):
						max_key = temp_cost
						final_state_mat = temp_mat
						row = i
						column = j

				if (flag == 'MIN'):
					write_traverse_log_file(node, cur_depth, min_key)
					temp_cost = min_max(get_node(i, j), cost_mat, temp_mat, cur_depth + 1, opponent, player, 'MAX')
					write_traverse_log_file(get_node(i, j), cur_depth + 1, temp_cost)
					if (temp_cost < min_key):
						min_key = temp_cost
						row = i
						column = j

	write_next_state(final_state_mat)
	if (flag == 'MAX'):
		return max_key
	else:
		return min_key
		


def alpha_beta(node, cost_mat, state_mat, cur_depth, player, opponent, flag, alpha_val, beta_val):
	global row
	global column
	final_state_mat = []
	val = 0
	alpha = 1
	beta = 2
	vab = [-2000, -2000, 2000]		#list of value, alpha and beta
	vab[alpha] = alpha_val
	vab[beta] = beta_val

	if (cur_depth == given_depth):
#TODO: player passed over here should be dynamic
		vab[val] = evaluate(cost_mat, state_mat, 'X')

		return vab
	
	for i in range(len(state_mat)):
		for j in range(len(state_mat)):
			if (state_mat[i][j] == '*'):
				temp_mat = get_copy(state_mat)
				temp_mat[i][j] = player

				if (chk_raid(state_mat, i, j, player) == True):
					update_conquered_cell(temp_mat, i, j, player)

				if (flag == 'MAX'):
					write_ab_traverse_log_file(node, cur_depth, vab[val], vab[alpha], vab[beta])
					vab = alpha_beta(get_node(i, j), cost_mat, temp_mat, cur_depth + 1, opponent, player, 'MIN', vab[alpha], vab[beta])
				
					write_ab_traverse_log_file(get_node(i, j), cur_depth + 1, vab[val], vab[alpha], vab[beta])
					if (vab[val] > vab[alpha]):
						vab[alpha] = vab[val]
						final_state_mat = temp_mat
						row = i
						column = j
					vab[beta] = 2000
					if (vab[alpha] > vab[val]):
						vab[val] = vab[alpha]
						
					if(vab[alpha] > vab[beta]):					
						print "got 1"
						return vab

				if (flag == 'MIN'):
					write_ab_traverse_log_file(node, cur_depth, vab[beta], vab[alpha], vab[beta])
					vab = alpha_beta(get_node(i, j), cost_mat, temp_mat, cur_depth + 1, opponent, player, 'MAX', vab[alpha], vab[beta])
					write_ab_traverse_log_file(get_node(i, j), cur_depth + 1, vab[val], vab[alpha], vab[beta])
					if (vab[alpha] >= vab[val]):
						print "got 2"
						return vab
					
					if (vab[val] < vab[beta]):
						vab[beta] = vab[val]
						row = i
						column = j
					
					vab[val] = vab[beta]


				

	write_next_state(final_state_mat)
	return vab

		
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
	reset_output_files()

	alpha_beta('root', cost_mat, state_mat, 0, 'X', 'O', 'MAX', -2000, +2000)
#	print "\ngiven depth = \n" + str(given_depth)

#TODO: Make "player" input driven
#	key = min_max('root', cost_mat, state_mat, 0, 'X', 'O', 'MAX')
#	write_traverse_log_file("root", 0, key)
#	display_mat(cost_mat)
#	display_mat(state_mat)

#	GBFS(cost_mat, state_mat, 'X')
#	display_mat(state_mat)
#	write_next_state(state_mat)


if __name__ == "__main__":
	main(sys.argv[1:])
























