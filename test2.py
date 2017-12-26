class decisionnode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col  # column index of criteria being tested
        self.value = value  # vlaue necessary to get a true result
        self.results = results  # dict of results for a branch, None for everything except endpoints
        self.tb = tb  # true decision nodes
        self.fb = fb  # false decision nodes


def divideset(rows, column, value):
    # Make a function that tells us if a row is in the first group
    # (true) or the second group (false)
    split_function = None
    # for numerical values
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    # for nominal values
    else:
        split_function = lambda row: row[column] == value

        # Divide the rows into two sets and return them
    set1 = [row for row in rows if split_function(row)]  # if split_function(row)
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


def uniquecounts(rows):
    results = {}
    for row in rows:
        # The result is the last column
        r = row[len(row) - 1]
        if r not in results: results[r] = 0
        results[r] += 1
    return results


def entropy(rows):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    # Now calculate the entropy
    ent = 0.0
    for r in results.keys():
        # current probability of class
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent


def buildtree(rows):
    if len(rows) == 0: return decisionnode()




    """
    Returns a new decision tree based on the examples given.
    """
    data    = data[:]
    vals    = [record[16] for record in data]
    default = mode(data)

    # If the dataset is empty or the attributes list is empty, return the
    # default value. When checking the attributes list for emptiness, we
    # need to subtract 1 to account for the target attribute.
    if not data or (len(attributes) - 1) <= 0:
        return default
    # If all the records in the dataset have the same classification,
    # return that classification.
    elif vals.count(vals[0]) == len(vals):
        return vals[0]



    current_score = entropy(rows)

    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1  # last column is result
    for col in range(0, column_count):
        colum_t = sorted(set([row[col] for row in rows]))

        column_values = [float(x) for x in colum_t]

        # for each possible value, try to divide on that value
        for i in range(1, len(column_values)):
            value = (column_values[i] - column_values[i - 1]) / 2 + column_values[i - 1]
            # print(value)
            set1, set2 = divideset(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p * entropy(set1) - (1 - p) * entropy(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))


def printtree(tree,indent=''):
    # Is this a leaf node?
    if tree.results!=None:
        print (str(tree.results))
    else:
        # Print the criteria
        print('Column ' + str(tree.col)+' : '+str(tree.value)+'? ')

        # Print the branches
        print(indent+'True->', end=" ")
        print(printtree(tree.tb,indent+'  '))
        print(indent+'False->', end=' ')
        print(printtree(tree.fb,indent+'  '))

def parse():
    with open('horseTrain.txt') as f:
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
            index = index + 1

    return data



data = parse()
tree = buildtree(data)
print(tree.tb.col)