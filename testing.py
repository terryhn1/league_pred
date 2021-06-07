import factors
import numpy as np
import pyGMs as gm


def testConditions(model, valid, vars, pos):
    reset = model
    for xj in valid:
        conditions = {model.X[0]: xj[0], model.X[1]: xj[1], model.X[2]: xj[2], model.X[3]: xj[3]
                    , model.X[4]: xj[4], model.X[5]: xj[5], model.X[6]: xj[6], model.X[7]: xj[7]
                    , model.X[8]: xj[8], model.X[9]: xj[9]}
        model.condition(conditions)
        model.drawMarkovGraph(var_labels = vars, pos= pos)
        return 
    pass


if __name__ == "__main__":
    model, factor_list = factors.initializeGraphModel()
    model, valid = factors.loadData(model, factor_list)
    testConditions(model,valid)