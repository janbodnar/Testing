# A mock example with Bun

Mocking in testing is a technique used to **simulate the behavior of real objects or components**  
in a controlled way, so you can test a specific piece of code in isolation.


Mocking involves creating **mock objects**—stand-ins for real dependencies like  
databases, APIs, or services—that behave in predictable ways during tests. This  
allows you to:  

- Focus on the **unit under test** without relying on external systems
- Simulate **edge cases** or **error conditions** that are hard to reproduce
- **Speed up** tests by avoiding slow or flaky dependencies

## Why Use Mocks?

| Scenario | Why Mocking Helps |
|---------|-------------------|
| Your code calls an external API | Avoids network delays and failures |
| You interact with a database | Prevents data corruption and speeds up tests |
| You want to test error handling | Easily simulate exceptions or timeouts |
| You need to verify interactions | Check if a method was called with the right arguments |


## Types of Test Doubles (Mocks Are One)

| Type | Description |
|------|-------------|
| **Stub** | Returns predefined responses, doesn’t care how it’s used |
| **Mock** | Like a stub, but also **verifies interactions** (e.g., method calls) |
| **Fake** | A working but simplified implementation (e.g., in-memory DB) |
| **Spy** | Records how it was used, but doesn’t fail the test if expectations aren’t met |


## Example (JavaScript with Jest)

```js
const sendEmail = require('./emailService');

test('sends welcome email', () => {
  const mockSend = jest.fn();
  sendEmail.send = mockSend;

  registerUser('jan@example.com');

  expect(mockSend).toHaveBeenCalledWith('jan@example.com', 'Welcome!');
});
```

Here, `sendEmail.send` is mocked so we can test `registerUser` without actually  
sending an email.


## Mocking fetch service

In the example below, we will mock the `fetch` service to simulate an API call.
It will fetch the latest blog posts from Symfony's blog, parse the HTML, and
extract the titles and first paragraphs of the posts. 

The mock version of the `fetch` service will return a predefined HTML response
instead of making a real HTTP request. 

```json
{
  "name": "bunjs-mock-example",
  "version": "1.0.0",
  "scripts": {
    "test": "bun test"
  },
  "dependencies": {
    "linkedom": "^0.18.11"
  }
}
```

We have one dependency: `linkedom`.

```js
// sut.js
import { parseHTML } from "linkedom";

export const fetchArticles = async () => {
  const response = await fetch("https://symfony.com/blog/");
  const html = await response.text();

  const { document } = parseHTML(html);

  // Select blog posts within <article class="content">
  const blogPosts = Array.from(
    document.querySelectorAll('article.content .blog-post.mb-4')
  ).slice(0, 5);

  // extract titles and first paragraphs
  // the titles in h2 tags inside <div class="ui-heading mb-2 mb-lg-0">
  // the paragraph is in <div class="ui-prose mb-2">

  return blogPosts.map(post => {
    // Try to find a title in <div class="ui-heading mb-2 mb-lg-0">
    const title = post.querySelector("div.ui-heading.mb-2.mb-lg-0 h2")?.textContent.trim() || "";
    // Get the first 5 paragraphs from <div class="ui-prose mb-2">
    const paragraph = post.querySelector("div.ui-prose.mb-2").textContent.trim();
    return { title, paragraph };
  });

};
```

The `fetchArticles` function fetches the blog posts from Symfony's blog,
parses the HTML, and extracts the titles and first paragraphs of the posts.

