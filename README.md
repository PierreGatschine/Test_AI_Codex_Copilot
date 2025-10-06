# Test_AI_Codex_Copilot

This project provides a small Tkinter GUI for recording response templates in an SQLite database.

It also includes helper utilities for assisting with common support scenarios such as interpreting ``brew doctor`` output.

## Running the app
1. Initialize the database by executing `python db.py`.
2. Launch the GUI (the "server") with `python gui.py`.

## Analysing Homebrew diagnostics

Pipe the output of `brew doctor` to the analyser to receive a condensed list of
suggestions. On systems where the `python` shim is not available, invoke the
tool with `python3` (or run the script directly because it is executable):

```bash
brew doctor | python3 brew_diagnose.py
# or
brew doctor | ./brew_diagnose.py
```
