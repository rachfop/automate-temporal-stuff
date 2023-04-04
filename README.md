# Automate the Temporal Stuff

This repository implements the _Practice Projects_ in each chapter of [Automate the Boring Stuff](https://automatetheboringstuff.com) by Al Sweigart.

## Usage

Prerequisites:

* Python >= 3.7
* [Poetry](https://python-poetry.org)
* [Local Temporal server running](https://docs.temporal.io/application-development/foundations#run-a-development-cluster)

With this repository cloned, run the following at the root of the directory:

    poetry install

That loads all required dependencies. Then to run a sample, usually you just run it in Python. For example:

    poetry run python chapter_04/list_joiner.py

## Chapters

- [x] [Chapter 03](./chapter_03/)
  - [x] The Collatz Sequence (MathPlotLib)
- [x] [Chapter 04](./chapter_04/)
  - [x] Character Grid
  - [x] Oxford Comma
- [x] [Chapter 05](./chapter_05/)
  - [x] Fantasy Game Inventory
  - [x] List to Dictionary Function for Fantasy Game Inventory
- [x] [Chapter 06](./chapter_06/)
  - [x] Table Printer
- [x] [Chapter 07](./chapter_07/)
  - [x] Strip() Method
  - [x] Password strength checker
- [x] [Chapter 07 with Encryption](./chapter_07_encryption/)
  - [x] Password strength checker with encryption
- [x] [Chapter 08](./chapter_08/)
  - [x] Madlib
- [x] [Chapter 10](./chapter_10/)
  - [x] Coin toss
- [x] [Chapter 17](./chapter_17/)
  - [x] Prettified Stopwatch
- [x] [Chapter 18](./chapter_18/)
  - [x] Look Busy mouse mover

### Extras

- [Web Servers](./web_frameworks/)
  - [Fast API](./web_frameworks/fast/)
  - [Flask](./web_frameworks/flask/)
  - [Starlette](./web_frameworks/starlette/)
- [IOT](./iot/)
  - CO2 monitor

## Pull requests

Before making a pull request, lint and format.

```bash
poe lint
poe format
```
