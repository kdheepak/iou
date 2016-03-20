from pyomo.environ import SolverFactory, Objective, ConcreteModel, Var, NonNegativeReals, Constraint, maximize, Set


def create_model(net_value):

    lenders = sorted([key for key, value in net_value.items() if value < 0])
    loaners = sorted([key for key, value in net_value.items() if value >= 0])

    model = ConcreteModel()

    model.Loaners = Set(initialize=loaners)
    model.Lenders = Set(initialize=lenders)

    model.Amount = Var(model.Loaners, model.Lenders, domain=NonNegativeReals)

    def obj_expression(model):
        return sum(model.Amount[i, j] * model.Amount[i, j]
                   for i in model.Loaners for j in model.Lenders)

    model.OBJ = Objective(rule=obj_expression, sense=maximize)

    def loaner_constraint_rule(model, i):
        return sum(model.Amount[i, j]
                   for j in model.Lenders) <= net_value[i]

    def lender_constraint_rule(model, j):
        return sum(model.Amount[i, j]
                   for i in model.Loaners) <= -net_value[j]

    model.AmountConstraintLoaner = Constraint(model.Loaners,
                                              rule=loaner_constraint_rule)
    model.AmountConstraintLender = Constraint(model.Lenders,
                                              rule=lender_constraint_rule)

    return model


def solve(model):

    opt = SolverFactory('ipopt')
    instance = model
    results = opt.solve(instance)
    instance.solutions.store_to(results)

    return results
