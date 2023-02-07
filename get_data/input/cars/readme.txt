
1. Data

Car time series -> all vehicles (trusted and untrusted)
Request time series -> following Poisson

Requests (Poisson) -> Number of Vehicles (?)

2. Predictions

For Request Prediction I followed this approach:

- Tasks (requests) are generated following a Poisson distribution. In this case, we have 20.000 requests. I'm using 85% for training and 15% for testing.

- We will use from the test data (15%) to run the simulations.

- In this case, we will know how many requests there are at times 15, 30, 45 and 60 seconds.

For Resource Prediction I will follow this approach:

- Run the prediction models considering the time series already created for each cell. I will use 85% for training and 15% for testing.

- For each observation interval (15, 30, 45, 60), subtract the number of untrusted vehicles.

- This is necessary because we do not have the time series with only trusted vehicles.

3. 


Cell1 -> 10 cars -> {1:[1,0,0,1,2,3,4], 2:[4,1,2,4,1,0,0], ..., 10:[0,0,1,3,3,0,1]} -> SUM(1+4+,..,+0)