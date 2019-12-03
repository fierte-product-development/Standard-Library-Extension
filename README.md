# Install
`pip install git+https://github.com/fierte-product-development/Standard-Library-Extension`

# Modules
* logging_wrappers.py

	Returns configured logger and log message dictionary.  
	getLogger: If you pass a Path object to second argument, logger will save log to file.  
	GetLogMessages: The original log messages must be saved as 'messages.json'.  
	```python
	import pathlib
	from fmodules.logging_wrappers import loggingWrappers, loggingTools

	me = pathlib.Path(__file__)
	logger, _ = loggingWrappers.getLogger(__name__, me.parent)
	msg = loggingTools.GetLogMessages(me)
	logger.info('log!')
	logger.debug(msg['test'])
	```

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
