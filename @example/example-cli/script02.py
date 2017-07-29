import sys
import jasily.cli as cli

class D:
    def x(self):
        return 3

print(cli.fire(D))
