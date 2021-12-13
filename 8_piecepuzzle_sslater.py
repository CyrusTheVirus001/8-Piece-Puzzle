# -*- coding: utf-8 -*-
"""8_PiecePuzzle_sslater.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iy5KGAc-RstzmJiD2F4bz9ay9Mow0hZO

Sheldon Slater</p>
810865586</p>
AI DFS, BFS, A* on 8-Piece Puzzle
"""

from google.colab import drive
drive.mount('/content/drive')

def Get_GameStates(Data_JSON):
  PuzzleState = Data_JSON['start']
  PuzzleGoal = Data_JSON['goal']
  PuzzleDimension = Data_JSON['n']
  if (len(PuzzleState) != PuzzleDimension)&(len(PuzzleState[0])!= PuzzleDimension):
    print("ERROR IN PuzzleState Dimensions!")
    return
  if (len(PuzzleGoal) != PuzzleDimension)&(len(PuzzleGoal[0])!= PuzzleDimension):
    print("ERROR IN PuzzleGoal Dimensions!")
    return
  if (PuzzleDimension <= 0):
    print("ERROR IN Puzzle Dimensions!")
    return
  
  print("Valid Puzzle")
  return PuzzleState,PuzzleGoal,PuzzleDimension

import json

file_path_1mov = '/content/drive/MyDrive/8_piece_puzzle_data/1-move.json'
file_path_triv = '/content/drive/MyDrive/8_piece_puzzle_data/trivial.json'
JSON_Data_1mov = json.load(open(file_path_1mov))
JSON_Data_triv = json.load(open(file_path_triv))

puzzle_state, puzzle_goal, n_dim = Get_GameStates(JSON_Data_1mov)

puzzle_state

def get_ZeroPiece_loc(PuzzleState,dimension):
  for i in range(dimension):
    for j in range(dimension):
      if (PuzzleState[i][j]== 0):
        return [j,i]
  print("Error '0' not Found")
  return

def check_Goal(gameState, goalState, dimension):
  for i in range(dimension):
    for j in range(dimension):
      if(gameState[i][j] != goalState[i][j]):
        return False
  return True

def Simple_Rules(Zero_Piece_loc):
  Rules = [] 
  if Zero_Piece_loc[0] != 0: Rules.append('L') #can_move_left
  if Zero_Piece_loc[0] != 2: Rules.append('R') #can_move_right
  if Zero_Piece_loc[1] != 0: Rules.append('U') #can_move_up
  if Zero_Piece_loc[1] != 2: Rules.append('D') #can_move_down
  return Rules

def Apply_Rule(gameState,Zero_Piece_loc,move):
  x = Zero_Piece_loc[0]
  y = Zero_Piece_loc[1]
  GS = [x[:] for x in gameState]
  if move == 'L':
    temp = GS[y][x-1]
    GS[y][x-1] = 0
    GS[y][x] = temp
  elif move == 'R':
    temp = GS[y][x+1]
    GS[y][x+1] = 0
    GS[y][x] = temp
  elif move == 'U':
    temp = GS[y-1][x]
    GS[y-1][x] = 0
    GS[y][x] = temp
  elif move == 'D':
    temp = GS[y+1][x]
    GS[y+1][x] = 0
    GS[y][x] = temp
  
  return GS

def backTrack(gameState, goalState, Result_Bin, depth, puzzle_Dimension,dictionairy,keyID,nodesVisited):
  Rules = []
  depth-=1;
  nodesVisited[0]+=1
  zero_pos = get_ZeroPiece_loc(gameState,puzzle_Dimension)
  if check_Goal(gameState,goalState,puzzle_Dimension):
    return 1

  if depth == 0:
    return 0

  if gameState in dictionairy.values():
    return 0
  else:
    dictionairy[keyID] = [x[:] for x in gameState]
    keyID+=1

  Rules = Simple_Rules(zero_pos)
  for i in Rules:
    R = i
    zero_pos = get_ZeroPiece_loc(gameState,puzzle_Dimension)
    newGameState = (Apply_Rule(gameState, zero_pos, R))

    if (backTrack(newGameState, goalState, Result_Bin, depth, puzzle_Dimension, dictionairy,keyID,nodesVisited)) != 0:
      Result_Bin.append(R)
      return 1

  return 0

file_path_1mov = '/content/drive/MyDrive/8_piece_puzzle_data/1-move.json'
file_path_triv = '/content/drive/MyDrive/8_piece_puzzle_data/trivial.json'
file_path_2mov = '/content/drive/MyDrive/8_piece_puzzle_data/2-moves.json'
file_path_10mov = '/content/drive/MyDrive/8_piece_puzzle_data/10-moves.json'
file_path_25mov = '/content/drive/MyDrive/8_piece_puzzle_data/25-moves.json'
file_path_problem_1 = '/content/drive/MyDrive/8_piece_puzzle_data/problem-1.json'
file_path_15mov = '/content/drive/MyDrive/8_piece_puzzle_data/15-moves.json'
file_path_20mov = '/content/drive/MyDrive/8_piece_puzzle_data/20-moves.json'
JSON_Data_1mov = json.load(open(file_path_1mov))
JSON_Data_triv = json.load(open(file_path_triv))
JSON_Data_2mov = json.load(open(file_path_2mov))
JSON_Data_10mov = json.load(open(file_path_10mov))
JSON_Data_25mov = json.load(open(file_path_25mov))
JSON_Data_15mov = json.load(open(file_path_15mov))
JSON_Data_20mov = json.load(open(file_path_20mov))
JSON_Data_problem_1 = json.load(open(file_path_problem_1))
puzzle_state, puzzle_goal, n_dim = Get_GameStates(JSON_Data_15mov)
print(puzzle_state)

