import numpy as np
import pandas as pd
import cvxpy as cp

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






















