import sys
import jasily.cli as cli

def x():
    raise cli.RuntimeException('raise a error')

print(cli.fire(x))