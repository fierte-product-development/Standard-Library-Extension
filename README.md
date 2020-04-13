# Install
`pip install git+https://github.com/fierte-product-development/Standard-Library-Extension`

# Modules
* logging_wrappers.py

	loggingWrappers.getLogger: Returns configured logger.  
	SetLogMessages: Sets log message to object's metadata.  
	logmsg: Gets log message from object's metadata.  
	```python
	from pathlib import Path
	from fmodules.logging_wrappers import loggingWrappers, GetLogMessages

	me = Path(__file__)
	logger, _ = loggingWrappers.getLogger(__name__, me.parent)
	logger.info('log!')

	class Foo:
		def foo(self):
			logger.info(logmsg().test)

	def bar():
		logger.info(logmsg().test)

	SetLogMessages()
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
