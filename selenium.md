# Selenium

Selenium is an open-source tool used for automating web browsers. It provides a suite of tools and libraries  
that allow developers to interact with web elements, perform browser-based tests, and automate repetitive  
web tasks. Selenium supports multiple programming languages such as Python, Java, and C#, and works with various  
browsers like Chrome, Firefox, and Edge. Its primary components include WebDriver,  
IDE (Integrated Development Environment), and Grid, which facilitate browser automation, recording,  
and parallel test execution.

## Get the driver 

Choose the driver that matches the version of your chrome.  

`https://googlechromelabs.github.io/chrome-for-testing/#stable`

Download the driver and place it into a directory that is located in the system environment `PATH`.


## Headless mode

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Use new Headless mode
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.example.com")
    print(driver.title)
finally:
    driver.quit()
```

## Unittest example

```python
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class WebCodeTest(unittest.TestCase):

    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")

        self.driver = webdriver.Chrome(options=opts)

    def test_title(self):

        self.driver.get("https://webcode.me")
        print(self.driver.title)
        self.assertIn("My html page", self.driver.title)

    def test_paragraphs(self):

        self.driver.get("https://webcode.me")

        els = self.driver.find_elements(By.TAG_NAME, "p")

        self.assertIn('Today is a beautiful day', els[0].text)
        self.assertIn('Hello there', els[1].text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
```
