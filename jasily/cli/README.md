# jasily.cli

jasily.cli is a sample cli framework for python.

Google has a cli framework name `fire`, but jasily.cli is more faster.

## HOW TO USE

Write a command line script:

``` py
import sys
import jasily.cli as cli

d = {
    'x': 3
}
print(cli.fire(d))
```

Save as `script01.py`. Run it:

``` cmd
>>> script01.py x // output 3
```

Try to take over the world !

## MORE

`cli.fire` just a wrapper for `cli.EngineBuilder`:

``` py
def fire(obj, argv=sys.argv, **kwargs):
    engine = EngineBuilder().add(obj).build()
    return engine.execute(argv, **kwargs)
```

### use class

``` py
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
```

Save as `script02.py`. Run it:

``` cmd
>>> script02.py x1
// output:
// [1]: 1
// [2]: 3
```

**If only got one func in class (like `D2`), engine will auto match the func and skip parse argv.**

### use function

``` py
import sys
import jasily.cli as cli

def x():
    return 3

print(cli.fire(x))
```

Save as `script03.py`. Run it:

``` cmd
>>> script03.py // output 3
```

### use descriptor

``` py
import sys
import jasily.cli as cli

builder = cli.EngineBuilder()

@builder.command
def x():
    return 3

print(builder.build().execute(sys.argv))
```

Save as `script04.py`. Run it:

``` cmd
>>> script04.py // output 3
```

### use error

``` py
import sys
import jasily.cli as cli

def x():
    raise cli.RuntimeException('raise a error')

print(cli.fire(x))
# raise a error   // engine auto print `RuntimeException` message
# None            // engine return value for print().
```
