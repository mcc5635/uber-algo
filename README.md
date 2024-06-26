
# First-Dispatch Routing Protocol with a Maximum Dispatch Radius

## Overview

This white paper outlines the implementation of the First-Dispatch Routing Protocol with a Maximum Dispatch Radius (MDR). The protocol aims to efficiently match a single rider requesting a pick-up with the closest available driver, considering a maximum dispatch radius to enhance the efficiency of the ride-hailing service.

## Problem Statement

The task is to implement the first-dispatch protocol as an optimization problem, where the goal is to dispatch a single driver from a collection of available drivers to a single rider. The implementation must consider the following:

- Each request is immediately assigned to the open driver predicted to have the shortest en route time (ETA).
- A maximum dispatch radius (MDR) constraint is imposed to prevent drivers from being dispatched to pick up very distant riders.

## Data Description

The data required for this implementation includes:

1. **Rider Data**: The location of a single rider requesting a pick-up.
2. **Driver Data**: A data frame containing:
   - Physical distances from the rider to each driver.
   - En route times (ETA) representing the estimated time it will take for a driver to meet the rider once dispatched.
3. **Maximum Dispatch Radius (MDR)**: A cutoff value for dispatching drivers based on their distance to the rider.

## Optimization Model

### Decision Variables

- \( x_i \): A binary variable indicating whether driver \( i \) is dispatched (1 if dispatched, 0 otherwise).

### Objective Function

Minimize the en route time (ETA) for the dispatched driver:
\[ 	ext{Minimize} \sum_{i} 	ext{ETA}_i \cdot x_i \]

### Constraints

1. **Dispatch Constraint**: Only one driver can be dispatched:
   \[ \sum_{i} x_i = 1 \]
2. **MDR Constraint**: Drivers can only be dispatched if their distance to the rider is within the MDR:
   \[ x_i \cdot 	ext{Distance}_i \leq 	ext{MDR}, \quad orall i \]
3. **Binary Constraint**: The decision variables are binary:
   \[ x_i \in \{0, 1\}, \quad orall i \]

## Implementation Steps

1. **Data Preparation**: Load the rider data, driver data (distances and ETAs), and MDR.
2. **Optimization Model Formulation**: Define the decision variables, objective function, and constraints.
3. **Solve the Optimization Problem**: Use an appropriate solver to find the optimal solution.
4. **Result Interpretation**: Determine which driver is dispatched to the rider based on the optimization result.

## Example

Consider the following randomly generated data:

- **Rider**: Location coordinates (e.g., latitude and longitude).
- **Drivers**: A data frame with distances and ETAs to the rider.
- **MDR**: A threshold value (e.g., 5 kilometers).

Using this data, the optimization model can be implemented and solved to determine the best driver to dispatch according to the first-dispatch protocol with an MDR constraint.

## Conclusion

This implementation of the First-Dispatch Routing Protocol with a Maximum Dispatch Radius enhances the efficiency of ride-hailing services by ensuring that drivers are not dispatched to distant riders, thereby optimizing the matching process and reducing overall en route times.
