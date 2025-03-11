# Python `unittest` 

## Introduction to `unittest`

The `unittest` module is Python's built-in framework for writing and executing  
unit tests, inspired by JUnit from the Java ecosystem. It enables developers to  
verify that individual components (functions, methods, or classes) of their code  
work as intended. Unit testing is a cornerstone of reliable software  
development, helping you catch bugs early, validate functionality, and ensure  
maintainability.  

### Key Concepts in `unittest`

1. **Test Case**: The smallest unit of testing, typically validating a specific  
   behavior or output for a given input. Test cases are defined by subclassing  
   `unittest.TestCase`.

2. **Test Fixture**: The setup and teardown logic required for tests, such as  
   initializing resources (e.g., files, databases) before tests run and cleaning  
   up afterward.  

3. **Test Suite**: A collection of test cases or other test suites, allowing you  
   to group related tests for execution.  
  
4. **Test Runner**: The mechanism that executes tests and reports results, such  
   as pass/fail counts and error details.  

5. **Assertions**: Methods like `assertEqual`, `assertTrue`, `assertRaises`,  
   etc., used to check if the code behaves as expected. A failed assertion marks  
   the test as failed.  

---

## Setting Up `unittest`

To get started, import `unittest` and create a test class by subclassing  
`unittest.TestCase`. Test methods must start with `test_` to be recognized by  
the test runner.  

```python
import unittest

class MyTestCase(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
```

Run the tests from the command line:

```bash
python -m unittest <filename>.py
```

For verbose output (showing test names and results):

```bash
python -m unittest <filename>.py -v
```

---

## Practical Examples of `unittest`

Below are 15 practical examples showcasing `unittest` in  
various scenarios, from basic functions to advanced features.  

### Example 1: Testing a Simple Function

Test a basic addition function with multiple cases.

```python
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_mixed_numbers(self):
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
```

### Example 2: Testing String Methods

Verify built-in string methods with positive and negative tests.

```python
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('hello'.upper(), 'HELLO')

    def test_isupper(self):
        self.assertTrue('HELLO'.isupper())
        self.assertFalse('Hello'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)  # split() expects a string, not an integer

if __name__ == '__main__':
    unittest.main()
```

### Example 3: Testing List Methods

Test list manipulation methods for correctness.

```python
import unittest

class TestListMethods(unittest.TestCase):
    def test_append(self):
        my_list = [1, 2, 3]
        my_list.append(4)
        self.assertEqual(my_list, [1, 2, 3, 4])

    def test_pop(self):
        my_list = [1, 2, 3]
        popped_value = my_list.pop()
        self.assertEqual(popped_value, 3)
        self.assertEqual(my_list, [1, 2])

if __name__ == '__main__':
    unittest.main()
```

### Example 4: Testing Exceptions

Ensure a function raises exceptions as expected.

```python
import unittest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestDivideFunction(unittest.TestCase):
    def test_divide_valid(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
```

### Example 5: Using `setUp` and `tearDown`

Simulate a resource (e.g., a database) with setup and teardown.

```python
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Simulate opening a database connection
        self.database = []

    def tearDown(self):
        # Simulate closing the connection
        self.database = None

    def test_insert(self):
        self.database.append('data')
        self.assertIn('data', self.database)

    def test_delete(self):
        self.database.append('data')
        self.database.remove('data')
        self.assertNotIn('data', self.database)

if __name__ == '__main__':
    unittest.main()
```

### Example 6: Testing a Class

Test methods of a simple `Calculator` class.

```python
import unittest

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

if __name__ == '__main__':
    unittest.main()
```

### Example 7: Skipping Tests

Demonstrate how to skip tests conditionally or unconditionally.

```python
import unittest

class TestSkipExample(unittest.TestCase):
    @unittest.skip("Skipping this test for demonstration")
    def test_skip(self):
        self.fail("This test should be skipped")

    @unittest.skipIf(2 > 1, "Skipping because condition is true")
    def test_skip_if(self):
        self.assertEqual(1, 2)  # Would fail if not skipped

    def test_normal(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
```

### Example 8: Testing with `assertAlmostEqual`

