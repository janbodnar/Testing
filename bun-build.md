# Bun build 


## Simple test binary

The example creates a simple mock server with Bun and `data.json` file. 

The `data.json`:

```json
[
  { "name": "John Doe", "age": 30, "city": "New York" },
  { "name": "Jane Smith", "age": 25, "city": "London" },
  { "name": "Peter Jones", "age": 35, "city": "Paris" },
  { "name": "Susan Williams", "age": 28, "city": "Sydney" },
  { "name": "Michael Brown", "age": 42, "city": "Tokyo" }
]
```

The `index.html` file uses `fetch` to get the data and display in HTML table.  

```html
<!DOCTYPE html>
<html>
<head>
  <title>Bun.js App</title>
</head>
<body>
  <h1>Data from JSON</h1>
  <table id="data-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Age</th>
        <th>City</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>

  <script>
    fetch('/data')
      .then(response => response.json())
      .then(data => {
        const tableBody = document.querySelector('#data-table tbody');
        data.forEach(item => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.age}</td>
            <td>${item.city}</td>
          `;
          tableBody.appendChild(row);
        });
      });
  </script>
</body>
</html>
```

The `index.ts` file starts a server that sends either an HTML file or JSON data. 

```ts
import { serve } from 'bun';
import data from './data.json';

const server = serve({
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === '/') {
      return new Response(Bun.file('index.html'));
    } else if (url.pathname === '/data') {
      return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json' },
      });
    } 
    return new Response('Not Found', { status: 404 });
  },
});

console.log(`Application started at http://${server.hostname}:${server.port}`);
```

```
xh :3000/data | jq
```

Using `xh` to get the data and jq to process it.  

```
xh :3000/data | jq -r ".[0:3]"
[
  {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
  },
  {
    "name": "Jane Smith",
    "age": 25,
    "city": "London"
  },
  {
    "name": "Peter Jones",
    "age": 35,
    "city": "Paris"
  }
]
```

This displays first three rows.  


```
nu -c "xh :3000/data | from json | first 3 | select name age city"
╭───┬─────────────┬─────┬──────────╮
│ # │    name     │ age │   city   │
├───┼─────────────┼─────┼──────────┤
│ 0 │ John Doe    │  30 │ New York │
│ 1 │ Jane Smith  │  25 │ London   │
│ 2 │ Peter Jones │  35 │ Paris    │
╰───┴─────────────┴─────┴──────────╯
```

Nushell can be used to display data in table format.  
