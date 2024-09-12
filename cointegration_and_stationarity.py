#Source: https://www.youtube.com/watch?v=Pn_RiDbK82M
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

import pandas as pd

import matplotlib.pyplot as plt

# explore cointegration
def test_cointegration(stock1, stock2, stock1_name="stock1", stock2_name="stock2"):
    cointegration_test = statsmodels.tsa.stattools.coint(stock1, stock2)
    if (cointegration_test[0] < cointegration_test[2][1]):
        print(f"{stock1_name} and {stock2_name} are likely cointegrated")
    else:
        print(f"{stock1_name} and {stock2_name} are likely not cointegrated")
    print("The t-statistic of unit-root test on residuals", cointegration_test[0])
    print("pvalue", cointegration_test[1])
    print("Critical values @ 1 %, 5 %, and 10 %", cointegration_test[2])
    print("-------------------")
    

def check_cointegration_for_all_pairs(main_df, stocks = ("bol", "odet", "viv", "umg")):
    print("--- ALL OTHER PAIRS ---")
    for i in range(len(stocks)):
        for j in range(i+1, len(stocks)):
            stock1_name = stocks[i]
            stock2_name = stocks[j]
            stock1_column = f"4. close_{stocks[i]}"
            stock2_column = f"4. close_{stocks[j]}"
            test_cointegration(main_df[stock1_column], main_df[stock2_column], stock1_name=stock1_name, stock2_name=stock2_name)

# experiments with stationarity
def check_for_stationarity(timeseries, cutoff=0.05):
    p_value = adfuller(timeseries)[1]
    print("p value:", p_value, "cutoff:", cutoff)
    if p_value < cutoff:
        print(f"{timeseries.name} is likely stationary")
        return True
    else:
        print(f"{timeseries.name} is likely not stationary")
        return False
    
    



def explore_cointegration(stock1, stock2, stock1_name="stock1", stock2_name="stock2"):
    X1 = stock1
    X2 = stock2
    
    # original_column_name = X1.columns[0]
    # print(original_column_name)

    X1 = sm.add_constant(X1)
    fitted_results = sm.OLS(X2, X1).fit()

    column_label = fitted_results.params.index[1]
    print(column_label)
    print(type(column_label))

    # Get rid of the constant column
    X1 = X1[column_label]

    print(fitted_results.params)
    
    #b = fitted_results.params["4. close_bol"]
    
    b = fitted_results.params[column_label]
    Z = X2 - b * X1
    Z.name = "Z"


    mean_Z = Z.mean()
    std_Z = Z.std()
    number_std_deviations = 2
    upper_bound_Z = mean_Z + number_std_deviations * std_Z
    lower_bound_Z = mean_Z - number_std_deviations * std_Z

    plt.figure(figsize=(11, 5))

    plt.plot(Z.index, Z.values, label=Z.name)
    plt.axhline(y=mean_Z, color='#9E9E9E', linestyle='--', label='Mean')
    plt.axhline(y=upper_bound_Z, color="r", linestyle='--', label=f'+{number_std_deviations} std')
    plt.axhline(y=lower_bound_Z, color="r", linestyle='--', label=f'-{number_std_deviations} std')
    plt.xlabel("time")
    plt.ylabel("series value")
    plt.legend()

    check_for_stationarity(Z)
    plt.show()
    
    # second plot:
    plt.figure(figsize=(11, 5))

    plt.plot(X1.index, X1 * b + mean_Z, label=f"beta & intercept adjusted {stock1_name}")
    plt.plot(X2.index, X2, label=f"{stock2_name}")

    plt.xlabel("time")
    plt.ylabel("series value")
    plt.legend(loc='upper left')

    plt.show()
    
    
def explore_cointegration_moving_averages(stock1, stock2, stock1_name="stock1", stock2_name="stock2"):
    # Modified from: https://github.com/quantopian/research_public/blob/master/notebooks/lectures/Introduction_to_Pairs_Trading/notebook.ipynb
    # Get the spread between the 2 stocks
    # Calculate rolling beta coefficient
    S1 = stock1
    S2 = stock2
        
     # Perform rolling OLS regression
    rolling_window = 80
    rolling_beta = pd.DataFrame(index=S1.index)
    for i in range(len(S1) - rolling_window + 1):
        window_S1 = S1.iloc[i:i+rolling_window]
        window_S2 = S2.iloc[i:i+rolling_window]
        model = sm.OLS(window_S2, sm.add_constant(window_S1))
        results = model.fit()
        rolling_beta.loc[window_S1.index[-1], 'beta'] = results.params[1]
    
    spread = S2 - rolling_beta["beta"] * S1
    spread.name = 'spread'

    # Get the 1 day moving average of the price spread
    spread_mavg1 = spread.rolling(window=1).mean()
    spread_mavg1.name = 'spread 1d mavg'

    # Get the 30 day moving average
    spread_mavg80= spread.rolling(window=rolling_window).mean()
    spread_mavg80.name = 'spread 80d mavg'

    plt.plot(spread_mavg1.index, spread_mavg1.values)
    plt.plot(spread_mavg80.index, spread_mavg80.values)

    plt.legend(['1 Day Spread MAVG', '80 Day Spread MAVG'])

    plt.ylabel('Spread');