Handle floating-point arithmetic precision issues.

```python
import unittest

class TestFloatingPoint(unittest.TestCase):
    def test_almost_equal(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)  # Accounts for float precision

    def test_not_almost_equal(self):
        self.assertNotAlmostEqual(0.1 + 0.2, 0.4, places=7)

if __name__ == '__main__':
    unittest.main()
```

### Example 9: Testing with `assertRaises`

Verify that exceptions are raised as expected.

```python
import unittest

def raise_exception():
    raise ValueError("An error occurred")

class TestException(unittest.TestCase):
    def test_raise_exception(self):
        with self.assertRaises(ValueError) as context:
            raise_exception()
        self.assertEqual(str(context.exception), "An error occurred")

if __name__ == '__main__':
    unittest.main()
```

### Example 10: Using Test Suites

Manually create and run a custom test suite.

```python
import unittest

class TestSuiteExample1(unittest.TestCase):
    def test_case1(self):
        self.assertEqual(1, 1)

class TestSuiteExample2(unittest.TestCase):
    def test_case2(self):
        self.assertEqual(2, 2)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSuiteExample1('test_case1'))
    suite.addTest(TestSuiteExample2('test_case2'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
```

### Example 11: Testing Dictionary Operations

Test dictionary methods and edge cases.

```python
import unittest

class TestDictionaryMethods(unittest.TestCase):
    def test_get(self):
        my_dict = {'a': 1, 'b': 2}
        self.assertEqual(my_dict.get('a'), 1)
        self.assertIsNone(my_dict.get('c'))  # Non-existent key returns None

    def test_update(self):
        my_dict = {'a': 1}
        my_dict.update({'b': 2})
        self.assertEqual(my_dict, {'a': 1, 'b': 2})

if __name__ == '__main__':
    unittest.main()
```

### Example 12: Testing File Operations

Simulate file operations with a temporary file.

```python
import unittest
import os

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.filename = "temp_test.txt"
        with open(self.filename, 'w') as f:
            f.write("Hello, world!")

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_read_file(self):
        with open(self.filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, "Hello, world!")

if __name__ == '__main__':
    unittest.main()
```

### Example 13: Testing Mocking with `unittest.mock`

Use mocking to isolate dependencies.

```python
import unittest
from unittest.mock import Mock

def fetch_data(api):
    return api.get_data()

class TestMocking(unittest.TestCase):
    def test_fetch_data(self):
        # Create a mock API object
        mock_api = Mock()
        mock_api.get_data.return_value = "mocked data"
        
        result = fetch_data(mock_api)
        self.assertEqual(result, "mocked data")
        mock_api.get_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

### Example 14: Testing Type Checking

Ensure functions handle input types correctly.

```python
import unittest

