import sys

board = []
state_board = []
filename = ' '

def Prepare_Board():
	line_count = 0

	file_pointer = open(filename, "r")
	al = int(file_pointer.readline())

	player = file_pointer.readline()
		
	cutoff = int(file_pointer.readline())

	for line in file_pointer.readlines():
		if (line_count < 5):
			board.append([])
			for point in line.split():
				board[-1].append(int(point))
			line_count = line_count + 1
			continue

		state_board.append([])
		for char in line:
			state_board[-1].append(char)

def calculate(player):
	point = 0
	for i in range(len(state_board)):
		for j in range(len(state_board)):
			if (state_board[i][j] == player):
				point = point + board[i][j]
	return point



def Greedy_Best_First_Search():
	final_row = 0
	final_column = 0
	max_point = -5000

	val =  calculate('X') - calculate('O')
	for i in range(len(board)):
		for j in range(len(board)):
			if (state_board[i][j] == '*'):
				temp_point = val + board[i][j]
				if (temp_point > max_point):
					max_point = temp_point
					final_row = i
					final_column = j

	if (max_point > -5000):
		state_board[final_row][final_column] = 'X'
		
	file_pointer = open("next_state.txt", "w")	
	
	for i in range(len(board)):
		string = ' '
		for j in range(len(board)):
			string = string + str(state_board[i][j])
		string = string + '\n'
		file_pointer.write(string)
	file_pointer.close()	
	

def main(argv):
	global filename

	filename = argv[1]

	Prepare_Board()
	Greedy_Best_First_Search()

if __name__ == "__main__":
	main(sys.argv[1:])
