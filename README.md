# Halfords Search Tool

This project is made to help search the Halfords website for available stock. It came in very handy during the bike shortage of 2021.

Using the tool, you can return a table of available stock for any barcode and address. Futher, you can have it run in the background and send an email when the desired item is available.

## Installation

I haven't uploaded to PyPI, but it can be easily installed locally.

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
halfords_search.wait_until_available(barcode, address)

# Email yourself when item is available (non blocking)
halfords_search.wait_until_available(barcode, address, background_search=True)
```
## Roadmap
It would be convenient for the background search to open in a hidden console so that it can continue to search after main window has closed.

## Expected Issues

For sending an email when stock is available. I used a .env file to protect my login details, you should replace the USER and PASS credentials with your preferred method of authentication.
