# Python Playwright

In this article we show how to automate browsers in Python with Playwright.

## Playwright

Playwright is a cross-browser automation library created by Microsoft. It supports all modern  
rendering engines including Chromium, WebKit, and Firefox.

Playwright can be used in Node, Python, .NET, and JVM.  

Playwright allows you to use a browser in a headless mode (the default mode), which works without  
the UI. This is great for scripting.

```sh
$ pip install --upgrade pip
$ pip install playwright
$ playwright install
```

We install Playwright library and the browser drivers.

## Python Playwright get title

In the first example, we get the title of a web page.

```python
#!/usr/bin/python

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:

    webkit = playwright.webkit

    browser = webkit.launch()
    page = browser.new_page()

    url = 'http://webcode.me'
    page.goto(url)

    title = page.title()
    print(title)

    browser.close()
```

The example retrieves and prints the title of a small webpage.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
...
```

We use Playwright in a synchronous manner.

```python
webkit = playwright.webkit
```

We use the Webkit driver.

```python
browser = webkit.launch()
page = browser.new_page()
```

We launch the browser and create a new page. The default browser mode is headless; that is, no UI is shown.

```python
url = 'http://webcode.me'
page.goto(url)
```

We navigate to the specified URL.

```python
title = page.title()
print(title)
```

We get the title and print it.

```sh
$ ./main.py
My html page
```

## Python Playwright create screenshot

In the following example, we create a screenshot of a web page.

```python
#!/usr/bin/python

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:

    webkit = playwright.webkit
    browser = webkit.launch()
    page = browser.new_page()

    url = 'http://webcode.me'
    page.goto(url)

    page.screenshot(path='shot.png')
    browser.close()
```

The screenshot is created with the `screenshot` function; the `path` attribute specifies the file name.

## Python Playwright async example

The next example is an asynchronous version of the previous one.

```python
#!/usr/bin/python

import asyncio

from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:

        webkit = playwright.webkit
        browser = await webkit.launch()
        page = await browser.new_page()

        url = 'http://webcode.me'
        await page.goto(url)
        await page.screenshot(path='shot.png')

        await browser.close()

asyncio.run(main())
```

For the asynchronous version, we use the `async/await` keywords and the `asyncio` module.

## Python Playwright set HTTP headers

With the `set_extra_http_headers` function, we can specify HTTP headers for the client.

```python
#!/usr/bin/python

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:

    webkit = playwright.webkit
    browser = webkit.launch()
    page = browser.new_page()

    page.set_extra_http_headers({"User-Agent": "Python program"})

    url = 'http://webcode.me/ua.php'
    page.goto(url)

    content = page.text_content('*')
    print(content)

    browser.close()
```

We set the `User-Agent` header to the request and navigate to the `http://webcode.me/ua.php` URL, which  
returns the `User-Agent` header back to the client.

```sh
$ ./main.py 
Python program
```

## Python Playwright click on element

In the next example, we click on the `button` element with `click`. After clicking on the button,  
a text message is displayed in the output div element.

```python
#!/usr/bin/python

import time
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:

    webkit = playwright.webkit
    browser = webkit.launch(headless=False)
    page = browser.new_page()

    url = 'http://webcode.me/click.html'
    page.goto(url)

    time.sleep(2)

    btn = page.locator('button');
    btn.click()

    output = page.locator('#output');
    print(output.text_content())

    time.sleep(1)

    browser.close()
```

The example starts the browser.

```python
browser = webkit.launch(headless=False)
```

To start the UI, we set the `headless` option to `False`.

```python
time.sleep(2)
```

We slow down the program a bit.

```python
btn = page.locator('button');
btn.click()
```

We locate the button element with `locator` and click on it with `click`.

```python
output = page.locator('#output');
print(output.text_content())
```

We locate the output element and get its text content.

```sh
$ ./main.py
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 ...
```

## Python Playwright locating elements

In the next example, we find elements with `locator`.

```python
#!/usr/bin/python

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:

    webkit = playwright.webkit
    browser = webkit.launch()
    page = browser.new_page()

    url = 'http://webcode.me/os.html'
    page.goto(url)

    els = page.locator('ul li').all();

    for e in els:
        print(e.text_content())

    browser.close()
```

The program finds all `li` tags and prints their content.

```sh
$ ./main.py
Solaris
FreeBSD
Debian
NetBSD
Windows
```

## Source

[Python Playwright documentation](https://playwright.dev/python/docs/intro)


## SHMU


```python
#!/usr/bin/python
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    webkit = playwright.webkit
    browser = webkit.launch(headless=False)
    page = browser.new_page()

    url = 'https://www.shmu.sk/sk/?page=1'
    page.goto(url)

    # Wait for the page to load
    page.wait_for_load_state('load')

    # Locate the div with id="first-level"
    div = page.locator('#first-level')

    # Narrow down to the li with class="hydro" inside that div
    li = div.locator('li.hydro')

    # Find the link (<a>) inside the li using get_by_role
    link = li.get_by_role("link")

    # Click the link
    link.click()

    # Wait for the page to load after clicking
    page.wait_for_load_state('load')

    # Take a screenshot of the entire page
    page.screenshot(path="screenshot.png")

    # Optionally, take a screenshot of just the link element
    # link.screenshot(path="link_screenshot.png")

    html_content = page.content()
    print(html_content)

    time.sleep(1)
    browser.close()








# #!/usr/bin/python

# import time
# from playwright.sync_api import sync_playwright
# import time


# with sync_playwright() as playwright:

#     webkit = playwright.webkit
#     browser = webkit.launch(headless=False)
#     page = browser.new_page()

#     url = 'https://www.shmu.sk/sk/?page=1'
#     page.goto(url)

#     time.sleep(2)

#     btn = page.get_by_role("hydro", name="Hydrologické spravodajstvo").check()
#     btn.wait_for()  # Ensure the button is visible and ready
#     btn.click()  # Click the button

#         # Step 3: Wait for navigation or content to load
#     page.wait_for_load_state('load')  # Wait for the page to load completely

#     html_content = page.content()  # Get the full HTML content of the page
#     print(html_content)


#     time.sleep(1)

#     browser.close()
```
