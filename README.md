# Install
`pip install git+https://github.com/fierte-product-development/Modules`

# Modules
* logging_wrappers.py

	Returns configured logger and log message dictionary.  
	The original log messages must be saved as 'messages.json'.  
	If you pass the True to third argument, logger will not save log to file.
	```python
	import pathlib
	from fmodules.logging_wrappers import loggingWrappers

	me = pathlib.Path(__file__)
	logger, msg = loggingWrappers.GetLoggingKit(me.stem, me.parent)
	logger.info('log!')
	logger.debug(msg['test'])
	```

	You can also get logger and log messages, using their respective functions.

* subprocess_wrappers.py

	Returned CompletedProcess object has encoded stdout and stderr attributes.
	```python
	from fmodules.subprocess_wrappers import subprocessWrappers

	cp = subprocessWrappers.run('attrib', __file__, shell=True)
	print(cp.stdout)
	```

* pathlib_extensions.py

	Makes hidden directory on Windows/Linux.
	```python
	import pathlib
	import fmodules.pathlib_extensions  # noqa

	hidden_folder = (pathlib.Path(__file__).parent/'hidden_folder').mkdir_hidden()
	```
