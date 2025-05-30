#All Interventions Analysis for Long Cooking Time

#Date: 7-10-2024

#Written by: Eartha Weber

# Supplementary Analysis With Long Cooktime
#%%
from datetime import datetime
import numpy as np
import math 
import matplotlib
import matplotlib.pyplot as plt

#%%
import pandas as pd

#%%

# Parameters for the lognormal Monte Carlo distributions for different variables

# Cooking time Long
mean_cooking_time = 259.2
std_dev_cooking_time = 85.2
min_time = 73.2
max_time = 401.4

#Cook time short (test to see if result is similar as changed code to export csv)
#mean_cooking_time = 49.95
#std_dev_cooking_time = 56.36
#min_time = 0
#max_time = 162
# Kitchen volume data 
mean_kitchen_volume = 30.7
std_dev_kitchen_volume = 15.38
min_vol = 13.38
max_vol = 60.57

# Air exchange rate 
mean_air_ex = 14.54
std_dev_air_ex = 8.96
min_air_ex = 4.04
max_air_ex = 33.27

# Number of simulations
num_simulations = 5000

# Calculate the parameters for the lognormal distribution for cooking time, kitchen volume, and air exchange rate 
# Cooking time
mu = np.log((mean_cooking_time**2) / np.sqrt(std_dev_cooking_time**2 + mean_cooking_time**2))
sigma = np.sqrt(np.log(1 + (std_dev_cooking_time**2) / (mean_cooking_time**2)))

# Kitchen volume
mu2 = np.log((mean_kitchen_volume**2) / np.sqrt(std_dev_kitchen_volume**2 + mean_kitchen_volume**2))
sigma2 = np.sqrt(np.log(1 + (std_dev_kitchen_volume**2) / (mean_kitchen_volume**2)))

# Air exchange rate
mu3 = np.log((mean_air_ex**2) / np.sqrt(std_dev_air_ex**2 + mean_air_ex**2))
sigma3 = np.sqrt(np.log(1 + (std_dev_air_ex**2) / (mean_air_ex**2)))

# Constants
MINUTES_PER_DAY = 24 * 60
EMISSION_RATES = { # mg/min
    'trad': 45,
    'lpg': 0.2,
    'improvedcookstove': 21,
    'kerosene': 2.7,
    'naturalgas': 0.2,
    'Biogas': 2.7,
    'Electricity': 0.2
}

# Function to calculate concentration vector and its average
def calculate_concentration_timeline(q, f, c_b, nr_cooking_events, total_cooking_time, alpha_h, V):
    non_cooking_time = MINUTES_PER_DAY - total_cooking_time
    cooking_time_per_event = total_cooking_time // nr_cooking_events
    interval_between_cooking_events = non_cooking_time // nr_cooking_events

    cooking_timeline = np.tile(np.concatenate((np.ones((cooking_time_per_event)), np.zeros(interval_between_cooking_events))), nr_cooking_events)
    cooking_timeline = np.concatenate((cooking_timeline, np.zeros((MINUTES_PER_DAY - len(cooking_timeline))))) # pad with zeros to get a vector of length 1440

    alpha = alpha_h / 60 # convert from changes/hour to changes/minute
    concentration_inflow = np.dot(q, f) # inflow into kitchen during cooking events
    c_cooking = concentration_inflow / (alpha * V) # during cooking events, concentration will converge to this number

    c = np.zeros((MINUTES_PER_DAY)) # initialize concentration vector
    last_cooking_event_time = 0
    last_noncooking_time = 0
    for t in range(MINUTES_PER_DAY):
        if cooking_timeline[t]:
            dt = t - last_noncooking_time
            c[t] = c_cooking * (1 - np.exp(- alpha * dt)) + c_b
            last_cooking_event_time = t
        else:
            dt = t - last_cooking_event_time
            c[t] = c_cooking * np.exp(- alpha * dt) + c_b
            last_noncooking_time = t

    c_k = np.mean(c)
    return c, c_k

# Generate random samples from the lognormal distribution
rng = np.random.default_rng()

simulated_volumes = np.clip(rng.lognormal(mu2, sigma2, num_simulations), min_vol, max_vol)
simulated_airexc = np.clip(rng.lognormal(mu3, sigma3, num_simulations), min_air_ex, max_air_ex)
simulated_times = np.clip(rng.lognormal(mu, sigma, num_simulations), min_time, max_time)

