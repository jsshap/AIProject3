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

        self.values_prime = util.Counter()

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        lambd = 0

        for s in self.mdp.getStates():
            self.values[s] = 0

        print "we're in this method", self.iterations
        for i in range (self.iterations):
            self.values = self.values_prime
            lambd = 0
            for s in mdp.getStates():
                max = 0
                for a in self.mdp.getPossibleActions(s):
                    sum = 0
                    nexts = self.mdp.getTransitionStatesAndProbs(s, a)
                    #t =  self.discount*sum([n[1]*self.values_prime[0]+ self.mdp.getReward(s,a,n[0]) for n in nexts])

                    for newState in nexts:
                        prob = newState[1]
                        state = newState[0]
                        reward = self.mdp.getReward(s, a, state)
                        sum += prob*self.values[newState] 
                        #should we do the reward here? it's the only place that makes sense

                    if sum>max:
                        max = sum
                self.values_prime[s] = max + self.mdp.getReward(s,None, None)#problem: reward function requires more args than we have
                if self.values_prime[s] - self.values[s] > lambd:
                    lambd = self.values_prime[s] - self.values[s]
            # if lambd <  (epsilon*(1-self.discount))/self.discount:
            #     break   



                




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        succs = self.mdp.getTransitionStatesAndProbs(state, action)
        #list of (state, prob)
        total =0
        #print succs
        for s in succs:
            #print self.values[s[0]]
            total += s[1] * self.values[s[0]]
        #print total
        #add reward in this state and gamma * future reward
        currentReward = self.mdp.getReward(state, None, None)
        future = self.discount * total
        return future + currentReward


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.values[state] == 0:
            return None

        bestScore = 0
        bestMove = None
        actions = self.mdp.getPossibleActions(state)
        for a in actions:
            if self.computeQValueFromValues(state, a)> bestScore:
                bestMove = a
                bestScore = 0

        return bestMove
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
