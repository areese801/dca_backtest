# DCA Backtest

This repository contains programs to help backtest Dollar Cost Averaging (DCA)

## `ticker_history.py`
You can use `ticker_history.py` to collect ticker history for a single ticker for a given historical time range.  The returned payload is TSV data which is written into the `ticker_data` (created if not exists) path.

The program can be invoked from the command line to simply print the results (along with other messages) to stdout, in addition to creating a flat file under `ticker_data`.

It can also be used as a module that you could `import` into another program.  The same payload (a string of .tsv data) is returned by the program in this case that can be consumed by the caller.

Note:  There's a check on if a file with the matching data already exists under `ticker_data`, with the pattern `{ticker.upper()}_{start_date_string}_to_{end_date_string}.tsv`.  If such a file exists, it is read and a trip to the Yahoo Finance API (via the `yfinance` module) is suppressed.  If for some reason you want to force the re-creation of a file, simply delete it and call `ticker_history.py` accordingly.

## A simulation program
2023-04-21 - 
A program that would simulate buying SPY (or any ticker) using a DCA strategy of "buying a little on dates where the stock trades lower" is forthcoming.  Still, this repo is sufficiently useful as is, so I'll make it public for now.