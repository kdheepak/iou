
# coding: utf-8

# In[124]:

from coopr.pyomo import *


# In[125]:

lenders = sorted([key for key, value in net_value.items() if value < 0])


# In[126]:

loaners = sorted([key for key, value in net_value.items() if value >= 0])


# In[127]:

loaners


# In[128]:

lenders


# In[144]:

model = ConcreteModel()

model.Loaners = RangeSet(1, len(loaners))
model.Lenders = RangeSet(1, len(lenders))

model.Amount = Var(model.Loaners, model.Lenders, domain=NonNegativeReals)
model.TransactionsSwitch = Var(model.Loaners, model.Lenders, domain=Boolean)

def obj_expression(model):
    return sum(model.Amount[i,j] for i in model.Loaners for j in model.Lenders)

model.OBJ = Objective(rule=obj_expression)

def loaner_constraint_rule(model, i):
    return sum(model.Amount[i,j] for j in model.Lenders) == net_value[loaners[i-1]]

def lender_constraint_rule(model, j):
    return sum(model.Amount[i,j] for i in model.Loaners) == -net_value[lenders[j-1]]

# def max_lenders_constraint_rule(model, i, j):
#     return model.Amount[i, j] <= net_value[lenders[j-1]]

# def max_loaners_constraint_rule(model, i, j):
#     return model.Amount[i, j] <= net_value[loaners[i-1]]
                   
model.AmountConstraintLoaner = Constraint(model.Loaners, rule=loaner_constraint_rule)
model.AmountConstraintLender = Constraint(model.Lenders, rule=lender_constraint_rule)

# model.Constraint_1 = Constraint(expr=model.Amount[1,1]+model.Amount[1,2]==25.0)
# model.Constraint_2 = Constraint(expr=model.Amount[2,1]+model.Amount[2,2]==50.0)
# model.Constraint_3 = Constraint(expr=model.Amount[1,1]+model.Amount[2,1]==60.0)


# In[145]:

model.pprint()


# In[146]:

import coopr.environ
from coopr.opt.base import SolverFactory


# In[147]:

opt = SolverFactory('cplex')
 
# create model instance, solve
instance = model.create()
results = opt.solve(instance)
instance.load(results) #load results back into model framework
 
## REPORT ##
print("status=" + str(results.Solution.Status))
print("solution=" + str(results.Solution.Objective) + "\n")


# In[160]:

for i in range(0, len(loaners)):
    for j in range(0, len(lenders)):
        if(instance.Amount[i+1, j+1].value != 0.0):
            print("{} pays {} a total of ${:.2f}".format(loaners[i], lenders[j], (instance.Amount[i+1, j+1].value)))


# In[ ]:



