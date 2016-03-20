"""
Minimize transactions between friends
"""
import json
import networkx as nx

from pyomo.environ import SolverFactory, Objective, ConcreteModel, RangeSet, Var, NonNegativeReals, Boolean, Constraint
from oauth2client.client import SignedJwtAssertionCredentials
import gspread


def sign_in_gspread():

    json_key = json.load(open(".iou"))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key[
                                                'private_key'].encode(), scope)

    gc = gspread.authorize(credentials)

    return gc


def create_graph(gc, expense_sheet_name):

    worksheet = gc.open(expense_sheet_name).sheet1

    # Find list of people involved
    values_list = worksheet.row_values(1)
    people = values_list[3:]

    G = nx.Graph()

    for person_name in people:
        if person_name is None:
            pass
        else:
            G.add_node(person_name)
    print(people)

    for row_number in range(2, 21):
        row = worksheet.row_values(row_number)
        number_of_contributors = sum([float(item) for item in row[3:]])
        for i, item in enumerate(row[3:]):
            if item != '0':
                G.add_edge(people[i], row[2], owe=float(
                    item) * float(row[1].strip('$')) / number_of_contributors)
        print("{number_of_contributors} people owe {person} {amount} for {expense}".format(
            number_of_contributors=number_of_contributors,
            person=row[2],
            expense=row[0],
            amount=row[1])
        )

    return G


def compress_edges(G):
    # empty dictionary
    net_value = {}
    for node in G.nodes():
        net_value[node] = 0

    for edge in G.edges(data=True):
        net_value[edge[0]] -= edge[2]['owe']
        net_value[edge[1]] += edge[2]['owe']

    for person, value in net_value.items():
        if value > 0:
            print("{person}'s net spend \t{value}".format(
                person=person, value=-1 * value))
        if value < 0:
            print("{person}'s net spend \t {value}".format(
                person=person, value=-1 * value))

    net_value = {key: -value for key, value in net_value.items()}

    return net_value


def find_optimal(net_value):

    lenders = sorted([key for key, value in net_value.items() if value < 0])
    loaners = sorted([key for key, value in net_value.items() if value >= 0])

    model = ConcreteModel()

    model.Loaners = RangeSet(1, len(loaners))
    model.Lenders = RangeSet(1, len(lenders))

    model.Amount = Var(model.Loaners, model.Lenders, domain=NonNegativeReals)
    model.TransactionsSwitch = Var(
        model.Loaners, model.Lenders, domain=Boolean)

    def obj_expression(model):
        return sum(model.Amount[i, j] * model.Amount[i, j] for i in model.Loaners for j in model.Lenders)

    model.OBJ = Objective(rule=obj_expression)

    def loaner_constraint_rule(model, i):
        return sum(model.Amount[i, j] for j in model.Lenders) <= net_value[loaners[i - 1]]

    def lender_constraint_rule(model, j):
        return sum(model.Amount[i, j] for i in model.Loaners) <= -net_value[lenders[j - 1]]

    model.AmountConstraintLoaner = Constraint(
        model.Loaners, rule=loaner_constraint_rule)
    model.AmountConstraintLender = Constraint(
        model.Lenders, rule=lender_constraint_rule)

    # model.pprint()

    opt = SolverFactory('ipopt')

    # create model instance, solve
    instance = model.create()
    results = opt.solve(instance)
    instance.load(results)  # load results back into model framework

    for i in range(0, len(loaners)):
        for j in range(0, len(lenders)):
            if(instance.Amount[i + 1, j + 1].value != 0.0):
                print("{} pays {} a total of ${:.2f}".format(
                    loaners[i], lenders[j], (instance.Amount[i + 1, j + 1].value)))
