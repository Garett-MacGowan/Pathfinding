import heapq
import copy

def main():
    # pathProblems are in the form [[grid],[grid],...]
    # where each grid is in the form grid[row][column]
    # pathStartEnd are in the form [[(row, column),(row, column)],[(),()],...
    # where the first tuple represents the start state and the second represents the goal state
    pathProblemsA, pathStartEndA, pathProblemsB, pathStartEndB = gridRead()
    pathSolutionsA = solutionHandler(pathProblemsA, pathStartEndA, "A")
    pathSolutionsB = solutionHandler(pathProblemsB, pathStartEndB, "B")

    writeSolutions("pathfinding_a_out.txt", pathSolutionsA)
    writeSolutions("pathfinding_b_out.txt", pathSolutionsB)

def gridRead():
    pathProblemsA = []
    pathStartEndA = [[None, None]]
    pathProblemsB = []
    pathStartEndB = [[None, None]]
    try:
        fileA = open("pathfinding_a.txt", 'r')
        fileB = open("pathfinding_b.txt", 'r')
    except IOError:
        print("Cannot open one of the input files!")
    else:
        for line in fileA:
            currentLine = line.strip('\n')
            if len(pathProblemsA) == 0:
                pathProblemsA.append([])
            if currentLine == "":
                pathProblemsA.append([])
                continue
            pathProblemsA[-1].append([])
            for index in range(len(currentLine)):
                pathProblemsA[-1][-1].append(currentLine[index])
                if currentLine[index] == "S":
                    if pathStartEndA[-1][0] == None:
                        pathStartEndA[-1][0] = (len(pathProblemsA[-1]) - 1, index)
                    elif pathStartEndA[-1][0] != None and pathStartEndA[-1][1] != None:
                        pathStartEndA.append([(len(pathProblemsA[-1]) - 1, index), None])
                if currentLine[index] == "G":
                    if pathStartEndA[-1][1] == None:
                        pathStartEndA[-1][1] = (len(pathProblemsA[-1]) - 1, index)
                    elif pathStartEndA[-1][0] != None and pathStartEndA[-1][1] != None:
                        pathStartEndA.append([None, (len(pathProblemsA[-1]) - 1, index)])
        fileA.close()
        for line in fileB:
            currentLine = line.strip('\n')
            if len(pathProblemsB) == 0:
                pathProblemsB.append([])
            if currentLine == "":
                pathProblemsB.append([])
                continue
            pathProblemsB[-1].append([])
            for index in range(len(currentLine)):
                pathProblemsB[-1][-1].append(currentLine[index])
                if currentLine[index] == "S":
                    if pathStartEndB[-1][0] == None:
                        pathStartEndB[-1][0] = (len(pathProblemsB[-1]) - 1, index)
                    elif pathStartEndB[-1][0] != None and pathStartEndB[-1][1] != None:
                        pathStartEndB.append([(len(pathProblemsB[-1]) - 1, index), None])
                if currentLine[index] == "G":
                    if pathStartEndB[-1][1] == None:
                        pathStartEndB[-1][1] = (len(pathProblemsB[-1]) - 1, index)
                    elif pathStartEndB[-1][0] != None and pathStartEndB[-1][1] != None:
                        pathStartEndB.append([None, (len(pathProblemsB[-1]) - 1, index)])
        fileB.close()
    return pathProblemsA, pathStartEndA, pathProblemsB, pathStartEndB

def retrieveNeighbors(node, grid, pType):
    # Neighbors take the form [(row, column),(row, column),...]
    neighbors = []
    row = int(node[0])
    column = int(node[1])
    # Note, problem type A means that valid movements are only up, down, left, and right.
    if pType == "A":
        if column - 1 >= 0 and grid[row][column - 1] != "X":
            neighbors.append((row, column - 1))
        if row - 1 >= 0 and grid[row - 1][column] != "X":
            neighbors.append((row - 1, column))
        if column + 1 <= len(grid[row]) - 1 and grid[row][column + 1] != "X":
            neighbors.append((row, column + 1))
        if row + 1 <= len(grid) - 1 and grid[row + 1][column] != "X":
            neighbors.append((row + 1, column))
    # Problem type B means that valid movements are up, down, left, right, and diagonal.
    else:
        if column - 1 >= 0 and grid[row][column - 1] != "X":
            neighbors.append((row, column - 1))
        if row - 1 >= 0 and grid[row - 1][column] != "X":
            neighbors.append((row - 1, column))
        if column + 1 <= len(grid[row]) - 1 and grid[row][column + 1] != "X":
            neighbors.append((row, column + 1))
        if row + 1 <= len(grid) - 1 and grid[row + 1][column] != "X":
            neighbors.append((row + 1, column))
        if row - 1 >= 0 and column - 1 >= 0 and grid[row - 1][column - 1] != "X":
            neighbors.append((row - 1, column - 1))
        if row - 1 >= 0 and column + 1 <= len(grid[row]) - 1 and grid[row - 1][column + 1] != "X":
            neighbors.append((row - 1, column + 1))
        if row + 1 <= len(grid) - 1 and column + 1 <= len(grid[row]) - 1 and grid[row + 1][column + 1] != "X":
            neighbors.append((row + 1, column + 1))
        if row + 1 <= len(grid) - 1 and column - 1 >= 0 and grid[row + 1][column - 1] != "X":
            neighbors.append((row + 1, column - 1))
    return neighbors

