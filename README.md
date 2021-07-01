[![Test](https://github.com/fierte-product-development/Standard-Library-Extension/actions/workflows/Test.yml/badge.svg)](https://github.com/fierte-product-development/Standard-Library-Extension/actions/workflows/Test.yml)
[![python](https://img.shields.io/github/pipenv/locked/python-version/fierte-product-development/Standard-Library-Extension)](https://github.com/fierte-product-development/Standard-Library-Extension/blob/master/Pipfile)
[![license](https://img.shields.io/github/license/fierte-product-development/Standard-Library-Extension.svg)](https://github.com/fierte-product-development/Standard-Library-Extension/blob/master/LICENSE)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Install
`pip install git+https://github.com/fierte-product-development/Standard-Library-Extension`

# Modules
## logging_wrappers
`getLogger` will always return a logger with the same name(*\_\_package__*).  
These loggers change their behavior depending on the three arguments that passed to `getLogger` **last**.  

- `output_dir` (Path, optional): Logger will Output a .log file to the specified path. Defaults to None.
- `root` (bool, optional): The name of module that called `getLogger` last is added to log messages. Defaults to False.
- `name` (str, optional): You can directly specify the name to be added to log messages. Defaults to "".
```py
# module A
from fmodules.logging_wrappers import getLogger

logger = getLogger()

def log_info(msg: str):
	logger.info(msg)
```

```py
# module B
from fmodules.logging_wrappers import getLogger
import A

logger = getLogger(root=True)

def log_debug(msg: str):
	logger.debug(msg)

log_debug("foo")
>>>   DEBUG 2021-07-01 20:51:36 [B] foo (8:log_debug)
A.log_info("bar")
>>>    INFO 2021-07-01 20:51:37 [B.A] bar
```

## subprocess_wrappers
subprocessWrappers is a wrapper of `run` and `Popen`.  
This wrapper executes `run` and `Popen` with appropriate encoding on Windows/Linux and capture settings.  
```py
from fmodules.subprocess_wrappers import subprocessWrappers

cp = subprocessWrappers.run("attrib", __file__, shell=True)
print(cp.stdout)
```

## pathlib_extensions
`mkdir_hidden` makes hidden directory on Windows/Linux.  
```py
from pathlib import Path
import fmodules.pathlib_extensions  # noqa

path = Path(__file__).parent / "hidden_folder"
path.mkdir_hidden()
```

## dict_wrapper
`AttrDict` is a `dict` allow their elements to be accessed both as keys and as attributes.  
```py
from fmodules.dict_wrapper import AttrDict

attr_dict = AttrDict({"foo": "bar"})
print(attr_dict["foo"])
>>> bar
print(attr_dict.foo)
>>> bar
```

## dataclasses_wrappers
Automatically determines whether to use `defalut` or `default_factory` as the argument to the `field` function.  
`Default` passes init in Ture, `Initial` passes init in False.  
```py
from dataclasses import dataclass
from fmodules.dataclasses_wrappers import Default, Initial

@dataclass
class Foo:
	foo: int = Default(0)  # If you pass T, use default
	bar: list[str] = Initial(list)  # Pass type[T], use default_factory
	baz: bool = Initial()  # Pass nothing to Initial, it will be an instance variable with no initial value.
```

## inspect_wrappers
`previousframe` returns the frame back from `currentframe()` specified by `back` of times."""
```py
from fmodules.inspect_wrappers import previousframe

def foo() -> str:
	return previousframe(2).function

def bar() -> str:
	return foo()

bar()
>>> bar
```
