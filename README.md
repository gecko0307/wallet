# Wallet
Simple personal accounting application. Written in Python 3.7 using Bottle for a server and CEF for a client.

## Features

* Web GUI powered by Chromium Embedded Framework
* Create one or more accounts and track incomes and expenses for them
* Edit existing entries
* All entries fall into one of several predefined categories (for example, Food, Accommodation, Salary, Transportation)
* A number of statistics charts, including cash flow, dynamics, assets distribution, income/expense distribution.

## Limitations and peculiarities

Keep in mind that I wrote this for my own personal use, mainly because I didn't want to entrust my financial information to existing apps. It does the job for me, but it's tailored for my needs and preferences. I don't plan to turn Wallet into more feature-rich and competitive solution.

* The app is in Russian, and making an international version is currently a low priority for me
* Main currency is Russian ruble (RUB). Also USD and EUR are supported for individual accounts, but for statistics all currencies are converted to RUB. I did't need arbitrary currencies, and thus did't implement support for them
* Wallet database is not encrypted! Don't run the app on insecure devices and other people's computers if you use it to store sensitive information
* Data model in the app is very simple, for example there are no double-entries (entries that transfer money from one account to another). I don't plan to improve or change this
* There's no way to add custom categories.

## Usage

To run Wallet, you should install [CEF Python](https://github.com/cztomczak/cefpython) first:

`pip install cefpython3`

And then:

`python wallet.py`