def multiply(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numbers")
    return a * b

class TestTypeChecking(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            multiply("2", 3)

if __name__ == '__main__':
    unittest.main()
```

### Example 15: Testing Edge Cases

Test a function with boundary conditions.

```python
import unittest

def clamp(value, min_val, max_val):
    """Clamp value between min_val and max_val."""
    return max(min_val, min(max_val, value))

class TestClampFunction(unittest.TestCase):
    def test_within_range(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_below_range(self):
        self.assertEqual(clamp(-1, 0, 10), 0)

    def test_above_range(self):
        self.assertEqual(clamp(15, 0, 10), 10)

if __name__ == '__main__':
    unittest.main()
```

## Testing sorting algorithms

The `sorting_algos.py` file:  

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def selection_sort(arr, ascending=True):
    n = len(arr)
    for i in range(n):
        idx = i
        for j in range(i + 1, n):
            if (ascending and arr[j] < arr[idx]) or (not ascending and arr[j] > arr[idx]):
                idx = j
        arr[i], arr[idx] = arr[idx], arr[i]
    return arr
```

The `test_algos.py` file:  

```python
import unittest
from sorting_algos import bubble_sort, selection_sort


class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with various input arrays."""
        self.unsorted_list = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_asc_list = [11, 12, 22, 25, 34, 64, 90]
        self.sorted_desc_list = [90, 64, 34, 25, 22, 12, 11]
        self.empty_list = []
        self.single_element_list = [42]
        self.duplicates_list = [5, 2, 8, 5, 1, 9, 2]

    def test_bubble_sort_unsorted(self):
        """Test bubble_sort with an unsorted list."""
        arr = self.unsorted_list.copy()  # Use copy to preserve original fixture
        bubble_sort(arr)
        self.assertEqual(arr, self.sorted_asc_list)

    def test_bubble_sort_already_sorted(self):
        """Test bubble_sort with an already sorted list."""
        arr = self.sorted_asc_list.copy()
        bubble_sort(arr)
        self.assertEqual(arr, self.sorted_asc_list)

    def test_bubble_sort_empty(self):
        """Test bubble_sort with an empty list."""
        arr = self.empty_list.copy()
        bubble_sort(arr)
        self.assertEqual(arr, self.empty_list)

    def test_bubble_sort_single_element(self):
        """Test bubble_sort with a single-element list."""
        arr = self.single_element_list.copy()
        bubble_sort(arr)
        self.assertEqual(arr, self.single_element_list)

    def test_bubble_sort_duplicates(self):
        """Test bubble_sort with a list containing duplicates."""
        arr = self.duplicates_list.copy()
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 2, 5, 5, 8, 9])

    def test_selection_sort_ascending_unsorted(self):
        """Test selection_sort with an unsorted list in ascending order."""
        arr = self.unsorted_list.copy()
        result = selection_sort(arr, ascending=True)
        self.assertEqual(result, self.sorted_asc_list)

    def test_selection_sort_descending_unsorted(self):
        """Test selection_sort with an unsorted list in descending order."""
        arr = self.unsorted_list.copy()
        result = selection_sort(arr, ascending=False)
        self.assertEqual(result, self.sorted_desc_list)

    def test_selection_sort_ascending_sorted(self):
        """Test selection_sort with an already sorted list in ascending order."""
        arr = self.sorted_asc_list.copy()
        result = selection_sort(arr, ascending=True)
        self.assertEqual(result, self.sorted_asc_list)

    def test_selection_sort_descending_sorted(self):
        """Test selection_sort with an already sorted list in descending order."""
        arr = self.sorted_desc_list.copy()
        result = selection_sort(arr, ascending=False)
        self.assertEqual(result, self.sorted_desc_list)

    def test_selection_sort_empty(self):
        """Test selection_sort with an empty list."""
        arr = self.empty_list.copy()
        result = selection_sort(arr, ascending=True)
        self.assertEqual(result, self.empty_list)

    def test_selection_sort_single_element(self):
        """Test selection_sort with a single-element list."""
        arr = self.single_element_list.copy()
        result = selection_sort(arr, ascending=True)
        self.assertEqual(result, self.single_element_list)

    def test_selection_sort_duplicates_ascending(self):
        """Test selection_sort with duplicates in ascending order."""
        arr = self.duplicates_list.copy()
        result = selection_sort(arr, ascending=True)
        self.assertEqual(result, [1, 2, 2, 5, 5, 8, 9])

    def test_selection_sort_duplicates_descending(self):
        """Test selection_sort with duplicates in descending order."""
        arr = self.duplicates_list.copy()
        result = selection_sort(arr, ascending=False)
        self.assertEqual(result, [9, 8, 5, 5, 2, 2, 1])


if __name__ == '__main__':
    unittest.main()
```



---

## Tips for Effective Unit Testing

- **Test One Thing at a Time**: Each test should focus on a single behavior or condition.
- **Use Descriptive Names**: Method names like `test_add_positive_numbers` make failures easier to diagnose.
- **Cover Edge Cases**: Test boundaries, exceptions, and unusual inputs.
- **Keep Tests Independent**: Avoid dependencies between tests using `setUp` and `tearDown`.
- **Run Tests Frequently**: Integrate testing into your workflow to catch issues early.

---

## Conclusion

The `unittest` module provides a versatile and powerful framework for testing  
Python code. With the 15 examples above, you’ve seen how to test functions,  
classes, exceptions, and more, including advanced features like mocking and test  
suites. Start incorporating unit tests into your projects to improve code  
quality and confidence.  

