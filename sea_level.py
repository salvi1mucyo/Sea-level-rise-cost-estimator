# -*- coding: utf-8 -*-
# 6.100B Fall 2024
# Problem Set 4: Sea Level Rise
# Name: Salvi Mucyo
# Collaborators:

import matplotlib.pyplot as plt
import numpy as np
import csv

#####################
# Begin helper code #
#####################

def load_data():
    """
	Loads data from sea_level_change.csv and puts it into numpy arrays

	Returns:
		a length 3 tuple of 1-d numpy arrays:
		    1. an array of years as ints
		    2. an array of mean annual sea level rises (as floats) for the years from the first array
		    3. an array of standard deviation of annual sea level rise (as floats) for the years from the first array
        eg.
            (
                [2030, 2040, ..., 2100],
                [0.17, 0.21, ..., 0.8],
                [0.01, 0.02, ..., 0.13]
            )
            can be interpreted as:
                The mean sea level rise in the calendar year 2030 will be 0.17 inches
                with a standard deviation of 0.01 inches.
	"""
    with open("sea_level_change.csv", mode='r') as file:
        reader = csv.reader(file)

        _ = next(reader)
        years = []
        mean = []
        std = []
        for row in reader:
            years.append(int(row[0]))
            mean.append(float(row[1]))
            std.append(float(row[2]))

        return (np.array(years), np.array(mean), np.array(std))

def get_damage_cost_no_insurance():
    """
    Returns:
        dictionary mapping sea level rise (inches) during the year to
        the percentage of the home that is damaged and must be paid for,
        assuming no insurance
    """
    return {
        0.1: 0,
        0.2: 2,
        0.3: 5,
        0.4: 8,
        0.5: 11,
        0.6: 15,
        0.7: 20,
        0.8: 25
    }

def get_damage_cost_with_insurance():
    """
    Returns:
        dictionary mapping sea level rise (inches) during the year to
        the percentage of the home that is damaged and must be paid for,
        given that the homeowner has insurance
    """
    return {
        0.1: 0,
        0.2: 0,
        0.3: 0,
        0.4: 2,
        0.5: 5,
        0.6: 8,
        0.7: 11,
        0.8: 15
    }

def get_cumulative_std_devs(std_devs):
    '''
    Given an array of standard deviations, produces a 1D numpy array
    with the cumulative standard deviations up until each index in the
    original array.

    Args:
        std_devs: a 1D numpy array of standard deviations you want to
        accumulate
    Returns:
        A 1D numpy array with the cumulative sum so far for each index
        in the original array
    '''
    return np.sqrt(np.cumsum(std_devs))

###################
# End helper code #
###################


##########
# Part 1 #
##########

def predict_sea_level_rise():
    """
	Creates a numpy array from the data in sea_level_change.csv.
    If the year is between 2030 and 2100, inclusive, and not included in the data,
    the values for that year should be interpolated.

	Returns:
		a 2-d numpy array with each row containing the year, the mean, the 2.5th
        percentile, 97.5th percentile, and standard deviation of the annual sea
        level rise for all the years between 2030 and 2100.
	"""
    years, mean, std = load_data()
    years_included_data = {years[i]: (mean[i], std[i]) for i in range(len(years))}

    # find years not included in the data and then interporate the data
    years_not_included = [year for year in range(2030,2101) if year not in years_included_data]
    mean_interp = np.interp(years_not_included, years, mean)
    std_interp = np.interp(years_not_included, years, std)
    years_not_included_data = {years_not_included[i]: (mean_interp[i], std_interp[i]) for i in range(len(years_not_included))}
    sea_level_data = []

    # find the corresponding mean, standard deviation, 2.5th percentile and 97.5th percentile
    for year in range(2030,2101):
        # if the data was previously included
        if year in years_included_data:
            mean, std = years_included_data[year]
            slow_slr = mean - 2 * std
            fast_slr = mean + 2 * std
            data = [year, mean, slow_slr, fast_slr, std]
            sea_level_data.append(data)

        # if the data wasn;t previouslsy included
        else:
            mean, std = years_not_included_data[year]
            slow_slr = mean - 2 * std
            fast_slr = mean + 2 * std
            data = [year, mean, slow_slr, fast_slr, std]
            sea_level_data.append(data)
    return np.array(sea_level_data)




