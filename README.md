# Halfords Search Tool

This project is made to help search the Halfords website for available stock. It came in very handy during the bike shortage of 2021.

Using the tool, you can return a table of available stock for any barcode and address. Futher, you can have it run in the background and send an email when the desired item is available.

## Installation

Install locally.

```bash
pip install -e C:\\directory_package_is_in\halfords_search
```

## Usage
``` python
import halfords_search

# Making stock queries
stock = halfords_search.query_stock(barcode, address)

# Print table of stock
halfords_search.print_stock(stock)

# Email yourself when an item is available nearby
halfords_search.loop_until_available(barcode, address)
```
## Roadmap
It would be useful for the package to wait in the background until stock is available while the program is open or perhaps even after it closes. The former can be done via the multi-threading or multi-processing packages, but the latter is more difficult to accomplish in a OS independent manner.
