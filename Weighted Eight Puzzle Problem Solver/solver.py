import pdqpq
import puzz
import sys
import random
import matplotlib.pyplot as plt


def eight_puzzle_is_goal(state):
    """check whether the state is goal state

    :param state: EightPuzzleBoard
    :return: boolean value:
        True: is goal state
        False: not goal state
    """
    goal = puzz.EightPuzzleBoard("012345678")
    if state == goal:
        return True
    else:
        return False


def bfs_cost(state):
    """return the cost in bfs which is simply 0

    :param state: EightPuzzleBoard, the current state
    :return: int
    """
    return 0


def traceback(state):
    """trace back to get the path
        return a list that contains all states in the path
    :return: list which element type is EightPuzzleBoard
    """
    path = [state]
    pred = state.predecessor
    while pred is not None:
        path.append(pred)
        pred = pred.predecessor
    path.reverse()
    return path


def bfs(gameboard, is_weight):
    """solve the Game with Breath-First-Search
    print:
        steps and states of solution
        Total path cost of solution
        Total number of states added to the frontier queue
        Total number of states popped from the frontier queue and expanded
    :param is_weight: boolean
    :param gameboard: string, the string that describe gameboard
    :return: void
    """
    # TODO:
    # create initial state:
    init = puzz.EightPuzzleBoard(gameboard)
    # create frontier queue and add initial state
    frontier = pdqpq.PriorityQueue()
    frontier.add(init)
    # set operation to initial state
    init.op = 'start'
    # num_front/num_explored record number of states added/popped to/out the frontier
    num_front = 1
    num_explored = 0
    # create explored list
    explored = set()

    # if the initial state is the goal state:
    if eight_puzzle_is_goal(init):
        print(0, '\t', "start", '\t', init)
        print("path cost: %d" % init.cost)
        print("frontier: %d" % num_front)
        print("expanded: %d" % num_explored)
        return 1

    while not frontier.empty():
        # if we have expanded 100000 nodes, print 'search halted' and exit
        if num_explored >= 100000:
            print("search halted")
            return 0

        # pop a state from frontier
        state = frontier.pop()
        # add it to the explored set
        explored.add(state)
        # update num_explored
        num_explored += 1
        # zero_coord: record the coordinate of '0' in the state:
        zero_coord = state.find('0')

        # k is the keyword we get from successors
        for k in state.successors():
            # next_state: the next possible state if we expand current state:
            next_state = state.successors()[k]
            # set operation and predecessor of next_state:
            next_state.op = k
            next_state.predecessor = state
            # record the total cost so far of next_state
            cost_with_k = ucost_cost(next_state, zero_coord, is_weight)
            next_state.cost = state.cost + cost_with_k

            if (next_state not in frontier) and (next_state not in explored):
                if eight_puzzle_is_goal(next_state):
                    # get the path
                    solution = traceback(next_state)
                    # set step to 0
                    step = 0
                    for sol in solution:
                        print(step, '\t', sol.op, '\t', sol)
                        step += 1
                    print("path cost: %d" % next_state.cost)
                    print("frontier: %d" % num_front)
                    print("expanded: %d" % num_explored)
                    tup = (state.cost, num_front, num_explored)
                    return tup
                else:  # if next_state is not goal state
                    frontier.add(next_state)
                    num_front += 1
    # if no solution found, print "failure"
    print("failure")
    return 0


def ucost_cost(state, coord, is_weight):
    """return the cost in cost which is path cost

    :param state: EightPuzzleBoard, the current state
    :param coord: tuple, coordinate of move that take place
    :param is_weight: boolean, check whether we weight
    :return: int
    """
    if is_weight:
        num_in_str = state._get_tile(coord[0], coord[1])
        num = int(num_in_str)
        return num ** 2
    else:
        return 1


