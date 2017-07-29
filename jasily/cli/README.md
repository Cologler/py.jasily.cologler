# jasily.cli

jasily.cli is a sample cli framework for python.

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

class D:
    def x(self):
        return 3

print(cli.fire(D))
```

Save as `script02.py`. Run it:

``` cmd
>>> script02.py x // output 3
```

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
>>> script03.py x // output 3
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
>>> script04.py x // output 3
```
