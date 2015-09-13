## py.test

The project is quite messy, the current `py.test` project was extracted
from the [pylib](https://pylib.readthedocs.org/) project. Futher down
it's development the plugin architecture was extracted into 
[pluggy](https://github.com/hpk42/pluggy/).

## bird's eye view

The overall control flow is messy, it goes something like this:

- `pytest.py` module is installed as a entry point, it imports and runs
  `_pytest.config:main`
- `_pytest.config:main` does:
  - Instantiates `Config` and `PytestPluginManager`
  - Installs the defaults plugins into `PytestPluginManager`
  - Call the hook `pytest_cmdline_parse`, the implementation `_pytest.config:Config.parse` will be called.
  
    > if no argument is given, it adds the CWD as an argument, this is required for the collection to work
  
  - Call the hook `pytest_cmdline_main`, this will call `_pytest.main:pytest_test_cmdline_main`
- `_pytest.main:pytest_test_cmdline_main` does:
  - Creates a `_pytest.main:Session`
    - `_pytest.main:Session` register itself as a plugin
  - Call the hooks `pytest_sessionstart`, `pytest_collection` and `pytest_runtestloop`
- `_pytest.main:pytest_collection` does:
  - Call the method `_pytest.main:Session.perform_collect`
  
    > this method depends on the arguments parsed by `pytest_cmdline_parse` stored on `_pytest.config:Config.args`
  
  - Call `_pytest.runner:collect_one_node`
  - `_pytest.runner:collect_one_node` does:
    - Call the hook `pytest_collectstart`
    
      > by default it is `_pytest.main:Session.pytest_collectstart`, it checks if it should stop
      
    - Call the hook `pytest_make_collect_report`:
      - It calls `_pytest.capture:CaptureManager.pytest_make_collect_report` to capture the stderr and stdin
      - It calls `_pytest.runner:pytest_make_collect_report` that instantiates `_pytest.runner:Callinfo`
        passing a private method `_memocollect` from the collector (at this point the collector is the
        `_pytest.main:Session` instance), the method name is as such because the collection is `memoized`
        and it wraps the `collect` method
  - `_pytest.main:Session.collect` does:
    - Run the collection for every argument in `_pytest.config:Config.args`, and it dispatches to `_collect`
  - `_pytest.main:Session._collect` does:  
    - Create a [py.local](https://pylib.readthedocs.org/en/latest/path.html#py-path-local-local-file-system-path)
      instance for every argument and calls the `visit` method.
      - it will loop through the directories calling the hooks `pytest_ignore_collect` and `pytest_collect_directory`
      - it will loop through the files and call the hooks `pytest_ignore_collect` and `pytest_collect_file`.
  
  - `pytest_collect_file` will collect doctests through `_pytest.doctest:pytest_collect_file` and python modules through
    `_pytest.python:pytest_collect_file`
    
  - `_pytest.runner:collect_one_node` will use the `_pytest.runner:Callinfo.result` (this is a `_memocollect` wrapper)
    and pass it to `_pytest.runner:CollectReport.result`, the `CollectReport` is returned to
    `_pytest.main:Session.perform_collect` that calls the hook `pytest_collect_modifyitems` on the `CollectReport`
- The `pytest_runtestloop` hook calls `_pytest.main:pytest_runtestloop` which does:
  - Use the report `items` and for each item calls the hook `pytest_runtest_protocol`
  
## PluginManager

- PytestPluginManager is a pluggy.PluginManager with some methods
  overwritten, it's end goal is twofold:

  - to declare a plugin interface, it can be a class or a module, every
    method will have it's own `hook`
  - the hook is a "multicall", where it calls all callbacks that were register
    for that given method.
    
     _pytest.hookspec.py