def ucost(gameboard, is_weight):
    """solve the Game with Uniform Cost Search
    print:
        steps and states of solution
        Total path cost of solution
        Total number of states added to the frontier queue
        Total number of states popped from the frontier queue and expanded
    :param gameboard: string, string that describe the gameboard
    :param is_weight: boolean,
                      True: weighted
                      False: noweight (transition cost = 1)
    :return: void
    """
    # TODO:
    # create initial state:
    init = puzz.EightPuzzleBoard(gameboard)
    # create frontier (priority) queue and add initial state with priority 0
    frontier = pdqpq.PriorityQueue()
    frontier.add(init, 0)
    # set operation to initial state
    init.op = 'start'
    # num_front/num_explored record number of states added/popped to/out the frontier
    num_front = 1
    num_explored = 0
    # create explored list
    explored = set()

    while not frontier.empty():
        # if we have expanded 100000 nodes, print 'search halted' and exit
        if num_explored >= 100000:
            print("search halted")
            return 0

        # pop a state from frontier
        state = frontier.pop()
        if eight_puzzle_is_goal(state):
            # get the path
            solution = traceback(state)
            # set step to 0
            step = 0
            for sol in solution:
                print(step, '\t', sol.op, '\t', sol)
                step += 1
            print("path cost: %d" % state.cost)
            print("frontier: %d" % num_front)
            print("expanded: %d" % num_explored)
            tup = (state.cost, num_front, num_explored)
            return tup
        # add it to the explored set
        explored.add(state)
        # update num_explored
        num_explored += 1
        # zero_coord: record the coordinate of '0' in the state:
        zero_coord = state.find('0')

        # k is the keyword we get from successors
        for k in state.successors():
            # next_state: the next possible state if we expand current state:
            next_state = state.successors()[k]
            # set operation and predecessor of next_state:
            next_state.op = k
            next_state.predecessor = state
            # record the total cost so far of next_state
            # TODO: change the cost function for further use
            cost_with_k = ucost_cost(next_state, zero_coord, is_weight)
            next_state.cost = state.cost + cost_with_k

            if (next_state not in frontier) and (next_state not in explored):
                frontier.add(next_state, next_state.cost)
                num_front += 1
            elif (next_state in frontier) and (frontier.get(next_state) > next_state.cost):
                frontier.add(next_state, next_state.cost)

    # if no solution found, print "failure"
    print("failure")
    return 0


def heuristic_eight_puzzle(state):
    """return the heuristics with given state and coordinate

    :param state: EightPuzzleBoard, the current state
    :param coord: tuple, coordinate of move that take place
    :return: int
    """
    goal = puzz.EightPuzzleBoard("012345678")
    heuristic = 0
    for i in range(9):
        coord = state.find(str(i))
        target = goal.find(str(i))
        manhattan_x = abs(coord[0] - target[0])
        manhattan_y = abs(coord[1] - target[1])
        heuristic += (i ** 2) * (manhattan_x + manhattan_y)
    return heuristic


def greedy(gameboard, is_weight):
    # TODO
    """solve the Game with Breath-First-Search
        print:
            steps and states of solution
            Total path cost of solution
            Total number of states added to the frontier queue
            Total number of states popped from the frontier queue and expanded
        :param gameboard: string, string that describe the gameboard
        :return: void
        """
    # TODO:
    # create initial state:
    init = puzz.EightPuzzleBoard(gameboard)
    # create frontier (priority) queue and add initial state with its priority 0
    frontier = pdqpq.PriorityQueue()
    frontier.add(init, 0)
    # set operation to initial state
    init.op = 'start'
    # num_front/num_explored record number of states added/popped to/out the frontier
    num_front = 1
    num_explored = 0
    # create explored list
    explored = set()

    while not frontier.empty():
        # if we have expanded 100000 nodes, print 'search halted' and exit
        if num_explored >= 100000:
            print("search halted")
            return 0

        # pop a state from frontier
        state = frontier.pop()
        if eight_puzzle_is_goal(state):
            # get the path
            solution = traceback(state)
            # set step to 0
            step = 0
            for sol in solution:
                print(step, '\t', sol.op, '\t', sol)
                step += 1
            print("path cost: %d" % state.cost)
            print("frontier: %d" % num_front)
            print("expanded: %d" % num_explored)
            tup = (state.cost, num_front, num_explored)
            return tup
        # add it to the explored set
        explored.add(state)
        # update num_explored
        num_explored += 1
        # zero_coord: record the coordinate of '0' in the state:
        zero_coord = state.find('0')

        # k is the keyword we get from successors
        for k in state.successors():
            # next_state: the next possible state if we expand current state:
            next_state = state.successors()[k]
            # set operation and predecessor of next_state:
            next_state.op = k
            next_state.predecessor = state
            # record the total cost so far of next_state
            # TODO: change the cost function for further use
            cost_with_k = ucost_cost(next_state, zero_coord, is_weight)
            # path cost (only used to record path cost)
            next_state.cost = state.cost + cost_with_k
            # heuristic
            heuristic = heuristic_eight_puzzle(next_state)

            if (next_state not in frontier) and (next_state not in explored):
                frontier.add(next_state, heuristic)
                num_front += 1
            elif (next_state in frontier) and (frontier.get(next_state) > heuristic):
                frontier.add(next_state, heuristic)

    # if no solution found, print "failure"
    print("failure")
    return 0


