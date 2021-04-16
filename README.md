# Parser-translator for 2048-game family

This is a complete syntax-directed translation scheme that I build for the course Compiler construction at my university.
The specsheet is included for reference.

This is done using [PLY](https://www.dabeaz.com/ply/) in Python 3.

The lexer and parser implementation are in `main.py` while the 2048 game api is in `game.py`.

The source code for ply are present within the directory to avoid installation and also since the library's latesst version
is only available via GitHub: https://github.com/dabeaz/ply`

To run the code, simply run:

```Python3
python3 main.py
```

on the terminal. (python version 3.6+).
