# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:01:17 2020

@author: xfang13, glblank
"""
# IT340 - Intro to AI
# Dr. Xing Fang
# Expanded by Gordon (Tre) Blankenship

# A* Search
# f(n) = g(n) + h(n)
# where n is a node, g(n) is the distance from start to n
# and h(n) is the estimated distance to the end from n
# 3 Provided test cases with heuristics specific
# to each graph

#import operator
from heapq import heappush as push
from heapq import heappop as pop

class Node:
     def __init__(self, n, g, heurs):
          self.parent = None
          self.name = n
          self.g = g
          self.h = heurs[n]
     
     def f(self):
          return self.g + self.h

     def __lt__(self, other):
          return self.f() < other.f()

# Main Test Case Arad -> Bucharest
Romania_Map = {'Oradea':{'Zerind':71,'Sibiu':151},
               'Zerind':{'Arad':75,'Oradea':71},
               'Arad':{'Zerind':75,'Sibiu':140,'Timisoara':118},
               'Timisoara':{'Arad':118,'Lugoj':111},
               'Lugoj':{'Timisoara':111,'Mehadia':70},
               'Mehadia':{'Lugoj':70,'Drobeta':75},
               'Drobeta':{'Mehadia':75,'Craiova':120},
               'Craiova':{'Drobeta':120,'Rimnicu Vilcea':146,'Pitesti':138},
               'Rimnicu Vilcea':{'Craiova':146,'Sibiu':80,'Pitesti':97},
               'Sibiu':{'Oradea':151,'Arad':140,'Fagaras':99,'Rimnicu Vilcea':80},
               'Fagaras':{'Sibiu':99,'Bucharest':211},
               'Pitesti':{'Rimnicu Vilcea':97,'Craiova':138,'Bucharest':101},
               'Bucharest':{'Fagaras':211,'Pitesti':101,'Giurgiu':90,'Urziceni':85},
               'Giurgiu':{'Bucharest':90},
               'Urziceni':{'Bucharest':85,'Vaslui':142,'Hirsova':98},
               'Neamt':{'Iasi':87},
               'Iasi':{'Neamt':87,'Vaslui':92},
               'Vaslui':{'Iasi':92,'Urziceni':142},
               'Hirsova':{'Urziceni':98,'Eforie':86},
               'Eforie':{'Hirsova':86}           
              }

Heuristics = {'Oradea':380,
               'Zerind':374,
               'Arad':366,
               'Timisoara':329,
               'Lugoj':244,
               'Mehadia':241,
               'Drobeta':242,
               'Craiova':160,
               'Rimnicu Vilcea':193,
               'Sibiu':253,
               'Fagaras':176,
               'Pitesti':100,
               'Bucharest':0,
               'Giurgiu':77,
               'Urziceni':80,
               'Neamt':234,
               'Iasi':226,
               'Vaslui':199,
               'Hirsova':151,
               'Eforie':161           
              }

# Extra Test Case S -> G
G = {'A':{'B':2,'C':5,'G':12},
     'B':{'C':2,},
     'C':{'G':3},
     'G':{},
     'S':{'B':4,'A':1}
     }

H = {'S':7,'A':6,'B':2,'C':1,'G':0}

# Extra Test Case A -> P
g2 = {'A':{'B':5, 'C':5},
      'B':{'A':5, 'C':4, 'D':3},
      'C':{'A':5, 'B':4, 'D':7, 'E':5, 'H':8},
      'D':{'B':3, 'C':7, 'H':11, 'K':16, 'L':13, 'M':14},
      'E':{'C':7, 'F':4, 'H':5},
      'F':{'E':4, 'G':9},
      'G':{'F':9, 'N':12},
      'H':{'C':8, 'D':11, 'E':5, 'I':3},
      'I':{'H':3, 'J':4},
      'J':{'I':4, 'N':3, 'P':8},
      'K':{'D':16, 'L':5, 'P':4, 'N':7},
      'L':{'D':13, 'K':5, 'M':9, 'O':4},
      'M':{'D':14, 'L':9, 'O':5},
      'N':{'G':12, 'J':3, 'K':7, 'P':7},
      'O':{'L':4, 'M':5},
      'P':{'J':8, 'K':4, 'N':7}}

h2 = {'A':16, 'B':17, 'C':13, 'D':16, 'E':16, 'F':20, 'G':17, 'H':11, 'I':10, 'J':8, 'K':4, 'L':7, 'M':10, 'N':7, 'O':5, 'P':0}

#Finds the shortest path to target from source
def solve(source, target, graph, heurs):

     open_heap = [] # nodes left to search
     closed_list = [] # searched nodes

     first_node = Node(source, 0, heurs)

     push(open_heap, first_node) # add it to the open_heap

     while open_heap: # while the heap is not empty

          # create the current working node and remove from open
          current_node = open_heap[0]
          pop(open_heap)

          # if we reach the end node, we are done
          if current_node.name == target:
               return get_path(current_node)

          # check the entire list of nodes adjacent to the current node
          for next in list(graph[current_node.name].keys()):

               curr_cost = current_node.g + graph[current_node.name][next] # cost to get to current node
               next_node = Node(next, graph[current_node.name][next], heurs) # new node of the next in adjacency

               # if the node is unopened, and next's g is lower than current g
               if next_node in open_heap and next_node.g <= curr_cost:
                    pass # just skip to next iteration
               elif next_node in closed_list: # if its closed
                    if next_node.g <= curr_cost: # and the g is less than current g
                         pass # skip to next iteration
                    closed_list.remove(next_node) # then reopen the node
                    push(open_heap, next_node) # adding it to the open heap again
               else: # just add it to the open list
                    push(open_heap, next_node)
               
               # Move on to the next adjacent node
               next_node.g = curr_cost
               next_node.parent = current_node

          # add to the closed list once it has been fully searched
          closed_list.append(current_node)

# function to retrace the steps
# and also properly format into readable print
def get_path(node):

     path = []

     while node:
          path.insert(0, (node.g, node.name))
          node = node.parent

     print('')
     # Printing the shortest path, final g-cost is the total
     for i in range(0, len(path)):
          if path[i] != path[-1]:
               print(str(path[i][1]), end=' -> ')
          else:
               print(str(path[i][1]))
               print("Total Distance => " + str(path[i][0]))
     print('')

if __name__=="__main__":
     source = 'Arad'
     target = 'Bucharest'

     solve(source, target, Romania_Map, Heuristics)

     source = 'S'
     target = 'G'

     solve(source, target, G, H)

     source = 'A'
     target = 'P'

     solve(source, target, g2, h2)