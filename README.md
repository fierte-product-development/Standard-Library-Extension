# Install
`pip install git+https://github.com/fierte-product-development/Standard-Library-Extension`

# Modules
* logging_wrappers.py

	`loggingWrappers.getLogger`: Returns configured `Logger`.  
	`SetLogMessages`: Sets log message to object's metadata.  
	`logmsg`: Gets log message from object's metadata.  
	```python
	from pathlib import Path
	from fmodules.logging_wrappers import loggingWrappers, SetLogMessages, logmsg

	me = Path(__file__)
	logger, _ = loggingWrappers.getLogger(__name__, me.parent)
	logger.info("log!")

	class Foo:
	    def foo(self):
	        logger.info(logmsg().test)

	def bar():
	    logger.info(logmsg().test)

	SetLogMessages()
	```

* subprocess_wrappers.py

	subprocessWrappers is a wrapper of `run` and `Popen`.  
	This wrapper executes `run` and `Popen` with appropriate encoding on Windows/Linux and capture settings.  
	```python
	from fmodules.subprocess_wrappers import subprocessWrappers

	cp = subprocessWrappers.run("attrib", __file__, shell=True)
	print(cp.stdout)
	```

* pathlib_extensions.py

	`mkdir_hidden` makes hidden directory on Windows/Linux.  
	```python
	import pathlib
	import fmodules.pathlib_extensions  # noqa

	hidden_folder = (pathlib.Path(__file__).parent / "hidden_folder").mkdir_hidden()
	```

* dict_wrappers.py

	`AttrDict` is a `dict` allow their elements to be accessed both as keys and as attributes.  
	```python
	from fmodules.dict_wrappers import AttrDict

	attr_dict = AttrDict({"foo": "bar"})
	print(attr_dict["foo"])
	print(attr_dict.foo)
	```

* dataclasses_wrappers.py

	Automatically determines whether to use `defalut` or `default_factory` as the argument to the `field` function.  
	`Default` passes init in Ture, `Initial` passes init in False.  
	```python
	from dataclasses import dataclass
	from fmodules.dataclasses_wrappers import Default, Initial

	@dataclass
	class Foo:
	    foo: int = Default(0)
	    bar: list[str] = Initial([])
	```
