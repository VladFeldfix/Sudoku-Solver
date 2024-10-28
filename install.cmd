set "currentDirectory=%cd%
pyinstaller --distpath %currentDirectory% -i favicon.ico --onefile --noconsole Sudoku-Solver.py
pause