def predict_cumulative_sea_level_rise(show_plot=True):
    """
    Calculate and plot the cumulative sea level rise since 2030
    for mean, slow SLR, and fast SLR scenarios from 2030-2100.

    Note, standard deviations are not additive so you should use the
    get_cumulative_std_devs() helper function and base your calculation
    of cumulative slow_SLR and fast_SLR on the result.

    Returns:
		a 2-d numpy array with each row containing the year, the mean, the 2.5th
        percentile, 97.5th percentile, and standard deviation of the cumulative
        sea level rise from 2030 to 2100 for the years between 2030-2100 inclusive
    """
    # get the years, means and standard deviation arrays
    predicted_slr_transpose = predict_sea_level_rise().T
    years, means, std_devs = predicted_slr_transpose[0], predicted_slr_transpose[1], predicted_slr_transpose[4]

    # calculate the cumulative standard devs, mean, slow slr and fast slr
    cumulative_std_devs = get_cumulative_std_devs(std_devs)
    cumulative_mean = np.cumsum(means)
    cumulative_slow_slr = cumulative_mean - 2 * cumulative_std_devs
    cumulative_fast_slr = cumulative_mean + 2 * cumulative_std_devs

    # plot the graphs
    plt.plot(years, cumulative_fast_slr, 'b--')
    plt.plot(years, cumulative_mean, color='orange')
    plt.plot(years, cumulative_slow_slr, 'g--')
    plt.title('Predicted Cumulative Sea Level Rise since 2030')
    plt.xlabel('Year')
    plt.ylabel('Sea leel rise (in)')
    plt.legend(('Upper bound', 'Mean', 'Lower bound'))
    if show_plot:
        plt.show()
    return np.column_stack([years, cumulative_mean, cumulative_slow_slr, cumulative_fast_slr, cumulative_std_devs])

def simulate_year(data, year, num):
    """
	Simulates the sea level rise for a particular year based on that year's
    mean and standard deviation, assuming a normal distribution.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2030-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year
		year: the year to simulate sea level rise for
        num: the number of samples you want from this year

	Returns:
		a 1-d numpy array of length num, that contains num simulated values for
        sea level rise during the year specified
	"""
    # find the corresponding mean and standard deviation for the year
    row = data[int(year)-2030]
    mean, std = row[1], row[-1]
    return np.random.normal(mean, std, num)

def plot_monte_carlo(data):
    """
	Runs and plots a Monte Carlo simulation, based on the values in data and
    assuming a normal distribution. Five hundred samples should be generated
    for each year.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2030-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year
	"""
    years, means, slow_slr, fast_slr, std_devs = data.T

    # sample 500 slr for each year and then plot on scatter graph
    simulations = [simulate_year(data, year, 500) for year in years]
    for x, y in zip(years, simulations):
        plt.scatter([x] * len(y), y,s=5, alpha=0.5, color='gray')

    # plt the mean and slow slr and fast slr
    plt.plot(years, fast_slr, '--', label='Upper bound')
    plt.plot(years, means, label='Mean')
    plt.plot(years, slow_slr, '--', label='Lower bound')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Sea level rise (in)')
    plt.title('Predicted annual sea level rise, 500 simulations')
    plt.show()


##########
# Part 2 #
##########

def simulate_water_levels(data):
    """
	Simulates the year-over-year sea level rise for all years in the range 2030 to 2100, inclusive.

	Args:
		data: a 2-d numpy array with each row containing the year, the mean, the 2.5th
            percentile, 97.5th percentile, and standard deviation of the sea level rise in
            a year for the years between 2030-2100 inclusive

	Returns:
		a python list of simulated sea level rise since 2030 for each year, in the order in which
        they would occur temporally
	"""
    return [simulate_year(data, year, None) for year in range(2030, 2101)]


