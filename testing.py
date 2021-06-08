from numpy.core.fromnumeric import var
import factors
import copy


def testConditions(model, valid):
    reset = copy.deepcopy(model)
    sumElim = lambda F, Xlist: F.sum(Xlist)
    limit = 10
    iter = 0
    accuracy = 0
    for xj in valid:
        conditions = {model.X[0]: xj[0], model.X[1]: xj[1], model.X[2]: xj[2], model.X[3]: xj[3]
                    , model.X[4]: xj[4], model.X[5]: xj[5], model.X[6]: xj[6], model.X[7]: xj[7]
                    , model.X[8]: xj[8], model.X[9]: xj[9]}
        model.condition(conditions)

        #Calculates the probability of win condition based on the evidence seen
        model.eliminate(model.X[:-1], sumElim)
        probs = list(enumerate(model.factors[-1].table/ model.factors[-1].table.sum()))
        winningPred = max(probs,key = lambda x: x[1])

        #If the winning prediction matches with the data
        if xj[10] == winningPred[0]:
            accuracy += 1

        #Reset the original model and the reset variable for every iteration
        model = reset
        reset = copy.deepcopy(model)
    
    return accuracy /len(valid)


if __name__ == "__main__":
    model, factor_list = factors.initializeGraphModel()
    
    model, valid = factors.loadData(model, factor_list)
    accuracy = testConditions(model, valid)
    print(accuracy)
    