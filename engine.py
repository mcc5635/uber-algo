import numpy as np
import pandas as pd
import cvxpy as cp




#############################
## Section 1: Introduction ##
##############################


rng = np.random.default_rng(42)
print(rng)

# rider count
num_riders = 1

# driver count
num_drivers = rng.poisson(lam=20)

# route driver to rider, rider to driver

# first, measure physical distance between riders and drivers
distances = pd.DataFrame(rng.uniform(0, 10, (num_riders, num_drivers)),
                         columns=[f'Driver {j}' for j in range(1, num_drivers+1)],
                         index=[f'Rider {i}' for i in range(1,num_riders+1)])

MDR = 5
maximum_dispatch_radius = (distances < MDR).apply(lambda x: np.where(x, 1, 0))
eta = distances.apply(lambda x: rng.pareto(x))
#print(eta)
#print(distances)
#print(maximum_dispatch_radius)

x = cp.Variable(len(eta.columns), integer = True)
time = np.array(eta).T
penalty = x @ time
objective = cp.Minimize(penalty)
compatible = np.array(maximum_dispatch_radius)
#print(compatible)

MDR = x @ compatible.T == 1

rider = x <= 1
driver = x >= 0

rider_driver = sum(x) == 1
prob = cp.Problem(objective, [MDR,rider,driver,rider_driver])
prob.solve()

#print(x.value)



####################################################################################
## Section 2: Batch Dispatch Protocol: Minimize the Aggregate En Route Time Model ##
####################################################################################

rng = np.random.default_rng(42)

num_riders = rng.poisson(lam=15)
num_drivers = rng.poisson(lam=15)

distances1 = pd.DataFrame(rng.uniform(0, 30, (num_riders, num_drivers)),
                         columns=[f'Driver {j}' for j in range(1, num_drivers+1)],
                         index=[f'Rider {i}' for i in range(1,num_riders+1)])

MDR = 5 # don't dispatch outside of MDR miles
MDR_1 = (distances1 <= MDR).apply(lambda x: np.where(x, 1, 0))

eta1 = distances1.apply(lambda x: rng.pareto(x)) 
# print(eta1)
# print(distances1)
# print(MDR_1)

# Minimize ETA: f(x) = x1eta+x2eta..x18*eta
num_drivers = len(eta1.values[0,:])
num_riders = len(eta1.values[:,0])

drivers = cp.Variable(eta1.shape, integer=True)

total_ETA = sum([eta1.values[i,j]*drivers[i,j] for i in range(eta1.shape[0])
  for j in range(eta1.shape[1])])

objective_function = cp.Minimize(total_ETA)

# set constraint
cons1 = []
cons2 = []

# scenario 1
if num_riders == num_drivers:

  for i in range(len(eta1.index)):
    cons1.append(sum([drivers[i,j]for j in range(eta1.shape[1])])==1)

  for j in range(len(eta1.columns)):
    
    cons2.append(sum([drivers[i,j] for i in range(eta1.shape[0])])==1)


#Scenario 2
elif num_riders > num_drivers:

  for i in range(len(eta1.index)):
    cons1.append(sum([drivers[i,j] for j in range(eta1.shape[1])])<=1)

  for j in range(len(eta1.columns)):
    cons2.append(sum([drivers[i,j] for i in range(eta1.shape[0])])==1)

#Scenario 3
elif num_riders < num_drivers:

  for i in range(len(eta1.index)):
    cons1.append(sum([drivers[i,j] for j in range(eta1.shape[1])])==1)
  
  for j in range(len(eta1.columns)):
    cons2.append(sum([drivers[i,j] for i in range(eta1.shape[0])])<=1)


neg = [drivers >=0]
pos = [drivers <=1]
constraint = neg+pos+cons1+cons2

prob = cp.Problem(objective_function, constraint)
prob.solve(), drivers.value


#################################################################################################
## Section 3: Batching Dispatch Protocol: Maximize Profit Model with a Maximum Dispatch Radius ##
#################################################################################################


rng = np.random.default_rng(42)


num_riders = rng.poisson(lam=15)
num_drivers = rng.poisson(lam=15)

distances = pd.DataFrame(rng.uniform(0, 30, (num_riders, num_drivers)),
                         columns=[f'Driver {j}' for j in range(1, num_drivers+1)],
                         index=[f'Rider {i}' for i in range(1,num_riders+1)])

MDR = 15 # don't dispatch outside of MDR miles
maximum_dispatch_radius = (distances < MDR).apply(lambda x: np.where(x, 1, 0)) # np.where(distances < MDR, 1, 0)

profits = distances.apply(lambda x: x + rng.lognormal(mean=1, sigma=3)) 
# print(maximum_dispatch_radius)
# print(profits)
































