def no_insurance_costs(simulated_annual_slr, house_value=1000000):
    """
	Uses simulated annual SLR data from all years in the range 2030 to 2100, inclusive,
    and calculates total cost incurred to owner at each year in millions.

    Each year the homeowner incurs some additional amount of cost based on the amount
    of SLR in that year. If the SLR is negative or 0, there is no additional cost that year.

    The specific damage cost can be calculated using the percentages
    from get_damage_cost_no_insurance(), where each water level corresponds to
    the percentage of the house that was damaged, and that percentage of house_value
    must be paid to repair damages.

    Interpolate values given to get the full continous range of damage cost percentages.

    The total cost at year i is the summation of all costs incurred in previous years,
    up to and including year i.

	Args:
		simulated_annual_slr: list of simulated annual sea level rise for 2030-2100, inclusive
        house_value: the value of the property we are estimating cost for

	Returns:
		a list of total costs incurred in millions for 2030-2100, in the order in which the costs would
        be incurred temporally
	"""
    # get percentage costs with no insurance
    percentage_costs = get_damage_cost_no_insurance()
    costs_incurred = []
    current_cummulative_cost = 0

    # find the asscociated costs for each year
    for year in range(2030, 2101):
        slr = simulated_annual_slr[year-2030]
        if slr > 0:
            if slr in percentage_costs:
                current_cummulative_cost += (house_value * (percentage_costs[slr]/ 100)) /1_000_000

            # if not found in the given costs, sort the slr and percentage costs in ascending order and then interpolate
            else:
                xp_yp = sorted(percentage_costs.items(), key=lambda x: x[0])
                xp = [xp_yp[i][0] for i in range(len(xp_yp))]
                yp = [xp_yp[i][1] for i in range(len(xp_yp))]
                percentage_cost = np.interp(slr, xp, yp)
                percentage_costs[slr] = percentage_cost
                current_cummulative_cost += (house_value * (percentage_cost/100)) /1_000_000
        costs_incurred.append(current_cummulative_cost)
    return costs_incurred

def insure_immediately_costs(simulated_annual_slr, house_value=1000000):
    """
	Uses the simulated annual SLR for all years in the range 2030 to 2100,
    inclusive, and calculates total costs incurred in millions resulting from a
    particular SLR during a given year, using the prepare immediately strategy.

    The homeowner initially invests 200,000 in home insurance in 2030 to reduce future
    costs due to damage.
    The specific additional cost incurred each year can be calculated using the values
    from `get_damage_cost_with_insurance()`, where each SLR amount corresponds to
    the percent of property that is damaged, and that percentage of house_value
    must be paid to repair damages.

	Args:
		simulated_annual_slr: list of simulated annual SLR for 2030-2100 inclusive
        house_value: the value of the property we are estimating cost for

	Returns:
		a list of total costs incurred in millions for 2030-2100, in the order in which the costs would
        be incurred temporally
	"""
    # get percentage costs with insurance and initialize the insurance costs
    percentage_costs = get_damage_cost_with_insurance()
    costs_incurred = []
    current_cummulative_cost = 0.2

    # find the asscociated costs for each year
    for year in range(2030, 2101):
        slr = simulated_annual_slr[year-2030]
        if slr > 0:
            if slr in percentage_costs:
                current_cummulative_cost += (house_value * (percentage_costs[slr]/ 100)) /1_000_000

            # if not found in the given costs, sort the slr and percentage costs in ascending order and then interpolate
            else:
                xp_yp = sorted(percentage_costs.items(), key=lambda x: x[0])
                xp = [xp_yp[i][0] for i in range(len(xp_yp))]
                yp = [xp_yp[i][1] for i in range(len(xp_yp))]
                percentage_cost = np.interp(slr, xp, yp)
                percentage_costs[slr] = percentage_cost
                current_cummulative_cost += (house_value * (percentage_cost/100)) /1_000_000
        costs_incurred.append(current_cummulative_cost)
    return costs_incurred