```js
// sut.test.js
import { test, expect } from "bun:test";

// Mock the global fetch function directly
globalThis.fetch = async (url) => {
  if (url === "https://symfony.com/blog/") {
    return new Response(`
      <article class="content">
        <div class="blog-post mb-4">
          <div class="ui-heading mb-2 mb-lg-0">
            <h2>June 30 – July 6, 2025 A Week of Symfony #966</h2>
          </div>
          <div class="ui-prose mb-2">
            <p>This week, development on the upcoming Symfony 8.0 version continued with the removal of deprecated features and the marking of several classes as final. In addition, we published two new case studies showcasing companies that use Symfony.</p>
          </div>
        </div>
        <div class="blog-post mb-4">
          <div class="ui-heading mb-2 mb-lg-0">
            <h2>Case study: Modernizing Audi France’s Digital Ecosystem with Symfony 6</h2>
          </div>
          <div class="ui-prose mb-2">
            <p>🚗 In the fast-paced automotive industry, performance and reliability are key!\r\nAudi teamed up with Wide Agency to modernize its lead management system with Symfony 6 — unlocking agility, security & scalability ✨</p>
          </div>
        </div>
        <div class="blog-post mb-4">
          <div class="ui-heading mb-2 mb-lg-0">
            <h2>Case study: A Long-Term Powerhouse Behind Vente-unique.com's E-Commerce Success (Zero Churn, All Wins!)</h2>
          </div>
          <div class="ui-prose mb-2">
            <p>From Symfony 1.0 to 6.4 — Vente-unique.com has powered its entire e-commerce platform with Symfony for over 15 years!\r\nDiscover how Symfony scaled with them from ERP to marketplace, handling 3M+ customers across 11 countries.</p>
          </div>
        </div>
        <div class="blog-post mb-4">
          <div class="ui-heading mb-2 mb-lg-0">
            <h2>June 23–29, 2025 A Week of Symfony #965</h2>
          </div>
          <div class="ui-prose mb-2">
            <p>This week, Symfony 6.4.23, 7.2.8 and 7.3.1 maintenance versions were released. Meanwhile, the upcoming Symfony 7.4 version continued adding new features such as better controller helpers, more precision in UUIDv7 values, and using PHP serialization instead of XML for dumping the container in debug/lint commands.</p>
          </div>
        </div>
        <div class="blog-post mb-4">
          <div class="ui-heading mb-2 mb-lg-0">
            <h2>Symfony 7.3.1 released</h2>
          </div>
          <div class="ui-prose mb-2">
            <p>Read release notes</p>
          </div>
        </div>
      </article>
    `, {
      status: 200,
      headers: { "Content-Type": "text/html" },
    });
  }
  return new Response("", { status: 404 });
};

// Import the system under test AFTER the mocks are set up
import { fetchArticles } from "./sut.js";

test("fetchArticles with mocked fetch", async () => {
  const result = await fetchArticles();
  expect(result).toEqual([
    {
      title: "June 30 – July 6, 2025 A Week of Symfony #966",
      paragraph: "This week, development on the upcoming Symfony 8.0 version continued with the removal of deprecated features and the marking of several classes as final. In addition, we published two new case studies showcasing companies that use Symfony."
    },
    {
      title: "Case study: Modernizing Audi France’s Digital Ecosystem with Symfony 6",
      paragraph: "🚗 In the fast-paced automotive industry, performance and reliability are key!\r\nAudi teamed up with Wide Agency to modernize its lead management system with Symfony 6 — unlocking agility, security & scalability ✨"
    },
    {
      title: "Case study: A Long-Term Powerhouse Behind Vente-unique.com's E-Commerce Success (Zero Churn, All Wins!)",
      paragraph: "From Symfony 1.0 to 6.4 — Vente-unique.com has powered its entire e-commerce platform with Symfony for over 15 years!\r\nDiscover how Symfony scaled with them from ERP to marketplace, handling 3M+ customers across 11 countries."
    },
    {
      title: "June 23–29, 2025 A Week of Symfony #965",
      paragraph: "This week, Symfony 6.4.23, 7.2.8 and 7.3.1 maintenance versions were released. Meanwhile, the upcoming Symfony 7.4 version continued adding new features such as better controller helpers, more precision in UUIDv7 values, and using PHP serialization instead of XML for dumping the container in debug/lint commands."
    },
    {
      title: "Symfony 7.3.1 released",
      paragraph: "Read release notes"
    }
  ]);
});
```

The test mocks the `fetch` function to return a predefined HTML response. It  
then imports the `fetchArticles` function and tests it against the expected  
output.


```js
// app.js
import { fetchArticles } from "./sut.js";

(async () => {
  const articles = await fetchArticles();
  console.log(JSON.stringify(articles, null, 2));
})();
```

The `app.js` file imports the `fetchArticles` function and logs the fetched  
articles to the console. 

