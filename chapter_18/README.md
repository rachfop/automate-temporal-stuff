# Chapter 18: Look busy

This program simulates user activity on a computer by moving the mouse cursor every 10 seconds. It does so by running a workflow with a single activity, which moves the mouse cursor by a small amount. The workflow runs indefinitely until interrupted.

## Requirements

- Python 3.7+
- temporalio library
- pyautogui library

## Usage

```python
poetry run python look_busy.py
```

The workflow will start executing and continue indefinitely until you interrupt it with `CTRL-C`.