def invest_and_wait_a_bit_costs(simulated_annual_slr, house_value=1000000, cost_threshold=200000):
    """
	Uses the simulated annual SLR for all years in the range 2030 to 2100,
    inclusive, and calculates total costs incurred in millions resulting from a
    particular SLR during a given year, using the investment + wait strategy.

    Strategy:

    invest $200,000 in a high yield savings account returning 5.4% compounded at the start
    each year, if owner hasn't bought insurnce yet
        - pay for all damage costs incurred that year according to `get_damage_costs_no_insurance()`
        - calculate total cost incurred up to and including that year
        - adjust total cost based on any money earned from the savings account, which reduces
          the total cost for that year
        - assess whether to buy insurance if total cost meets/exceeds cost_threshold
    when total cost at some year meets/exceeds cost_threshold
        - withdraw ALL the money and pay $200,000 for home insurance in the same year
            - add insurance cost to the same year's total cost
            - assume excess money does not earn any more interest
        - in subsequent years, costs incurred are based on the values from `get_damage_costs_with_insurance()`

    Assume the cost of insurance is stagnant at $200,000 for any year the owner chooses to purchase.

    See example on problem set page for clarification.

	Args:
		simulated_annual_slr: list of simulated annual SLR for 2030-2100 inclusive
        house_value: the value of the property we are estimating cost for
        cost_threshold: the amount of cost incurred before insurance is purchased

	Returns:
		a list of total costs incurred in millions for 2030-2100, in the order in which the costs would
        be incurred temporally
	"""
    total_money_in_hysa = 200_000
    costs_incurred = []
    total_cost_incurred = 0
    current_year = 2030
    percentage_costs_no_insurance = get_damage_cost_no_insurance()
    percentage_costs_with_insurance = get_damage_cost_with_insurance()

    # while you are still under the threshold continue without insurance and get interest
    while True:

        # calculate interest and the cost associated
        interest = round(total_money_in_hysa * 5.4 /100, 2)
        total_money_in_hysa += interest
        slr = simulated_annual_slr[current_year-2030]
        if slr > 0:
            if slr in percentage_costs_no_insurance:
                cost = (house_value * (percentage_costs_no_insurance[slr]/ 100)) /1_000_000

            # if not found in the given costs, sort the slr and percentage costs in ascending order and then interpolate
            else:
                xp_yp = sorted(percentage_costs_no_insurance.items(), key=lambda x: x[0])
                xp = [xp_yp[i][0] for i in range(len(xp_yp))]
                yp = [xp_yp[i][1] for i in range(len(xp_yp))]
                percentage_cost = np.interp(slr, xp, yp)
                percentage_costs_no_insurance[slr] = percentage_cost
                cost = (house_value * (percentage_cost/100)) /1_000_000
        total_cost_incurred += cost - (interest/1_000_000)
        current_year += 1

        # if all the years are over return
        if current_year > 2100:
            costs_incurred.append(total_cost_incurred)
            return costs_incurred

        # if you've reached the cost thresshold, pay the insurance and then break
        if total_cost_incurred >= cost_threshold/1_000_000:
            total_cost_incurred += 0.2
            costs_incurred.append(total_cost_incurred)
            break
        costs_incurred.append(total_cost_incurred)

    # after exceeding the threshold and pating the insurance continue by calculating damages with insurance
    for year in range(current_year, 2101):
        slr = simulated_annual_slr[year-2030]
        if slr > 0:
            if slr in percentage_costs_with_insurance:
                total_cost_incurred += (house_value * (percentage_costs_with_insurance[slr]/ 100)) /1_000_000

            # if not found in the given costs, sort the slr and percentage costs in ascending order and then interpolate
            else:
                xp_yp = sorted(percentage_costs_with_insurance.items(), key=lambda x: x[0])
                xp = [xp_yp[i][0] for i in range(len(xp_yp))]
                yp = [xp_yp[i][1] for i in range(len(xp_yp))]
                percentage_cost = np.interp(slr, xp, yp)
                percentage_costs_with_insurance[slr] = percentage_cost
                total_cost_incurred += (house_value * (percentage_cost/100)) /1_000_000
        costs_incurred.append(total_cost_incurred)
    return costs_incurred



