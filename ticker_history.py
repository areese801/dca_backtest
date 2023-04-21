"""
This module gets trailing stock history for a given ticker for a given historical timeframe from Yahoo finance
If called as a program from the CLI, the results (and other messages will be printed to stdout).
If called as a module, the results will be printed to stdout, and also returned
"""
import os
import sys
import datetime
import time_help
import argparse

import yfinance

EXPECTED_DATE_FORMAT = '%Y-%m-%d'

def _is_valid_date(date_string:str)-> bool:
    """
    Helper function to ensure that dates are well-formed for the main program
    :param date_string:
    :return:
    """

    # Test #1:  Should be a string
    if not type(date_string) is str:
        err_string = f"The date string should be of type {type(str)}.  Got {type(date_string)}"
        print(err_string, sys.stderr)
        return False

    # Test #2:  Should be YYYY-MM-DD.
    # Easiest test is to try to instantiate a datetime object as such and test for a failure
    try:
        _dt = datetime.datetime.strptime(date_string, EXPECTED_DATE_FORMAT)
    except Exception as ex:
        err_string = f"The input string is not in the proper format: {EXPECTED_DATE_FORMAT}."
        print(err_string, sys.stderr)
        return False

    return True




def main(ticker:str, start_date:str = None, end_date:str=None):
    """

    :param ticker: The ticker symbol you want to extract
    :param start_date: The start date for the trailing history as YYYY-MM-DD.  Optional.
        If not provided 365 trailing days will be retrieved
    :param end_date: The end date for the trailing history as YYYY-MM-DD.  Optional.
        If not provided, 365 trailing days will be retrieved
    :return: A string which is a tsv data matching the results
    """

    """
    Handle dates
    """
    yesterday = time_help.yesterday().replace(tzinfo=None)

    # Test and Cast:  Dates should be passed in as strings as YYYY-MM-DD
    if start_date is not None:
        if _is_valid_date(date_string=start_date) is False:
            raise ValueError(f"The start_date parameter passed into this program is invalid: {start_date}")
        else:
            start_date = datetime.datetime.strptime(start_date, EXPECTED_DATE_FORMAT)  # Coerce to date time object
    else:
        start_date = time_help.date_sub(some_datetime=yesterday, days_to_subtract=365)

    if end_date is not None:
        if _is_valid_date(date_string=end_date) is False:
            raise ValueError(f"The end_date parameter passed into this program is invalid: {end_date}")
        else:
            end_date = datetime.datetime.strptime(end_date, EXPECTED_DATE_FORMAT)  # Coerce to date time object
    else:
        end_date = yesterday

    # End Date must be <= yesterday
    if end_date > yesterday:
        end_date = yesterday
        print(f"The end date cannot be greater than yesterday's date.  Changed to "
              f"{datetime.datetime.strptime(end_date, EXPECTED_DATE_FORMAT)}", file=sys.stderr)

    # Start_date must be <= end_date.  Swap as necessary
    if not start_date <= end_date:
        print(f"Start Date was passed in as after the End Date.  Swapping.", file=sys.stderr)
        _temp_date = start_date
        start_date = end_date
        end_date = _temp_date
        print(f"Start Date is now {datetime.datetime.strftime(start_date, EXPECTED_DATE_FORMAT)}.  "
              f"End Date is now {datetime.datetime.strftime(end_date, EXPECTED_DATE_FORMAT)}")
    """
    Now for the good part.  Get the ticker data!
    """
    start_date_string = datetime.datetime.strftime(start_date, EXPECTED_DATE_FORMAT)
    end_date_string = datetime.datetime.strftime(end_date, EXPECTED_DATE_FORMAT)

    # Handle output file name
    this_dir = this_dir = os.path.dirname(os.path.realpath(__file__))
    ticker_output_dir = os.path.join(this_dir, 'ticker_data')
    ticker_file_name_short = f"{ticker.upper()}_{start_date_string}_to_{end_date_string}.tsv"
    ticker_file_name = os.path.join(ticker_output_dir, ticker_file_name_short)
    if not os.path.isdir(ticker_output_dir):
        os.makedirs(ticker_output_dir, exist_ok=False)

    # Save a call to yahoo finance if we already have a file with our desired data in it
    if os.path.isfile(ticker_file_name):
        with open(ticker_file_name, 'r') as f:
            ticker_data_tsv = f.read()
            print(f"Read ticker data from file {ticker_data_tsv}")
    else:
        ticker_data = yfinance.download(tickers=ticker, start=start_date_string, end=end_date_string)
        ticker_data_tsv = ticker_data.to_csv(sep="\t", index=False)

        with open(ticker_file_name, 'w') as f:
            f.write(ticker_data_tsv)
            print(f"Wrote ticker data into file {ticker_data_tsv}")

    print(ticker_data_tsv)
    return ticker_data_tsv


if __name__ == '__main__':
    argp = argparse.ArgumentParser(description="Retrieve historical stock data for a ticker")
    argp.add_argument('-s', '--start-date', required=False, default=None
                      , help="The start date for the time period as YYYY-MM-DD")
    argp.add_argument('-e', '--end-date', required=False, default=None
                      , help="The end date for the time period as YYYY-MM-DD")
    argp.add_argument('-t', '--ticker', required=False, default='SPY', help="The ticker symbol.  Defaults to SPY")

    args = vars(argp.parse_args())
    start_date = args.get('start_date')
    end_date = args.get('end_date')
    ticker = args.get('ticker')

    print(f"Calling main program with arguments: start_date = '{start_date}', end_date = '{end_date}', ticker = '{ticker}'")
    main(ticker=ticker, start_date=start_date, end_date=end_date)


