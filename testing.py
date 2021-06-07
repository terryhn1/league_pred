from numpy.core.fromnumeric import var
import factors
import copy


def testConditions(model, valid, vars, pos):
    reset = copy.deepcopy(model)
    limit = 10
    iter = 0
    for xj in valid:
        conditions = {model.X[0]: xj[0], model.X[1]: xj[1], model.X[2]: xj[2], model.X[3]: xj[3]
                    , model.X[4]: xj[4], model.X[5]: xj[5], model.X[6]: xj[6], model.X[7]: xj[7]
                    , model.X[8]: xj[8], model.X[9]: xj[9]}
        model.condition(conditions)
        model.drawMarkovGraph(var_labels = vars,pos = pos)
        sumElim = lambda F, Xlist: F.sum(Xlist)

        #Calculates the probability of win condition based on the evidence seen
        model.eliminate(model.X[:-1], sumElim)
        print(model.factors[-1].table/ model.factors[-1].table.sum())
        #Reset the original model and the reset variable for every iteration
        model = reset
        reset = copy.deepcopy(model)

        if iter == limit:
            break
        else:
            iter += 1
    
    return


if __name__ == "__main__":
    model, factor_list = factors.initializeGraphModel()
    
    model, valid = factors.loadData(model, factor_list)
    var_labels = {0: "jungle", 1: "turrets", 2: "cs", 3: "ward", 4: "elite", 5: "gold", 6: "exp", 7: "kda", 8: "lane", 9: "teamplay", 10: "win"}
    pos = {model.X[0]: (0,3), model.X[1]:(1,3), model.X[2]:(2,3), model.X[3]:(3,3), 
       model.X[4]:(4,3), model.X[5]:(1,2), model.X[6]:(2,2), model.X[7]:(3,2), 
       model.X[8]:(1,1), model.X[9]:(2,1), model.X[10]:(2,0)}
    testConditions(model, valid, var_labels, pos)
    