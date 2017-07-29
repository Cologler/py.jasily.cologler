import sys
import jasily.cli as cli

builder = cli.EngineBuilder()

@builder.command
def x():
    return 3

print(builder.build().execute(sys.argv))