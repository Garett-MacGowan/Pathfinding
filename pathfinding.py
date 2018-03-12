def main():
    # pathProblems are in the form [[grid],[grid],[grid],...]
    # where each grid is in the form grid[row][column]
    pathProblemsA, pathStartEndA, pathProblemsB, pathStartEndB = gridRead()
    pathSolutionsA = solutionHandler(pathProblemsA, pathStartEndA, "A")
    #pathSolutionsB = solutionHandler(pathProblemsB, pathStartEndB, "B")
    # writeSolutions("pathfinding_a_out.txt", pathSolutionsA)
    # writeSolutions("pathfinding_b_out.txt", pathSolutionsB)

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

def solutionHandler(pathProblems, pathStartEnd, pType):
    visualizer(pathProblems[0])
    visualizer(pathProblems[1])
    print(pathStartEnd)

'''
def writeSolutions(fileName, pathProblems):
    try:
        file = open(fileName, 'a')
    except IOError:
        print("Cannot open " + fileName)
    else:
'''

def cleanFiles(fileName):
    try:
        f = open(fileName, 'w')
    except IOError:
        print("Cannot open " + fileName)
    else:
        f.close()

def visualizer(grid):
    for row in grid:
        print(row)
    print()

main()
