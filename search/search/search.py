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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # credit for DFS algo intuition: [CS188 FA23] Lecture 2 - Uninformed Search
    # at 53:00 mins: https://www.youtube.com/watch?v=qDFFxx_j5Xo
    # print("Start:", problem.getStartState())  # returns (x,y) pos
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    fringe = util.Stack()
    explored = set()
    start = problem.getStartState()

    # edge case / best case
    if problem.isGoalState(start):
        return []
    fringe.push(([], start))  # store the states and their paths as tuple

    while fringe.isEmpty() == False:
        actions, state = fringe.pop()
        # current state is the goal, so return list of actions
        if problem.isGoalState(state):
            return actions
        explored.add(state)
        # search tree
        for successor_state, action, _ in problem.getSuccessors(state):
            appended_path = actions + [action]
            if successor_state not in explored:
                fringe.push((appended_path, successor_state))
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # credit for BFS algo intuition: [CS188 FA23] Lecture 2 - Uninformed Search
    # https://www.youtube.com/watch?v=qDFFxx_j5Xo
    fringe = util.Queue()
    explored = []
    start = problem.getStartState()
    # edge case / best case
    if problem.isGoalState(start):
        return []
    fringe.push(([], start))
    # print(fringe.list[0])
    while fringe.isEmpty() == False:
        actions, state = fringe.pop()
        # to avoid expanding same node more than once
        if state in explored:
            continue
        explored.append(state)
        # current state is the goal, so return list of actions
        if problem.isGoalState(state):
            return actions
        # search tree
        for successor_state, action, _ in problem.getSuccessors(state):
            appended_path = actions + [action]
            if successor_state not in explored:
                fringe.push((appended_path, successor_state))
    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # credit for UCS algo intuition: [CS188 FA23] Lecture 2 - Uninformed Search
    # https://www.youtube.com/watch?v=qDFFxx_j5Xo
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    explored = set()
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    fringe.push((0, start, []), 0)  # ((triple), priority)
    # print(fringe.heap)
    while fringe.isEmpty() == False:
        cost, state, actions = fringe.pop()
        if problem.isGoalState(state):
            return actions
        if state in explored:
            continue
        explored.add(state)
        for successor_state, action, step_cost in problem.getSuccessors(state):
            # priority_or_cost = problem.getCostOfActions(actions)
            priority_or_cost = cost + step_cost
            if successor_state not in explored:
                # make cost same as priority so we take elems of same cost
                # to explore at each level
                fringe.update(
                    (priority_or_cost, successor_state, actions + [action]),
                    priority_or_cost,
                )
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # credit for A* search algo intuition: [CS188 FA23] Lecture 3 - Informed Search
    # at 39:00 mins https://www.youtube.com/watch?v=nS6x5K7byng
    explored = []
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    fringe.push((0, start, []), 0)  # ((triple), priority)

    while fringe.isEmpty() == False:
        cost, state, actions = fringe.pop()
        if problem.isGoalState(state):
            return actions
        if state in explored:
            continue
        explored.append(state)
        for successor_state, action, step_cost in problem.getSuccessors(state):
            priority_or_cost = cost + step_cost
            if successor_state not in explored:
                # priority = heuristic cost = ucs cost (cost + step_cost) + greedy cost (h(x))
                fringe.update(
                    (priority_or_cost, successor_state, actions + [action]),
                    priority_or_cost + heuristic(successor_state, problem),
                )
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
