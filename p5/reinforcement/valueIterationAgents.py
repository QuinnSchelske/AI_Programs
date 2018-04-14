# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections
import time

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()
        
        

    def runValueIteration(self):
         #Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
			tempValues = self.values.copy()
			for state in self.mdp.getStates():
				newVal = None
				for action in self.mdp.getPossibleActions(state):
					val = self.computeQValueFromValues(state, action)
					if newVal == None or val > newVal:
						newVal = val
				if newVal == None:
					newVal = 0
				tempValues[state] = newVal
			self.values = tempValues

    def getValue(self, state):
         #Return the value of the state (computed in __init__).
        return self.values[state]


    def computeQValueFromValues(self, state, action):
		"""
		Compute the Q-value of action in state from the
		value function stored in self.values.
		"""
		"*** YOUR CODE HERE ***"
		qval = 0
		for s1, prob in self.mdp.getTransitionStatesAndProbs(state, action):
			reward = self.mdp.getReward(state,action,s1)
			val = prob * (reward + (self.discount * self.getValue(s1)))
			qval = qval + val
		return qval

    def computeActionFromValues(self, state):
		"""
		The policy is the best action in the given state
		according to the values currently stored in self.values.
		
		You may break ties any way you see fit.  Note that if
		there are no legal actions, which is the case at the
		terminal state, you should return None.
		"""
		"*** YOUR CODE HERE ***"
		bestAction = None
		maxVal = None
		if self.mdp.isTerminal(state):
			return bestAction
		for action in self.mdp.getPossibleActions(state):
			val = self.computeQValueFromValues(state,action)
			if maxVal == None or val > maxVal:
				maxVal = val
				bestAction = action
		return bestAction
        
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for i in range(self.iterations):
			state = states[i % len(states)]
			if not self.mdp.isTerminal(state):
				newVal = None
				for action in self.mdp.getPossibleActions(state):
					val = self.computeQValueFromValues(state, action)
					if newVal == None or val > newVal:
						newVal = val
				if newVal == None:
					newVal = 0
				self.values[state] = newVal

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        
        predecessors = {}
        for s in states:
            predecessors[s] = set()  
        for s1 in states:
			for a in self.mdp.getPossibleActions(s1):
				for post, prob in self.mdp.getTransitionStatesAndProbs(s1, a):
					if prob > 0:
						predecessors[post].add(s1)
        priQue = util.PriorityQueue()
        for s in states:
			if not self.mdp.isTerminal(s):
				v = self.values[s]
				highQ = max(self.computeQValueFromValues(s,a) for a in self.mdp.getPossibleActions(s))
				diff = abs(v - highQ)
				priQue.push(s, -diff)
        for i in range(self.iterations):
			if priQue.isEmpty():
				return
			s = priQue.pop()
			self.values[s] = max(self.computeQValueFromValues(s,a) for a in self.mdp.getPossibleActions(s))
			for p in list(predecessors[s]):
				if not self.mdp.isTerminal(p):
					curVal = self.values[p]
					highQ = max(self.computeQValueFromValues(p,a) for a in self.mdp.getPossibleActions(p))
					diff = abs(curVal - highQ)
					if diff > self.theta:
						priQue.update(p, -diff)
					
			
        
        

