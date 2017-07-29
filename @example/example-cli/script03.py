import sys
import jasily.cli as cli

def x():
    return 3

print(cli.fire(x))