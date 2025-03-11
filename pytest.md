# Pytest

Pytest tutorial shows how to test Python application using the pytest module.

## Python pytest

Pytest is a Python library for testing Python applications. It is an alternative
to nose and unittest.

## pytest install

Pytest is installed with the following command:

```
$ pip install pytest
```

This installs the `pytest` library.

## pytest test discovery conventions

If no arguments are specified then test files are searched in locations from
`testpaths` (if configured) or the current directory.
Alternatively, command line arguments can be used in any combination of
directories, file names or node ids.

In the selected directories, pytest looks for `test_*.py`
or `*_test.py` files. In the selected files, pytest looks for
test prefixed test functions outside of class and test prefixed test methods
inside Test prefixed test classes (without an `__init__` method).

## Running pytest

With no arguments, pytest looks at the current working directory (or some other
preconfigured directory) and all subdirectories for test files and runs the test
code it finds.

```
$ pytest
```

Running all test files in the current directory.

```
$ pytest min_max_test.py
```

We can run a specific test file by giving its name as an argument.

```

$ pytest min_max_test.py::test_min

```

A specific function can be run by providing its name after the `::`
characters.

```

$ pytest -m smoke

```

Markers can be used to group tests. A marked grouped of tests is then
run with `pytest -m`.

```

$ pytest -k <expression>

```

In addition, we can use expressions to run tests that match names of test
functions and classes.

## Python pytest simple example

In the first example, we are going to test two simple math algorithms with
pytest.

algo.py

```

def max(values):

  _max = values[0]

  for val in values:
      if val > _max:
          _max = val

  return _max

def min(values):

  _min = values[0]

  for val in values:
      if val < _min:
          _min = val

  return _min

```

We have a module with custom `max` and `min`
functions.

min\_max\_test.py

```

#!/usr/bin/python

import algo

def test_min():
    values = (2, 3, 1, 4, 6)

    val = algo.min(values)
    assert val == 1

def test_max():
    values = (2, 3, 1, 4, 6)

    val = algo.max(values)
    assert val == 6

```

The testing file `min_max_test.py` has a test
word in its name.

```

def test_min():
  values = (2, 3, 1, 4, 6)

  val = algo.min(values)
  assert val == 1

```

Also, the testing function `test_min` has a test word.
We use the `assert` keyword to test the value of the algorithm.

```

$ pytest min_max_test.py
================================================= test session starts =================================================
platform win32 -- Python 3.7.0, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: C:\Users\Jano\Documents\pyprogs\pytest
collected 2 items

min_max_test.py ..                                                                                               [100%]

============================================== 2 passed in 0.03 seconds ===============================================

```

This is the output. There were two tests and both have successfully passed.
A more verbose output is shown with `pytest -v min_max_test.py`.

## Pytest skip

With the skip decorator, we can skip the specified tests. There are multiple reasons
for skipping test; for instance, a database/online service is not available at
the moment or we skip Linux specific tests on Windows.

skipping.py

```

#!/usr/bin/python

import algo
import pytest

@pytest.mark.skip
def test_min():
    values = (2, 3, 1, 4, 6)

    val = algo.min(values)
    assert val == 1

def test_max():
    values = (2, 3, 1, 4, 6)

    val = algo.max(values)
    assert val == 6

```

In the example, the `test_min` is skipped.

```

$ pytest min_max_test.py
================================================= test session starts =================================================
platform win32 -- Python 3.7.0, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: C:\Users\Jano\Documents\pyprogs\pytest
collected 2 items

min_max_test.py s.                                                                                               [100%]

========================================= 1 passed, 1 skipped in 0.04 seconds =========================================

```

In the output following the test file name, s stands for skipped and . for passed.

## Pytest marking

We can use markers to organize tests into units.

marking.py

```

#!/usr/bin/python

# pytest -m a marking.py
# pytest -m b marking.py

import pytest

@pytest.mark.a
def test_a1():

    assert (1) == (1)

@pytest.mark.a
def test_a2():

    assert (1, 2) == (1, 2)

@pytest.mark.a
def test_a3():

    assert (1, 2, 3) == (1, 2, 3)

@pytest.mark.b
def test_b1():

    assert "falcon" == "fal" + "con"

@pytest.mark.b
def test_b2():

    assert "falcon" == f"fal{'con'}"

```

We have two groups of test identified by markers, a and b.
These units are run by `pytest -m a marking.py`
and `pytest -m b marking.py`.

## Pytest parameterized tests

With parameterized tests, we can add multiple values to
our assertions. We use the `@pytest.mark.parametrize`
marker.

parameterized.py

```

#!/usr/bin/python

import algo
import pytest

@pytest.mark.parametrize("data, expected", [((2, 3, 1, 4, 6), 1),
    ((5, -2, 0, 9, 12), -2), ((200, 100, 0, 300, 400), 0)])
def test_min(data, expected):

    val = algo.min(data)
    assert val == expected

@pytest.mark.parametrize("data, expected", [((2, 3, 1, 4, 6), 6),
    ((5, -2, 0, 9, 12), 12), ((200, 100, 0, 300, 400), 400)])
def test_max(data, expected):

    val = algo.max(data)
    assert val == expected

```

In the example, we test the two functions with multiple input data.

```

@pytest.mark.parametrize("data, expected", [((2, 3, 1, 4, 6), 1),
    ((5, -2, 0, 9, 12), -2), ((200, 100, 0, 300, 400), 0)])
def test_min(data, expected):

    val = algo.min(data)
    assert val == expected

```