def plot_strategies(data, house_value=1000000, cost_threshold=200000):
    """
	Runs and plots a Monte Carlo simulation of all of the different preparation
    strategies, based on the values in data and assuming a normal distribution.
    500 samples should be generated for each year.

    Scatter plot all 500 samples for each year and each preparation strategy.
    Overlay one line plot for each preparation strategy that shows the average
    cost across the 500 simulations for each year.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2030-2100
            inclusive, the 2.5th percentile, 97.5th percentile, mean, and standard
            deviation of the sea level rise for the given year
        house_value: the value of the property we are estimating cost for
        cost_threshold: the amount of cost that can be incurred before insurance is purchased
	"""
    means_strategy_1 = []
    means_strategy_2 = []
    means_strategy_3 = []
    simulations_1 = []
    simulations_2 = []
    simulations_3 = []
    years = [year for year in range(2030, 2101)]

    # do 500 simulations and get costs for each year
    for _ in range(500):
        simulated_slr = simulate_water_levels(data)
        simulations_1.append(no_insurance_costs(simulated_slr, house_value))
        simulations_2.append(insure_immediately_costs(simulated_slr, house_value))
        simulations_3.append(invest_and_wait_a_bit_costs(simulated_slr, house_value, cost_threshold))

    # plot the simulations
    for i in range(500):
        plt.scatter(years, simulations_1[i], color='#8AAAE5', s= 10, alpha= 0.5, label='No insurance')
        plt.scatter(years, simulations_2[i], color='orange', s= 10, alpha= 0.5, label='With Insurance')
        plt.scatter(years, simulations_3[i], color='#A7BEAE', s= 10, alpha= 0.5, label='Invest and insure later')

    # find the means for each year
    for year in range(2030, 2101):
        mean_1 = sum(simulations_1[i][year-2030] for i in range(500))/ 500
        means_strategy_1.append(mean_1)
        mean_2 = sum(simulations_2[i][year-2030] for i in range(500))/ 500
        means_strategy_2.append(mean_2)
        mean_3 = sum(simulations_3[i][year-2030] for i in range(500))/ 500
        means_strategy_3.append(mean_3)

    # plot the means
    plt.plot(years, means_strategy_1, '--',color='blue',  lw=2, label='Mean total cumulative damages per year with no insurance')
    plt.plot(years, means_strategy_2, '--',color='red', lw=2, label='Mean total cumulative damages per year with insurance')
    plt.plot(years, means_strategy_3, '--',color='green', lw=2, label='Mean total cumulative damages per year while investing and insuring later')

    # remove duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    plt.legend(unique_labels.values(), unique_labels.keys())
    plt.xlabel('Year')
    plt.ylabel('Cumulative damages (Million $)')
    plt.title('Predicted cumulative damages due to sea level rise with different strategies, 500 simulations')
    plt.show()

if __name__ == '__main__':
    # Comment out the 'pass' statement below to run the lines below it
    # pass
    annual_rise_data = predict_sea_level_rise()
    # simulated_rise = simulate_water_levels(annual_rise_data)
    # invest_and_wait_a_bit_costs(simulated_rise)
    # cumulative_rise_data = predict_cumulative_sea_level_rise(False)
    # plot_monte_carlo(annual_rise_data)
    plot_strategies(annual_rise_data)
    pass
