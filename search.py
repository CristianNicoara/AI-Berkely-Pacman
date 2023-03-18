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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ("Start:", problem.getStartState())
    print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print ("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from game import Directions
    from game import Stack

    initialState = problem.getStartState()
    stack = util.Stack()
    visited = []
    solution = []

    stack.push((initialState,[]))

    while not stack.isEmpty():
        currentNode = stack.pop()

        currentSol = currentNode[1]

        if problem.isGoalState(currentNode[0]):
            return currentSol

        visited.append(currentNode[0])
        succesors = problem.getSuccessors(currentNode[0])
        for node in succesors:
            if node[0] not in visited:
                stack.push((node[0],currentSol+[node[1]]))

    return solution


    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Queue

    initialState = problem.getStartState()
    visited = [initialState]

    queue = util.Queue()
    queue.push((initialState, []))

    while not queue.isEmpty():
        currentNode = queue.pop()

        currentSol = currentNode[1]

        if problem.isGoalState(currentNode[0]):
            return currentSol
        successors = problem.getSuccessors(currentNode[0])
        for node in successors:
            if node[0] not in visited:
                visited.append(node[0])
                queue.push([node[0], currentSol + [node[1]]])
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from game import PriorityQueue
    initialState = problem.getStartState()
    visited = [initialState]

    queue = util.PriorityQueue()
    queue.push([initialState, [], 0], 0)

    while not queue.isEmpty():
        currentNode = queue.pop()

        currentSol = currentNode[1]

        if problem.isGoalState(currentNode[0]):
            return currentSol

        successors = problem.getSuccessors(currentNode[0])
        for node in successors:
            if node[0] not in visited or problem.isGoalState(node[0]):
                visited.append(node[0])
                queue.push([node[0], currentSol + [node[1]],node[2] + currentNode[2]], node[2] + currentNode[2])

    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from game import PriorityQueue

    initialState = problem.getStartState()
    priorityQueue = util.PriorityQueue()
    visited = []

    priorityQueue.push([initialState, [], 0], 0)

    while not priorityQueue.isEmpty():
        currentNode = priorityQueue.pop()

        currentSol = currentNode[1]

        visited.append((currentNode[0],currentNode[2]))
        if problem.isGoalState(currentNode[0]):
            return currentSol
        else:
            succesors = problem.getSuccessors(currentNode[0])
            for node in succesors:
                cost = problem.getCostOfActions(currentSol + [node[1]])

                isVisited = False
                for visitedNodes in visited:
                    if (node[0] == visitedNodes[0]) and (cost >= visitedNodes[1]):
                        isVisited = True

                if (not isVisited) or (problem.isGoalState(node[0])):
                    priorityQueue.push([node[0], currentSol + [node[1]], cost],
                                       cost + heuristic(node[0], problem))
                    visited.append((node[0], cost))


    #util.raiseNotDefined()


def iterativeDeepeningSearch(problem):

    from game import Directions

    stack = util.Stack()
    limit = 0
    initialState = problem.getStartState()

    while True:
        visited = []
        stack.push((initialState,[],0))
        currentNode = stack.pop()
        visited.append(currentNode[0])

        while not problem.isGoalState(currentNode[0]):
            successors = problem.getSuccessors(currentNode[0])
            for successor in successors:
                if (not successor[0] in visited) and (currentNode[2] + successor[2] <= limit):
                    stack.push((successor[0],currentNode[1] + [successor[1]],currentNode[2] + successor[2]))
                    visited.append(successor[0])

            if stack.isEmpty():
                break

            currentNode = stack.pop()

        if problem.isGoalState(currentNode[0]):
            return currentNode[1]

        limit += 1









# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
