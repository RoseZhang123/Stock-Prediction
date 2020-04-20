"""
Stock market prediction using Markov chains.

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module3 as stocks
from collections import defaultdict
import random


### Model

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the 
    given list of data.
    """
    key_seq = []
    data1 = list(data)
    while len(data1) > order:
        key_seq.append(data1[:order + 1])
        data1.pop(0)

    # print key_list

    history = {}
    for item in key_seq:
        if tuple(item[:-1]) not in history.keys():
            history[tuple(item[:-1])] = [item[-1]]
        else:
            history[tuple(item[:-1])].append(item[-1])

    # print history

    for key, value in history.items():
        result_val = defaultdict(float)
        for num in value:
            result_val[num] += 1
        # print result_val
        for key_, val_ in result_val.items():
            result_val[key_] = val_ / len(value)

        history[key] = result_val

    return history


# print markov_chain([0, 1, 2, 1, 0, 1, 2, 1, 0], 1)

### Predict

def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.
    """
    model1 = dict(model)
    last1 = list(last)

    for key, value in model1.items():
        value_seq = [0, 0, 0, 0, 0, 0, 0]
        for keys, values in value.items():
            value_seq[keys] = values
        for idx in range(1, len(value_seq)):
            value_seq[idx] = value_seq[idx] + value_seq[idx - 1]
        model1[key] = value_seq

    # print model1

    for idx in range(num):
        for key, value in model1.items():
            # print "last:", last1[idx:]
            if key == tuple(last1[idx:]):

                # print "key:", key
                ran_num = random.random()
                # print random.random()
                for sub_value in value:
                    if sub_value > ran_num:
                        last1.append(value.index(sub_value))
                        break
                break
        else:
            last1.append(random.choice([0, 1, 2, 3]))

    return last1[-num:]


# print ("predict:", predict({}, [0], 1))


### Error

def mse(result, expected):
    """
    Calculate the mean squared error between the sequences
    result and expected.
    """
    pair = zip(result, expected)
    sum_ = 0
    outcome = 0
    for item in pair:
        sum_ += (item[0] - item[1]) ** 2
    outcome = float(sum_) / len(pair)

    return outcome


# print mse([0, 1, 0], [1, 1, 2])


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.  Returns the average
    mean squared error over the number of trials.

    train  - training data
    order  - order of the markov model to use
    test   - "order" days of testing data
    future - number of days to predict
    actual - actual results for next "future" days
    trials - number of trials to run
    """
    final = 0
    for _ in range(trials):
        result = predict(markov_chain(train, order), test, future)
        expected = actual
        final += mse(result, expected)

    average = float(final) / trials
    return average


print("outcome:", run_experiment([1, 2, 3, 4, 5], 2, [2, 3], 2, [4, 5], 5))


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order - days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)

    # You might want to comment this out while you are developing your code.


run()