def astar(gameboard, is_weight):
    # TODO
    """solve the Game with astar
        print:
            steps and states of solution
            Total path cost of solution
            Total number of states added to the frontier queue
            Total number of states popped from the frontier queue and expanded
        :param gameboard: string, string that describe the gameboard
        :param is_weight: boolean,
                    True: weighted
                    False: noweight (transition cost = 1)
        :return: void
        """
    # TODO:
    # create initial state:
    init = puzz.EightPuzzleBoard(gameboard)
    # create frontier (priority) queue and add initial state with its priority 0
    frontier = pdqpq.PriorityQueue()
    frontier.add(init, 0)
    # set operation to initial state
    init.op = 'start'
    # num_front/num_explored record number of states added/popped to/out the frontier
    num_front = 1
    num_explored = 0
    # create explored list
    explored = set()

    while not frontier.empty():
        # if we have expanded 100000 nodes, print 'search halted' and exit
        if num_explored >= 100000:
            print("search halted")
            return 0

        # pop a state from frontier
        state = frontier.pop()
        if eight_puzzle_is_goal(state):
            # get the path
            solution = traceback(state)
            # set step to 0
            step = 0
            for sol in solution:
                print(step, '\t', sol.op, '\t', sol)
                # print(step, sol.op, sol, sep='\t')
                step += 1
            print("path cost: %d" % state.cost)
            print("frontier: %d" % num_front)
            print("expanded: %d" % num_explored)
            tup = (state.cost, num_front, num_explored)
            return tup
        # add it to the explored set
        explored.add(state)
        # update num_explored
        num_explored += 1
        # zero_coord: record the coordinate of '0' in the state:
        zero_coord = state.find('0')

        # k is the keyword we get from successors
        for k in state.successors():
            # next_state: the next possible state if we expand current state:
            next_state = state.successors()[k]
            # set operation and predecessor of next_state:
            next_state.op = k
            next_state.predecessor = state
            # record the total cost so far of next_state
            # TODO: change the cost function for further use
            cost_with_k = ucost_cost(next_state, zero_coord, is_weight)
            # path cost
            next_state.cost = state.cost + cost_with_k
            # heuristic
            heuristic = heuristic_eight_puzzle(next_state)
            # total = path cast + heuristic
            total = next_state.cost + heuristic

            if (next_state not in frontier) and (next_state not in explored):
                frontier.add(next_state, total)
                num_front += 1
            elif (next_state in frontier) and (frontier.get(next_state) > total):
                frontier.add(next_state, total)

    # if no solution found, print "failure"
    print("failure")
    return 0


