# Install
`pip install git+https://github.com/fierte-product-development/Modules`

# Modules
* logging_wrappers.py

	Returns configured logger and log file path.  
	If you pass directory path to second argument, logger will save log to file.
	```python
	import pathlib
	from fmodules.logging_wrappers import loggingWrappers

	output_dir = pathlib.Path(__file__).parent
	logger, log_file = loggingWrappers.getLogger(__name__, output_dir)
	logger.info('log!')
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
