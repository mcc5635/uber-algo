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


num_drivers = len(eta1.values[0,:]) # column length
num_riders = len(eta1.values[:,0]) #row length

drivers = cp.Variable(profits.shape, integer=True)

total_profit = sum([profits.values[i,j]*drivers[i,j] for i in range(profits.shape[0])
  for j in range(profits.shape[1])])

objective_function = cp.Maximize(total_profit)

cons1 = []

#Scenario 1
if num_riders == num_drivers:

  for i in range(len(profits.index)):
    cons1.append(sum(drivers[i,j] for j in range(maximum_dispatch_radius.shape[1]))==1)

  for j in range(len(profits.columns)):
    cons1.append(sum(drivers[i,j] for i in range(maximum_dispatch_radius.shape[0]))==1)

    cons1.append(sum(maximum_dispatch_radius.values[i,j]*drivers[i,j] for i in range(maximum_dispatch_radius.shape[0]) 
  for j in range(maximum_dispatch_radius.shape[1])) == len(profits.columns))

#Scenario 2
elif num_riders > num_drivers:

  for i in range(len(profits.index)):
    cons1.append(sum(drivers[i,j] for j in range(maximum_dispatch_radius.shape[1]))<=1)

  for j in range(len(profits.columns)):
    cons1.append(sum(drivers[i,j] for i in range(maximum_dispatch_radius.shape[0]))==1)
  
  cons1.append(sum(maximum_dispatch_radius.values[i,j]*drivers[i,j] for i in range(maximum_dispatch_radius.shape[0]) 
  for j in range(maximum_dispatch_radius.shape[1])) == len(profits.columns))

#Scenario 3
elif num_riders < num_drivers:

  for i in range(len(profits.index)):
    cons1.append(sum(drivers[i,j] for j in range(maximum_dispatch_radius.shape[1]))==1)
    
  for j in range(len(profits.columns)):
    cons1.append(sum(drivers[i,j] for i in range(maximum_dispatch_radius.shape[0]))<=1)
    
  cons1.append(sum([maximum_dispatch_radius.values[i,j]*drivers[i,j] for i in range(maximum_dispatch_radius.shape[0])
    for j in range(maximum_dispatch_radius.shape[1])]) == len(profits.index))

###############################################################
## Section 4:  Optimal Scheduling of Uber Push Notifications ##
###############################################################

rng = np.random.default_rng(42)
# Number of times that you can schedule a push notification
time_periods = rng.integers(1,40) # 4

# Number of push notifications you need to schedule
num_notifications = rng.integers(1,40) # 9

# Goal is to schedule NOTIFICATION to TIME PERIOD

# Score that measures the value of a (push, time) pair
# It represents the output of a machine learning model 
# that predicts the probability of a user making an order within 24 hours of receiving push i at time t
scores = pd.DataFrame(rng.uniform(0, 50, (num_notifications, time_periods)),
                         columns=[f'Time Slot {j}' for j in range(1, time_periods+1)],
                         index=[f'Push Notification {i}' for i in range(1,num_notifications+1)])
# print(scores)

send = cp.Variable(scores.shape, integer=True)

notification_profit = sum([scores.values[i,j]*send[i,j] for i in range(scores.shape[0])
  for j in range(scores.shape[1])])

objective_function = cp.Maximize(notification_profit)

# Constraints
pushy = []

x = [send >= 0] #controll that send variable is binary between 0 and 1

y = [send <= 1] #controll that only one notification is sent


#controlling rows: constraining to send at most one of each push notification
for i in range(len(scores.index)):
    pushy.append(sum([send[i,j] for j in range(scores.shape[1])])<= 1)

#controlling columns: #Send at most F(2) pushes in the time horizon
for j in range(len(scores.columns)):
    pushy.append(sum(send[i,j] for i in range(scores.shape[0])) <=2)


constraint = pushy*x+y
prob = cp.Problem(objective_function, constraint)
prob.solve(), send.value
# print(prob)















































