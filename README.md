# Lotto_API
> Web scraping API, which provides polish Lotto data.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Features](#features)
* [Status](#status)

## General info
Made to improve some skills and for future idea, for a app which will allow to check the lottery ticket with a pic.
It's a self updating database, which will provade all kind of data about polish Lottery system in main branches (Lotto, Mini Lotto, Eurojackpot, Multimulti, Ekstapensja, Kaskada and Superszansa).
The data are collected from the main page of polish LOTTO (lotto.pl), by webscraping using selenium (JS).
This service is setup on [Heroku](https://api-lotto.herokuapp.com/) https://api-lotto.herokuapp.com/.
The project is in progress.

## Technologies
* Python 3.10
* Flask
* Webscraping, Selenium
* Heroku

## Features 
Till now:
* simple access to Lotto records, by ID /api/lotto/id/? or date /api/lotto/date/YYYYMMDD

## Status
In general this app is in progress, here is whats left to do:
* respond in json
* more possible respond ways
* adding the other branches (Mini Lotto, Eurojackpot etc.)
* adding some API manual