def greedy(grid, pathStartEnd, pType):
    pathStart = pathStartEnd[0]
    target = pathStartEnd[1]
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, pathStart))
    cameFrom = {}
    cameFrom[pathStart] = None

    while len(priorityQueue) != 0:
        current = heapq.heappop(priorityQueue)
        if current[1] == target:
            break
        neighbors = retrieveNeighbors(current[1], grid, pType)
        while len(neighbors) != 0:
            if neighbors[-1] not in cameFrom:
                if pType == "A":
                    priority = mannHeuristic(neighbors[-1], target)
                else:
                    priority = chebHeuristic(neighbors[-1], target)
                heapq.heappush(priorityQueue, (priority, neighbors[-1]))
                cameFrom[neighbors[-1]] = current
            del neighbors[-1]

    # Traverse the cameFrom dictionary in order to build the path that was found
    solution = []
    if cameFrom[current[1]] != None:
        nextNode = cameFrom[current[1]]
    else:
        return solution
    while cameFrom[nextNode[1]] != None:
        solution.append(nextNode[1])
        nextNode = cameFrom[nextNode[1]]
    return solution

def aStar(grid, pathStartEnd, pType):
    pathStart = pathStartEnd[0]
    target = pathStartEnd[1]
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, pathStart))
    cameFrom = {}
    cameFrom[pathStart] = None
    costSoFar = {}
    costSoFar[pathStart] = 0

    while len(priorityQueue) != 0:
        current = heapq.heappop(priorityQueue)
        if current[1] == target:
            break
        neighbors = retrieveNeighbors(current[1], grid, pType)
        while len(neighbors) != 0:
            newCost = costSoFar[current[1]] + 1
            if neighbors[-1] not in costSoFar or newCost < costSoFar[neighbors[-1]]:
                costSoFar[neighbors[-1]] = newCost
                if pType == "A":
                    priority = newCost + mannHeuristic(neighbors[-1], target)
                else:
                    priority = newCost + chebHeuristic(neighbors[-1], target)
                heapq.heappush(priorityQueue, (priority, neighbors[-1]))
                cameFrom[neighbors[-1]] = current
            del neighbors[-1]

    # Traverse the cameFrom dictionary in order to build the path that was found
    solution = []
    if cameFrom[current[1]] != None:
        nextNode = cameFrom[current[1]]
    else:
        return solution
    while cameFrom[nextNode[1]] != None:
        solution.append(nextNode[1])
        nextNode = cameFrom[nextNode[1]]
    return solution

def mannHeuristic(node, target):
    return abs(target[0] - node[0]) + abs(target[1] - node[1])

def chebHeuristic(node, target):
    return max(abs(target[0] - node[0]), abs(target[1] - node[1]))

def drawSolutionPath(solution, grid):
    for item in solution:
        grid[item[0]][item[1]] = "P"
    return grid

def solutionHandler(pathProblems, pathStartEnd, pType):
    # pathSolutions are in the form [[(board, algorithm), (board, alg), ...], [another problem], ...]
    # This is so that the grids can be updated to reflect the solution cleanly.
    pathSolutions = []
    currentProblem = []
    for index in range(len(pathProblems)):
        greedyPathProblem = copy.deepcopy(pathProblems[index])
        aStarPathProblem = copy.deepcopy(pathProblems[index])

        currentSolution = greedy(greedyPathProblem, pathStartEnd[index], pType)
        currentProblem.append((drawSolutionPath(currentSolution, greedyPathProblem), "Greedy"))

        currentSolution = aStar(aStarPathProblem, pathStartEnd[index], pType)
        currentProblem.append((drawSolutionPath(currentSolution, aStarPathProblem), "A*"))

        pathSolutions.append(currentProblem)
        currentProblem = []
    return pathSolutions

def writeSolutions(fileName, pathSolutions):
    try:
        file = open(fileName, 'w')
    except IOError:
        print("Cannot open " + fileName)
    else:
        for board in pathSolutions:
            for item in board:
                file.write(str(item[1]) + '\n')
                for i in range(len(item[0])):
                    row = ''.join(item[0][i])
                    file.write(row + '\n')
            file.write('\n')
    file.close()

def visualizer(grid):
    for row in grid:
        print(row)
    print()

main()
