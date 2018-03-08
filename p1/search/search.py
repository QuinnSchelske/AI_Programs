# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]
   
class Node:
	def __init__(self, state, parent, action,cost):
		self.state = state
		self.action = action
		self.parent = parent
		self.cost = cost

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    curr  = (problem.getStartState(), [])
    stack = util.Stack()
    visited = [problem.getStartState()]
    stack.push(curr)
    while (not stack.isEmpty()):
		curr = stack.pop()
		actions = curr[1]
		state = curr[0]
		succ = problem.getSuccessors(state)
		for node in succ:
			nextState = node[0]
			nextAction = node[1]
			if nextState not in visited:
				if problem.isGoalState(nextState):
					actions.append(nextAction)
					return actions
				else:
					#print "pushing .. :", nextState
					stack.push((nextState, actions + [nextAction]))
					visited.append(nextState)
    
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    curr  = (problem.getStartState(), 'Stop')
    stack = util.Stack()
    start = problem.getStartState()
    #visited = [problem.getStartState()]
    explored = []
    actionList= []
    stack.push(curr)
    while (not stack.isEmpty()):
		curr = stack.pop()
		action = curr[1]
		state = curr[0]
		if action!='Stop':
			actionList.append(action)
		if problem.isGoalState(state):
			return actionList
		succ = problem.getSuccessors(state)
		if state == start:
			actionList=[]

		explored.append(state)
		for node in succ:
			nextState = node[0]
			nextAction = node[1]
			if(nextState in explored):
				print "removing from action list...", actionList[-1]
				if len(actionList)!=0:
					actionList.remove(actionList[-1])
			if nextState not in explored:
			#print "pushing .. :", nextState
			    stack.push((nextState, nextAction))
			    #visited.append(nextState)"""
    node = Node(problem.getStartState(), 'None' , 'Stop', 0)
    closed = []
    fringe = Stack()
    fringe.push(node)
    while(1):
		if len(fringe)==0:
			return 0
		node = fringe.pop()
		if problem.isGoalState(node):
			return #node.list()
		if node.state not in closed:
			close.append(node.state)
			succ = problem.getSuccessors(node.state)
			for child in succ:
				childNode = Node(child[0], node.state, child[1], 0)
				fringe.push(childNode)

def breadthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:"""

    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    curr  = (problem.getStartState(), [])
    stack = util.Queue()
    visited = [problem.getStartState()]
    stack.push(curr)
    while (not stack.isEmpty()):
		curr = stack.pop()
		actions = curr[1]
		state = curr[0]
		succ = problem.getSuccessors(state)
		for node in succ:
			nextState = node[0]
			nextAction = node[1]
			if nextState not in visited:
				if problem.isGoalState(nextState):
					actions.append(nextAction)
					return actions
				else:
					#print "pushing .. :", nextState
					stack.push((nextState, actions + [nextAction]))
					visited.append(nextState)
    #util.raiseNotDefined()
def cost(problem, actions):
	return problem.getCostOfActions(actions)
def uniformCostSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:"""

    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #Our cost function is a call to the get cost of actions for our list of actions at that state
    cost = lambda curr: problem.getCostOfActions(curr[1])
    curr  = (problem.getStartState(), ["Stop"] ,0)
    stack = util.PriorityQueueWithFunction(cost)
    visited = [problem.getStartState()]
    stack.push(curr)
    while (not stack.isEmpty()):
		curr = stack.pop()
		actions = curr[1]
		state = curr[0]
		succ = problem.getSuccessors(state)
		for node in succ:
			nextState = node[0]
			nextAction = node[1]
			if nextState not in visited:
				if problem.isGoalState(nextState):
					actions.append(nextAction)
					return actions
				else:
					#print "pushing .. :", nextState
					stack.push((nextState, actions + [nextAction]))
					visited.append(nextState)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #Our cost function is a call to the get cost of actions for our list of actions at that state
    cost = lambda curr: problem.getCostOfActions(curr[1])+ heuristic(curr[0], problem)
    curr  = (problem.getStartState(), ["Stop"] ,0)
    stack = util.PriorityQueueWithFunction(cost)
    visited = [problem.getStartState()]
    stack.push(curr)
    while (not stack.isEmpty()):
		curr = stack.pop()
		actions = curr[1]
		state = curr[0]
		succ = problem.getSuccessors(state)
		for node in succ:
			nextState = node[0]
			nextAction = node[1]
			if nextState not in visited:
				if problem.isGoalState(nextState):
					actions.append(nextAction)
					return actions
				else:
					#print "pushing .. :", nextState
					stack.push((nextState, actions + [nextAction]))
					visited.append(nextState)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