We pass two values to the test function: the data and the exptected
value. In our case, we test the `min` function with
three data tuples.

```

$ pytest parameterized.py
================================================= test session starts =================================================
platform win32 -- Python 3.7.0, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: C:\Users\Jano\Documents\pyprogs\pytest
collected 6 items

parametrized.py ......                                                                                           [100%]

============================================== 6 passed in 0.03 seconds ===============================================

```

Pytest output informs that there were six runs.

## Pytest fixtures

Tests need to run against the background of a known set of objects. This set
of objects is called a *test fixture*.

algo.py

```

def sel_sort(data):

  if not isinstance(data, list):
      vals = list(data)
  else:
      vals = data

  size = len(vals)

  for i in range(0, size):

      for j in range(i+1, size):

          if vals[j] < vals[i]:
              _min = vals[j]
              vals[j] = vals[i]
              vals[i] = _min
  return vals
...

```

For this example, we add a selection sort algorithm to the `algo.py`
module.

fixtures.py

```

#!/usr/bin/python

import algo
import pytest

@pytest.fixture
def data():

    return [3, 2, 1, 5, -3, 2, 0, -2, 11, 9]

def test_sel_sort(data):

    sorted_vals = algo.sel_sort(data)
    assert sorted_vals == sorted(data)

```

We test the selection sort with a fixture.

```

@pytest.fixture
def data():

    return [3, 2, 1, 5, -3, 2, 0, -2, 11, 9]

```

Our test fixture simply returns some test data. Note that
we refer to this fixture by its name: `data`.

```

def test_sel_sort(data):

  sorted_vals = algo.sel_sort(data)
  assert sorted_vals == sorted(data)

```

In the `test_sel_sort` function, we pass the data
fixture as a function argument.

```

$ pytest fixtures.py
================================================= test session starts =================================================
platform win32 -- Python 3.7.0, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: C:\Users\Jano\Documents\pyprogs\pytest
collected 1 item

fixtures.py .                                                                                                    [100%]

============================================== 1 passed in 0.02 seconds ===============================================

```
## Pytest layouts

Python tests can be organized in various ways. Tests can be integrated in the
Python package or they can rest outside the package.

### Integrated tests

Next we show how to run tests within a Python package.

```

setup.py
utils
│   algo.py
│   srel.py
│   __init__.py
│
└───tests
        algo_test.py
        srel_test.py
        __init__.py

```

We have this package layout. The tests are located in the `tests`
subdirectory withing the package.

setup.py

```

#!/usr/bin/python

from setuptools import setup, find_packages

setup(name="utils", packages=find_packages())

```

This is the `setup.py`.

utils/algo.py

```

def sel_sort(data):

    if not isinstance(data, list):
        vals = list(data)
    else:
        vals = data

    size = len(vals)

    for i in range(0, size):

        for j in range(i+1, size):

            if vals[j] < vals[i]:
                _min = vals[j]
                vals[j] = vals[i]
                vals[i] = _min
    return vals

def max(values):

    _max = values[0]

    for val in values:
        if val > _max:
            _max = val

    return _max

def min(values):

    _min = values[0]

    for val in values:
        if val < _min:
            _min = val

    return _min

```

This is the `algo.py` file.

utils/srel.py

```

def is_palindrome(val):

    return val == val[::-1]

```

We have another module, which contains a function to
test whether a word is a palindrome.

tests/algo\_test.py

```

#!/usr/bin/python

import utils.algo
import pytest

@pytest.fixture
def data():

    return [3, 2, 1, 5, -3, 2, 0, -2, 11, 9]

def test_sel_sort(data):

    sorted_vals = utils.algo.sel_sort(data)
    assert sorted_vals == sorted(data)

def test_min():
    values = (2, 3, 1, 4, 6)

    val = utils.algo.min(values)
    assert val == 1

def test_max():
    values = (2, 3, 1, 4, 6)

    val = utils.algo.max(values)
    assert val == 6

```

These are the tests for the `utils.algo` module. Notice
that we use full module names.

tests/srel\_test.py

```

#!/usr/bin/python

import utils.srel
import pytest

@pytest.mark.parametrize("word, expected", [('kayak', True),
    ('civic', True), ('forest', False)])
def test_palindrome(word, expected):

    val = utils.srel.is_palindrome(word)
    assert val == expected

```

This is a test for the `is_palindrome` function.

utils/\_\_init\_\_.py

```

```
utils/tests/\_\_init\_\_.py

```

```

Both `__init__.py` files are empty.

```

$ pytest --pyargs utils
================================================= test session starts =================================================
platform win32 -- Python 3.7.0, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: C:\Users\Jano\Documents\pyprogs\pytest\structure
collected 6 items

utils\tests\algo_test.py ...                                                                                     [ 50%]
utils\tests\srel_test.py ...                                                                                     [100%]

============================================== 6 passed in 0.06 seconds ===============================================

```

We run the tests with `pytest --pyargs utils` command.

### Tests outside the package

The next example shows an application source layout where the tests
are not integrated inside the package.

```

setup.py
src
└───utils
│       algo.py
│       srel.py
tests
    algo_test.py
    srel_test.py

```

In this layout, we have tests outside the source tree.
Notice that the `__init__.py` files are not required.

```
$ set PYTHONPATH=src
$ pytest
```

We set the `PYTHONPATH` and run pytest.

## Source

[Python pytest documentation](https://docs.pytest.org/en/8.0.x/)


