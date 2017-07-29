# jasily.cli

jasily.cli is a sample cli framework for python.

## HOW TO USE

``` py
import jasily.cli as cli

d = {
    'x': 3
}
cli.fire(d, 'x') // output 3
```

Now, wrap as command line script:

``` py
import sys
import jasily.cli as cli

d = {
    'x': 3
}
cli.fire(d, sys.argv) // output 3
```

Try to take over the world !