# def graph():
#     game_boards = creat_situations()
#     n = len(game_boards)
#     sum_bfs_cost = 0
#     sum_ucost_cost = 0
#     sum_greedy_cost = 0
#     sum_astar_cost = 0
#
#     sum_bfs_frontier = 0
#     sum_ucost_frontier = 0
#     sum_greedy_frontier = 0
#     sum_astar_frontier = 0
#
#     sum_bfs_expanded = 0
#     sum_ucost_expanded = 0
#     sum_greedy_expanded = 0
#     sum_astar_expanded = 0
#
#     for gb in game_boards:
#         tup_bfs = bfs(gb)
#         tup_ucost = ucost(gb, True)
#         tup_greedy = greedy(gb)
#         tup_astar = astar(gb, True)
#
#         sum_bfs_cost += tup_bfs[0]
#         sum_ucost_cost += tup_ucost[0]
#         sum_greedy_cost += tup_greedy[0]
#         sum_astar_cost += tup_astar[0]
#
#         sum_bfs_frontier += tup_bfs[1]
#         sum_ucost_frontier += tup_ucost[1]
#         sum_greedy_frontier += tup_greedy[1]
#         sum_astar_frontier += tup_astar[1]
#
#         sum_bfs_expanded += tup_bfs[2]
#         sum_ucost_expanded += tup_ucost[2]
#         sum_greedy_expanded += tup_greedy[2]
#         sum_astar_expanded += tup_astar[2]
#
#     mean_bfs_cost = sum_bfs_cost / n
#     mean_ucost_cost = sum_ucost_cost / n
#     mean_greedy_cost = sum_greedy_cost / n
#     mean_astar_cost = sum_astar_cost / n
#
#     mean_bfs_frontier = sum_bfs_frontier / n
#     mean_ucost_frontier = sum_ucost_frontier / n
#     mean_greedy_frontier = sum_greedy_frontier / n
#     mean_astar_frontier = sum_astar_frontier / n
#
#     mean_bfs_expanded = sum_bfs_expanded / n
#     mean_ucost_expanded = sum_ucost_expanded / n
#     mean_greedy_expanded = sum_greedy_expanded / n
#     mean_astar_expanded = sum_astar_expanded / n
#
#     x = ["BFS", "UCS", "Greedy", "A*"]
#     cost_list = [mean_ucost_cost, mean_ucost_cost, mean_greedy_cost, mean_astar_cost]
#     frontier_list = [mean_bfs_frontier, mean_ucost_frontier, mean_greedy_frontier, mean_astar_frontier]
#     expanded_list = [mean_bfs_expanded, mean_ucost_expanded, mean_greedy_expanded, mean_astar_expanded]
#
#     plt.bar(x, cost_list)
#     plt.xlabel("Search Strategy")
#     plt.ylabel("Count")
#     plt.title("Average Path Cost")
#     plt.savefig("cost.pdf")
#     plt.show()
#
#     plt.bar(x, frontier_list)
#     plt.xlabel("Search Strategy")
#     plt.ylabel("Count")
#     plt.title("Average Number of States Added to Frontier")
#     plt.savefig("front.pdf")
#     plt.show()
#
#     plt.bar(x, expanded_list)
#     plt.xlabel("Search Strategy")
#     plt.ylabel("Count")
#     plt.title("Average Number of States Expanded")
#     plt.savefig("expand.pdf")
#     plt.show()


def main(argv):
    if len(argv) == 2:
        if argv[0] == "bfs":
            bfs(argv[1], True)
        elif argv[0] == "ucost":
            ucost(argv[1], True)
        elif argv[0] == "greedy":
            greedy(argv[1], True)
        elif argv[0] == "astar":
            astar(argv[1], True)
        else:
            print("Invalid input for function name")
    elif len(argv) == 3:
        if argv[0] == "bfs":
            bfs(argv[1], True)
        elif argv[0] == "ucost":
            ucost(argv[1], False)
        elif argv[0] == "greedy":
            greedy(argv[1], False)
        elif argv[0] == "astar":
            astar(argv[1], False)
        else:
            print("Invalid input for function name")
    else:
        print("Please write the right format: ")
        print("function name: string, 8 puzzle game board: 9-digit numbers, noweight: string")


# def main():
#     sample = "312458607"
#     sample2 = "802356174"
#     init = "012345678"
#     # bfs(init)
#     # ucost("307451628", True)
#     # greedy("307451628")
#     # astar("307451628", True)
#     # graph()


if __name__ == '__main__':
    # main()
    main(sys.argv[1:])
