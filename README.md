# DCA Backtest

This repository contains programs to help backtest Dollar Cost Averaging (DCA)

## `ticker_history.py`
You can use `ticker_history.py` to collect ticker history for a single ticker for a given historical time range.  The returned payload is TSV data which is written into the `ticker_data` (created if not exists) path.

The program can be invoked from the command line to simply print the results (along with other messages) to stdout, in addition to creating a flat file under `ticker_data`.  

To understand the arguments do this (Make sure your requirements are properly installed ahead of time):  `python3 ticker_history.py --help`

It can also be used as a module that you could `import` into another program.  The same payload (a string of .tsv data) is returned by the program in this case that can be consumed by the caller.

Note:  There's a check on if a file with the matching data already exists under `ticker_data`, with the pattern `{ticker.upper()}_{start_date_string}_to_{end_date_string}.tsv`.  If such a file exists, it is read and a trip to the Yahoo Finance API (via the `yfinance` module) is suppressed.  If for some reason you want to force the re-creation of a file, simply delete it and call `ticker_history.py` accordingly.

## `sim_dca.py`
`sim_dca.py` is used to simulate Dollar Cost Averaging (DCA) strategies.  Its author is a middle class fellow (i.e. NOT RICH), so take that knowledge and do what you will with it.

For now (at the time of this writing, 2023-04-21), I haven't bothered to parameterize this program.  It simply reads a file that would have been created by the `ticker_history.py` program.  It also exepcts that it will exist ahead of time.  All the parameters that influence the sim are towards the top of `main()` to make them easy to play with

It can be made more fancy at a later date, or never.  Pull requests are welcome