# sclogging

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 


A Python module (with the help of coloredlogs) to add color to logs.

Working on docs.

get_logger is where to get started.

Some options allow certain customations in the records themselves (e.g. %c.red%something%c%) sets color for that word then returns to defult color of that level of logging.


Other options:
Colored spacer

Easily setting seperate options for stderr and file logs

Custom timer class

  Allows this: var_a=Timer(level="INFO")
  
               var_a.start_timer(Note="I started it")
               
  Log record =  time <spacer> var_a.module.function.start_timer INFO I started it
  
  
Wraps logging, colorama.BACK, FORE, CURSOR