plt.hist(simulated_times, bins=30, density=True, edgecolor='black', alpha=0.5, label='Simulated Cooking Times')
plt.title('Monte Carlo Simulation of Cooking Times')
plt.xlabel('Cooking Time (minutes)')
plt.ylabel('Probability Density')
plt.show()

plt.hist(simulated_volumes, bins=30, density=True, edgecolor='black', alpha=0.5, label='Simulated Kitchen Volumes')
plt.title('Monte Carlo Simulation of Kitchen Volumes')
plt.xlabel('Kitchen Volume (m3)')
plt.ylabel('Probability Density')
plt.show()

plt.hist(simulated_airexc, bins=30, density=True, edgecolor='black', alpha=0.5, label='Simulated Air Exchange Rates')
plt.title('Monte Carlo Simulation of Air Exchange Rates')
plt.xlabel('Air Exchange Rate (hr-1)')
plt.ylabel('Probability Density')
plt.show()

# c_b values to iterate over
c_b_values = [ 5.54,7.17,11.14,8.32,6.56,8.1,26.77,25.95,15.44,7,9.8,7.31,9.2,5.11,22.31,5.23,26.68,20.21,12.09,20.15,9.4,11.24,7.93,5.94,18.92,
7.1]
#[4.73,7.05,11.27,9.91,8.4,11.64,24.12,28.61,13.62,8.3,9.73,9.6,10.21,6.6,23.9,6,26.6,33.3,
#17.84,33,16.03,11.84,9.6,6.22,31.28,5.72
#]






# Model inputs
sources = ['lpg'] # enter here which sources are present. could be multiple of the same type
emission_inflow_fractions = [1] # enter here the ratio of each source that enters the kitchen
nr_cooking_events = 3 # total cooking time is divided equally over the number of cooking events

# Dictionary to store all results for each c_b value
results = {}

mean_daily_cb = []
female_cb = []
male_cb = []



# Run the simulation for each c_b value
for c_b in c_b_values:
    all_concentrations = []
    all_ck = []

    for simulation_index in range(num_simulations):
        total_cooking_time = int(simulated_times[simulation_index])
        alpha_h = int(simulated_airexc[simulation_index])
        V = int(simulated_volumes[simulation_index])

        q = [EMISSION_RATES[source] * 1000 for source in sources]  # convert to ug/min

        c, c_k = calculate_concentration_timeline(q, emission_inflow_fractions, c_b, nr_cooking_events, total_cooking_time,
                                                  alpha_h, V)
        all_concentrations.append(c)
        all_ck.append(c_k)

    # Store the results for the current c_b value
    results[c_b] = {
        'concentrations': all_concentrations,
        'average_concentrations': all_ck
    }

    # Plot sample
    plt.plot(all_concentrations[0], label=f'Simulation for c_b={c_b}')
    plt.title(f'Monte Carlo Simulation of Concentrations for c_b={c_b}')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Concentration (ug/m3)')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Move legend to the right
    # plt.show()

    # Calculate and print exposures
    R_w = 0.742 # exposure rate women
    R_m = 0.450 # exposure rate men

    women_exposure = R_w * np.mean(all_ck)
    men_exposure = R_m * np.mean(all_ck)
    mean_daily_exposure = np.mean(all_ck)

    mean_daily_cb.append(mean_daily_exposure)
    female_cb.append(women_exposure)
    male_cb.append(men_exposure)

    print(f"Mean daily concentration for c_b={c_b}: {np.mean(all_ck)} ug/m3")
    print(f"Women exposure for c_b={c_b}: {women_exposure} ug/m3")
    print(f"Men exposure for c_b={c_b}: {men_exposure} ug/m3")


data = {
    'mean_daily_exposure': mean_daily_cb,
    'female_daily_exposure': female_cb,
    'men_daily_exposure': male_cb
    
}
df = pd.DataFrame(data)

current_timestamp = datetime.now().strftime("%Y%m%d%H%M")

# Create the CSV file name with the timestamp
csv_file_name = f'2050_LPG_All_exposure_values_{current_timestamp}.csv'

# Export the DataFrame to a CSV file
df.to_csv(csv_file_name, index=False)

print("Data has been exported to '{csv_file_name}'")
#%%


#%%
#%%



