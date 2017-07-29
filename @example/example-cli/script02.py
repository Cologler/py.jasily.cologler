import sys
import jasily.cli as cli

class D1:
    def x1(self):
        return 1

    def x2(self):
        return 2

class D2:
    def x(self):
        return 3

print('[1]: ' + str(cli.fire(D1)))
print('[2]: ' + str(cli.fire(D2)))