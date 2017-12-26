from math import log



#Split a set into two smaller attribute on the value
def splitOnAttribute(rows, column, value):
    bigger = [row for row in rows if row[column] >= value]  # if split_function(row)
    less = [row for row in rows if not row[column] >= value]
    return (bigger, less)


#Count how many unique elements exists in rows
def uniqueElements(rows):
    results = {}
    for row in rows:
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


#Calculates the entropy for the rows rows
def calcEntropy(rows):
    log2 = lambda x: log(x) / log(2)
    results = uniqueElements(rows)
    # Now calculate the calcEntropy()
    ent = 0.0
    for r in results.keys():
        # current probability of class
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent



#A simple class defining a node in a tree and its values
class node:
    def __init__(self, attribute=-1, thresHold=None, results=None, trueLeaf=None, falseLeaf=None):
        self.attribute = attribute  #The attribute being tested. Represents the column number from the input
        self.thresHold = thresHold  #The threshold
        self.results = results  #The result for an endpoint
        self.trueLeaf = trueLeaf  #true decision leaf
        self.falseLeaf = falseLeaf  #false decision leaf

#Builds a decision tree based upon the rows inputed
def buildtree(rows):
    if len(rows) == 0: return node()
    #Calculate the entropy on the current set
    currentEntropy = calcEntropy(rows)


    bestGain = 0.0
    bestSplit = None
    bestSubset = None

    #Don't want the last target attribute
    nbrofCols = len(rows[0]) - 1


    #Iterate thourgh every attribute to find the best attribute and value to split on
    for col in range(0, nbrofCols):

        #Get the unique values in an attribute
        columSet = sorted(set([row[col] for row in rows]))

        #Sort them
        column_values = [float(x) for x in columSet]

        for i in range(1, len(column_values)):
            #Selecting the threshold
            value = (column_values[i] - column_values[i-1]) /2 + column_values[i-1]

            #Try to split the current set on the the current attribute on the value value
            bigger, less = splitOnAttribute(rows, col, value)

            #Calculate the information gain
            p = float(len(bigger)) / len(rows)
            gain = currentEntropy - p * calcEntropy(bigger) - (1 - p) * calcEntropy(less)

            #If the calculated gain is the best so far, save it, the attribute and the value
            if gain > bestGain and len(bigger) > 0 and len(less) > 0:
                bestGain = gain
                bestSplit = (col, value)
                bestSubset = (bigger, less)
    #If gain is bigger than zero, then we build a new subtree from the subsets that gave the biggest information gain
    if bestGain > 0:
        trueBranch = buildtree(bestSubset[0])
        falseBranch = buildtree(bestSubset[1])
        return node(attribute=bestSplit[0], thresHold=bestSplit[1],
                            trueLeaf=trueBranch, falseLeaf=falseBranch)
    #If the information was 0, we cannot split anymore, so return a result node.
    else:
        return node(results=uniqueElements(rows))




#Parse a training file
def parse(name='horseTrain.txt'):
    with open(name) as f:
        lines = f.readlines()
        data = []
        index = 0
        for line in lines:
            line = line.strip('\n')
            test = line.split(',')
            last = test[16]
            del test[-1]
            data.append([float(x) for x in test])
            data[index].append(last)
            index = index +1

    return data


#Parse a test set, i.e exclude the target attribute
def parseTest(name='horseTest.txt'):
    with open(name) as f:
        lines = f.readlines()
        data = []
        for line in lines:
            line = line.strip('\n')
            test = line.split(',')
            del test[-1]
            data.append([float(x) for x in test])

    return data

#Tests a data set on a constructed tree. Returns the result
def testTree(row, tree):
        if tree.attribute is -1:
            return tree.results
        if row[tree.attribute] > tree.thresHold:
            return testTree(row, tree.trueLeaf)
        else:
            return testTree(row, tree.falseLeaf)




data = parse()

tree = buildtree(data)


test = parseTest()
testCompare = parse(name="horseTest.txt")

print("The results for testing of the tree from the horseTest.txt. Left hand side is what the file says the diagnosis is, the left hand is what the tree says")
for i in range(0, len(test)):
    if testCompare[i][16] in testTree(test[i], tree):
        print(testCompare[i][16], testTree(test[i], tree))
    else:
        print("false")



print("\n\n\n\n")

print("What the tree says about the test data")

test = parseTest(name="horseTrain.txt")
#Test a file and print the results together with the actual  result in the file
for i in range(0, len(test)):
    if data[i][16] in testTree(test[i], tree):
        print(data[i][16], testTree(test[i], tree))
    else:
        print("false")
