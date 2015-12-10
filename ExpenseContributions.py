
# coding: utf-8

# In[1]:

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

user_name

# In[2]:

### Get worksheet from drive.google.com


# In[3]:

json_key = json.load(open("/Users/"+user_name+"/Desktop/API Project-f746ec1d42cd.json"))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)


# In[4]:

### Create network of debt


# In[5]:

import networkx as nx


# In[6]:

G = nx.MultiDiGraph()


# In[7]:

expense_sheet_name = ""

worksheet = gc.open(expense_sheet_name).sheet1

### Find list of people involved
values_list = worksheet.row_values(1)
people = values_list[3:]

for person_name in people:
    if person_name is None:
        pass
    else:
        G.add_node(person_name)
        


# In[8]:

print(people)


# In[9]:

print(G.nodes())


# In[10]:

for row_number in range(2, 21):
    row = worksheet.row_values(row_number)
    number_of_contributors = sum([float(item) for item in row[3:]])
    for i, item in enumerate(row[3:]):
        if item != '0':
            G.add_edge(people[i], row[2], owe=float(item)*float(row[1].strip('$'))/number_of_contributors)
    print("{number_of_contributors} people owe {person} {amount} for {expense}".format(
            number_of_contributors=number_of_contributors, 
            person=row[2],
            expense=row[0],
            amount=row[1])
         )


# In[11]:

### combine multiple edges to find net value


# In[12]:

### empty dictionary
net_value = {}
for node in G.nodes():
    net_value[node] = 0


# In[13]:

for edge in G.edges(data=True):
    net_value[edge[0]] -= edge[2]['owe']
    net_value[edge[1]] += edge[2]['owe']


# In[14]:

for person, value in net_value.items():
    if value > 0:
        print("{person}'s net spend \t{value}".format(person=person, value=-1*value))
    if value < 0:
        print("{person}'s net spend \t {value}".format(person=person, value=-1*value))


# In[15]:

print(net_value)

# TODO Invert signs of net_value