import time

results = []
dictionairy = {}
key_ID = 0
nodesVisited = [0];
start_time = time.perf_counter()
backTrack(puzzle_state,puzzle_goal,results,30,n_dim,dictionairy,key_ID,nodesVisited)
end_time = time.perf_counter()

results.reverse()

print("Initial Puzzle: ")
print(puzzle_state)
print("Goal: ")
print(puzzle_goal)
print("")
print("Solution:")
print(results)
print("Steps: ", len(results))
print("Nodes Visited: ", nodesVisited[0])
print("Performance Time: ", end_time-start_time, "sec")
print("Hardware: Python 3 Google Compute Engine backend")

class node:
  def __init__(self, parent, gameState, move):
    self.parent = parent
    self.gameState = gameState
    self.move = move

def BFS(puzzle_state,goal_state):
  start_node = node(None,puzzle_state,'S')
  closed_List = []
  Open_List = []
  nodes_visited = 0
  
  Open_List.append(start_node)

  while len(Open_List) > 0:
    current_node = Open_List.pop(0)
    nodes_visited += 1
    closed_List.append(current_node)
    if check_Goal(current_node.gameState,goal_state,3):
      return Create_Path(current_node), nodes_visited

    zero_Pos = get_ZeroPiece_loc(current_node.gameState,3)
    Rules = Simple_Rules(zero_Pos)
    for r in Rules:
      new_Node = node(current_node,Apply_Rule(current_node.gameState,zero_Pos,r),r)
      exists = False
      for n in Open_List:
        if check_Goal(new_Node.gameState,n.gameState,3): exists = True
      for n in closed_List:
        if check_Goal(new_Node.gameState,n.gameState,3): exists = True
      if exists==False: Open_List.append(new_Node)


def Create_Path(Finish_Node):
  Path_Node = Finish_Node
  path = []
  while Path_Node.parent != None:
    path.append(Path_Node.move)
    Path_Node = Path_Node.parent
  return path

start_time = time.perf_counter()
Solution,nodes_visited01 = BFS(puzzle_state,puzzle_goal)
end_time = time.perf_counter()

Solution.reverse()

print("Initial Puzzle: ")
print(puzzle_state)
print("Goal: ")
print(puzzle_goal)
print("")
print("Solution:")
print(Solution)
print("Steps: ", len(Solution))
print("Nodes Visited: ", nodes_visited01)
print("Performance Time: ", end_time-start_time, "sec")
print("Hardware: Python 3 Google Compute Engine backend")

def manhatten_Distance(gameState,GoalState,dimension):
    sumDistances = 0
    for i in range(dimension):
      for j in range(dimension):
        target = gameState[i][j]
        for x in range(dimension):
          for y in range(dimension):
            if GoalState[x][y] == target:
              gY = y+1
              gX = x+1
              break
        x_value = i+1
        y_value = j+1
        dist = abs(x_value - gX) + abs(y_value - gY)
        sumDistances += dist
    return sumDistances

class nodeA:
  def __init__(self, parent, gameState, move,costg,costh):
    self.parent = parent
    self.gameState = gameState
    self.move = move
    self.costg = costg
    self.costh = costh

def get_function(NODE):
  return NODE.costg+NODE.costh    

def algorithm_Astar(puzzle_state,goal_state):
  start_node = nodeA(None,puzzle_state,'S',0,manhatten_Distance(puzzle_state,goal_state,3))
  closed_List = []
  Open_List = []
  nodes_visited = 0
  
  Open_List.append(start_node)

  while len(Open_List) > 0:
    Open_List.sort(key=get_function)
    current_node = Open_List.pop(0)
    nodes_visited+=1
    closed_List.append(current_node)
    if check_Goal(current_node.gameState,goal_state,3):
      return Create_Path(current_node),nodes_visited

    zero_Pos = get_ZeroPiece_loc(current_node.gameState,3)
    Rules = Simple_Rules(zero_Pos)
    for r in Rules:
      new_Node = nodeA(current_node,Apply_Rule(current_node.gameState,zero_Pos,r),r,current_node.costg+1,0)
      new_Node.costh = manhatten_Distance(new_Node.gameState,goal_state,3)
      exists = False
      
      
      for n in Open_List:
        if check_Goal(new_Node.gameState,n.gameState,3): exists = True
      for n in closed_List:
        if check_Goal(new_Node.gameState,n.gameState,3): exists = True
      if exists==False: Open_List.append(new_Node)

start_time = time.perf_counter()
solution,n = algorithm_Astar(puzzle_state,puzzle_goal)
end_time = time.perf_counter()

solution.reverse()

print("Initial Puzzle: ")
print(puzzle_state)
print("Goal: ")
print(puzzle_goal)
print("")
print("Solution:")
print(solution)
print("Steps: ", len(solution))
print("Nodes Visited: ", n)
print("Performance Time: ", end_time-start_time, "sec")
print("Hardware: Python 3 Google Compute Engine backend")