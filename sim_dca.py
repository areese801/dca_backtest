"""
This program consumes a data payload that would have been created by ticker_history.py
and simulates a strategy of investing a certain amount of money into SPY (or whatever ticker the data represents)
at or near the closing price on days when the stock was trading down.
"""
import os
import csv

def main():
    """
    This is the main program that does the sim described at the top of this module
    :return:
    """

    """
    👇👇👇 If you're tinkering with this sim, you can tweak these values 👇👇👇
    """

    # TODO:  Parameterize all this stuff
    # TODO:  Clean up unused variables

    # input_file = 'SPY_2022-01-01_to_2023-04-20.tsv'
    input_file = 'SPY_2003-01-01_to_2023-04-20.tsv'
    starting_cash = 100000  # How much money to start with (Dollars)
    deployment_size = 50  # How much money to invest at a time (Dollars)
    buy_at = -.0 # The percentage dip at when to buy


    """
    👆👆👆If you're tinkering with this sim, you can tweak these values 👆👆👆
    """


    this_dir = this_dir = os.path.dirname(os.path.realpath(__file__))
    ticker_data_dir = os.path.join(this_dir, 'ticker_data')

    # Read the tsv data into dicts, injecting a day sequence number along the way
    day_number = 0
    daily_trade_data = []
    with open(os.path.join(ticker_data_dir, input_file), 'r') as f:
        reader = csv.DictReader(f, delimiter="\t")
        data_rows = [r for r in reader]
        for row in data_rows:
            _tmp_dict = {}
            _tmp_dict['_day_number'] = day_number
            _tmp_dict.update(row)
            # print(_tmp_dict)
            daily_trade_data.append(_tmp_dict)
            day_number += 1

    # Traverse our list of dicts and inject a (trading) day-over-day price change value
    num_recs = len(daily_trade_data)
    days_since_last_buy = 0
    cash_remaining = starting_cash
    cash_invested = 0
    investments = [] # We'll track buys and their prices in this
    for curr_trading_day_rec in daily_trade_data:
        day_number = curr_trading_day_rec['_day_number']
        if day_number == 0:
            print("Skipping Day 0.  Need a previous day of history to calculate change")
            continue

        prev_day_number = day_number - 1

        curr_day_close_price = float(curr_trading_day_rec['Adj Close'])

        # Get the row for the next trading day.  We expect it to be at the same index in the list
        prev_trading_day_rec = daily_trade_data[prev_day_number]
        _prev_day_number_value = prev_trading_day_rec['_day_number'] # Actually read it out for sanity checking purposes
        prev_day_close_price = float(prev_trading_day_rec['Adj Close'])

        # Sanity Check
        if _prev_day_number_value != day_number - 1:
            err_string = f"Something is wrong with this program. " \
                         f"The previous day number should be one less than the current day.  " \
                         f"Got:  Previous Day = {_prev_day_number_value}.  Current Day = {day_number}"
            raise ValueError(err_string)

        # Calculate the change in price
        _price_change = curr_day_close_price - prev_day_close_price
        _price_change_percent = _price_change / prev_day_close_price

        # To buy or not to buy?
        if _price_change_percent <= buy_at:  #TODO:  This should be a paremeter or at least hard coded near the top
            # The price went down so we want to deploy some money

            # Calculate the amount to deploy based on how many days it's been since a buy
            multiplier = max(days_since_last_buy, 1)
            amount_to_deploy = min(deployment_size * multiplier, cash_remaining)
            cash_remaining = cash_remaining - amount_to_deploy
            cash_invested = cash_invested + amount_to_deploy

            # Calculate the number of (partial) shares the investor buys
            num_shares = amount_to_deploy / curr_day_close_price
            investment = dict(num_shares=num_shares, buy_price=curr_day_close_price)
            investments.append(investment)

            # Traverse all the investments that have been made and calculate their value
            _num_shares_cumulative = 0
            for inv in investments:
                _num_shares = inv['num_shares']
                _num_shares_cumulative += _num_shares
            _cumulative_value = _num_shares_cumulative * curr_day_close_price

            # Calculate the total amount invested vs the current value
            profit = _cumulative_value - cash_invested
            profit_percent = profit / cash_invested

            print(f"Investor Buys on Day {day_number} since the Percent Change since last close is {format(_price_change_percent, '.2%')}.  It has been {days_since_last_buy} days since the last buy.\nThe buy amount is {amount_to_deploy} for {num_shares} shares at a price of {curr_day_close_price}")
            print(f"\tThe investor started with {starting_cash} and has invested {cash_invested} into {_num_shares_cumulative} shares.\n\tThe cumulative value of all of the shares is {_cumulative_value} for a profit (or loss) of {profit} ({format(profit_percent, '.2%')}).  The investor has {cash_remaining} cash remaining.\n")
        else:
            days_since_last_buy += 1
            # print(f"Investor DOES NOT BUY on Day {day_number} since the Percent Change since last close is {format(_price_change_percent, '.2%')}")

        if cash_remaining == 0:
            print("Sim stops because cash is gone")
            break

    """
    # Do a Summary
    """
    last_day_rec = daily_trade_data[-1]
    last_day_closing_price = float(last_day_rec['Adj Close'])

    # Calc number of shares
    total_shares = 0
    for inv in investments:
        total_shares += inv['num_shares']
    value_of_shares = total_shares * last_day_closing_price
    total_profit = value_of_shares - cash_invested
    total_profit_percent = total_profit / cash_invested
    print(f"\n\nStrategy:\n\tBacktesting with data set: {input_file}\n\tStart with: {starting_cash} (dollars),\n\tDeploy Size: {deployment_size} (dollars)\n\tDeploy When:  The market dips (trading day over trading day) below {format(buy_at, '.2%')}")
    print(f"Summary:\n\tOwned Shares: {total_shares}\n\tValue of Shares: {value_of_shares}\n\tTotal Profit: {total_profit} ({format(total_profit_percent, '.2%')})")

    print("Done")

if __name__ == '__main__':
    main()
