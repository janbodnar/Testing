# Bruno

Bruno is an open-source API testing tool designed to be fast, Git-friendly, and  
offline-first. Unlike traditional API clients like Postman, Bruno stores  
collections as plain text files, making them easy to version-control with Git.  
This approach allows developers to collaborate seamlessly without relying on  
cloud-based storage. Bruno also supports scripting, assertions, and automated  
testing, enabling users to validate API responses efficiently.   

Bruno prioritizes privacy and performance, ensuring that API requests and  
responses remain local to the user's machine. It features a modern UI, powerful  
testing capabilities, and support for multiple environments, making it a  
versatile tool for API development. With its lightweight design and focus on  
developer experience, Bruno is an excellent choice for teams looking for a  
secure, efficient, and Git-integrated API client.  

## Simple example


```python
from flask import Flask, make_response, jsonify
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Home page</p>"


@app.route("/hello/<name>")
def hello(name):
    msg = f'Hello {escape(name)}!'
    return make_response(msg, 200)


@app.route("/current-time")
def current_time():
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"current-time": now}) # Return current time as JSON
```

## Bruno scripts


```json
{
  "name": "simple",
  "version": "1",
  "items": [
    {
      "type": "http",
      "name": "current-time",
      "filename": "current-time.bru",
      "seq": 4,
      "request": {
        "url": "http://localhost:5000/current-time",
        "method": "GET",
        "headers": [],
        "params": [],
        "body": {
          "mode": "none",
          "formUrlEncoded": [],
          "multipartForm": [],
          "file": []
        },
        "script": {},
        "vars": {},
        "assertions": [
          {
            "name": "res.status",
            "value": "eq 200",
            "enabled": true,
            "uid": "vg81MV7Y1BKTQ9SOjhgAb"
          },
          {
            "name": "res.body['current-time']",
            "value": "matches ^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$",
            "enabled": true,
            "uid": "lo5PSaPCaR5zd6OEJ3k8r"
          },
          {
            "name": "res.headers['content-type']",
            "value": "eq application/json",
            "enabled": true,
            "uid": "B61EqdAOCHWqUgSWY5wqu"
          }
        ],
        "tests": "",
        "docs": "",
        "auth": {
          "mode": "inherit"
        }
      }
    },
    {
      "type": "http",
      "name": "hello",
      "filename": "hello.bru",
      "seq": 2,
      "request": {
        "url": "http://localhost:5000/hello/{{NAME}}",
        "method": "GET",
        "headers": [],
        "params": [],
        "body": {
          "mode": "none",
          "formUrlEncoded": [],
          "multipartForm": [],
          "file": []
        },
        "script": {},
        "vars": {},
        "assertions": [
          {
            "name": "res.status",
            "value": "eq 200",
            "enabled": true,
            "uid": "UyNczc2g2uRJ2c17G4aqO"
          },
          {
            "name": "res.body",
            "value": "contains Hello {{NAME}}",
            "enabled": true,
            "uid": "xN3oFMCXhttu64dbTi8B3"
          },
          {
            "name": "res.headers['content-type']",
            "value": "eq text/html; charset=utf-8",
            "enabled": true,
            "uid": "5nYc8MUSvpZRcnB7T8xWP"
          }
        ],
        "tests": "",
        "docs": "",
        "auth": {
          "mode": "inherit"
        }
      }
    },
    {
      "type": "http",
      "name": "home",
      "filename": "home.bru",
      "seq": 1,
      "request": {
        "url": "http://localhost:5000/",
        "method": "GET",
        "headers": [],
        "params": [],
        "body": {
          "mode": "none",
          "formUrlEncoded": [],
          "multipartForm": [],
          "file": []
        },
        "script": {},
        "vars": {},
        "assertions": [
          {
            "name": "res.status",
            "value": "eq 200",
            "enabled": true,
            "uid": "JhraRijFFnAjkFHqa2G1d"
          },
          {
            "name": "res.body",
            "value": "contains Home page",
            "enabled": true,
            "uid": "gZ1bCwOMWXzksQwj5wNVw"
          }
        ],
        "tests": "",
        "docs": "",
        "auth": {
          "mode": "inherit"
        }
      }
    }
  ],
  "activeEnvironmentUid": "Euuur4eL1nEMeTypMqxAl",
  "environments": [
    {
      "variables": [
        {
          "name": "NAME",
          "value": "Robert",
          "enabled": true,
          "secret": false,
          "type": "text"
        }
      ],
      "name": "simple"
    }
  ],
  "brunoConfig": {
    "version": "1",
    "name": "simple",
    "type": "collection",
    "ignore": [
      "node_modules",
      ".git"
    ],
    "size": 0.000762939453125,
    "filesCount": 5
  }
}
```


