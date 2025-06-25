# Python gRPC & Insomnia

**gRPC** (short for *gRPC Remote Procedure Call*) is an open-source framework developed by Google that enables  
communication between distributed systems using a high-performance, language-agnostic protocol. It allows clients  
to call methods on a server as if they were local functions, making it ideal for microservices and real-time applications.

gRPC uses:

- **Protocol Buffers (Protobuf)** for efficient binary serialization
- **HTTP/2** as its transport protocol, enabling multiplexing and streaming

## Protobuf

Protocol Buffers is a language-neutral, platform-neutral, extensible mechanism for serializing structured data—developed  
by Google. Think of it as a more efficient alternative to JSON or XML, especially when performance and bandwidth matter. 

At its core, Protobuf lets you:

- Define data structures (called messages) in .proto files
- Automatically generate code in multiple languages (like Python, Go, Java, etc.)
- Serialize and deserialize data into a compact binary format


## Advantages of gRPC

- **High Performance:** Binary serialization and HTTP/2 make gRPC significantly faster and more efficient  
  than traditional REST APIs.
- **Streaming Support:** Supports client, server, and bidirectional streaming for real-time data exchange.  
- **Cross-language Compatibility:** Works across many languages like Go, Python, Java, C++, and more.  
- **Automatic Code Generation:** Protobuf definitions generate client and server code, reducing boilerplate.  
- **Strong Typing:** Protobuf enforces strict data contracts, reducing runtime errors.

## Disadvantages of gRPC

- **Limited Browser Support:** Browsers don’t natively support gRPC over HTTP/2, requiring workarounds like gRPC-Web.
- **Steeper Learning Curve:** Developers must learn Protobuf and gRPC-specific tooling.
- **Debugging Complexity:** Binary messages are not human-readable, making manual inspection harder.
- **Overhead for Simple Use Cases:** For basic CRUD APIs, REST might be simpler and more accessible.


In short, gRPC is a powerful tool for building fast, scalable APIs—especially when performance and real-time communication 
matter. 


## Python example 

The example creates a simple gRPC demo in Python. 

The `requirements.txt` file: 

```
grpcio==1.62.2 
grpcio-tools==1.62.2
```


```proto
syntax = "proto3";

package user;

service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
  rpc ListUsers (Empty) returns (UserListResponse);
  rpc CreateUser (CreateUserRequest) returns (UserResponse);
}

message UserRequest {
  int32 id = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message UserResponse {
  int32 id = 1;
  string name = 2;
  string email = 3;
}

message UserListResponse {
  repeated UserResponse users = 1;
}

message Empty {}
```

This user.proto file defines a gRPC service called `UserService` for managing user data. The service  
provides three RPC methods: GetUser retrieves a user by their ID, `ListUsers` returns all users,  
and `CreateUser` allows the creation of a new user with a name and email. Each method uses specific request  
and response message types to structure the data exchanged between client and server.  

The file also defines several message types: `UserRequest` (for specifying a user ID), `CreateUserRequest`  
(for providing a name and email when creating a user), `UserResponse` (representing a user's details),  
`UserListResponse` (a list of users), and an empty message type Empty (used when no input is needed).  
This structure enables efficient and type-safe communication for basic user management operations over gRPC. 


The `src\grpc_server.py` file: 

```python
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

# Mock in-memory user store
users = [
    user_pb2.UserResponse(id=1, name="Alice", email="alice@example.com"),
    user_pb2.UserResponse(id=2, name="Bob", email="bob@example.com"),
]
next_id = 3

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = next((u for u in users if u.id == request.id), None)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.UserResponse()
        return user

    def ListUsers(self, request, context):
        return user_pb2.UserListResponse(users=users)

    def CreateUser(self, request, context):
        global next_id
        if not request.name or not request.email:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Name and email are required")
            return user_pb2.UserResponse()
        new_user = user_pb2.UserResponse(id=next_id, name=request.name, email=request.email)
        users.append(new_user)
        next_id += 1
        return new_user

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server running at localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

The `src\grpc_client.py` file: 

```python
import grpc
import user_pb2
import user_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        # Test GetUser
        print("Getting user with ID 1:")
        try:
            response = stub.GetUser(user_pb2.UserRequest(id=1))
            print(f"User: id={response.id}, name={response.name}, email={response.email}")
        except grpc.RpcError as e:
            print(f"Error: {e.details()}")

        # Test ListUsers
        print("\nListing all users:")
        try:
            response = stub.ListUsers(user_pb2.Empty())
            for user in response.users:
                print(f"User: id={user.id}, name={user.name}, email={user.email}")
        except grpc.RpcError as e:
            print(f"Error: {e.details()}")

        # Test CreateUser
        print("\nCreating a new user:")
        try:
            response = stub.CreateUser(user_pb2.CreateUserRequest(name="Charlie", email="charlie@example.com"))
            print(f"Created user: id={response.id}, name={response.name}, email={response.email}")
        except grpc.RpcError as e:
            print(f"Error: {e.details()}")

if __name__ == "__main__":
    run()
```

Generate gRPC code from the proto file:

```
python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/user.proto
```

The Insomnia test file:

```yaml
type: collection.insomnia.rest/5.0
name: gRPC collection
meta:
  id: wrk_41a49fa14e7a40d086277ecabcec3615
  created: 1750850528192
  modified: 1750850703243
  description: ""
collection:
  - url: localhost:50051
    name: Get User by Id
    meta:
      id: greq_d8ff6f37c91f438abd62fc1f910624df
      created: 1750850722370
      modified: 1750851936784
      isPrivate: false
      sortKey: -1750850722370
      description: ""
    body:
      text: |-
        {
        	"id": 1
        }
    metadata:
      - id: pair_5a85dbe47e65459b9916fcf2395d094f
        name: ""
        value: ""
        description: ""
        disabled: false
      - id: pair_437e20f677e94ea48442313db3c15360
        name: ""
        value: ""
        description: ""
        disabled: false
    protoFileId: pf_3a1d3bd500e44890a703b667485f1eee
    protoMethodName: /user.UserService/GetUser
    reflectionApi:
      enabled: false
      url: https://buf.build
      apiKey: ""
      module: buf.build/connectrpc/eliza
  - url: localhost:50051
    name: Get All Users
    meta:
      id: greq_956fc583105c407aa08e398ed8f0ece9
      created: 1750851947364
      modified: 1750851975682
      isPrivate: false
      sortKey: -1750850722320
      description: ""
    body:
      text: |-
        {
        	"id": 1
        }
    metadata:
      - id: pair_5a85dbe47e65459b9916fcf2395d094f
        name: ""
        value: ""
        description: ""
        disabled: false
      - id: pair_437e20f677e94ea48442313db3c15360
        name: ""
        value: ""
        description: ""
        disabled: false
    protoFileId: pf_3a1d3bd500e44890a703b667485f1eee
    protoMethodName: /user.UserService/ListUsers
    reflectionApi:
      enabled: false
      url: https://buf.build
      apiKey: ""
      module: buf.build/connectrpc/eliza
  - url: localhost:50051
    name: Create New User
    meta:
      id: greq_a93a8cc3bbab4e7eb7ae49a8cf4067c9
      created: 1750852033481
      modified: 1750852050699
      isPrivate: false
      sortKey: -1750850722270
      description: ""
    body:
      text: |-
        {
          "name": "Jan Novak",
          "email": "jan.novak@example.com"
        }
    metadata:
      - id: pair_5a85dbe47e65459b9916fcf2395d094f
        name: ""
        value: ""
        description: ""
        disabled: false
      - id: pair_437e20f677e94ea48442313db3c15360
        name: ""
        value: ""
        description: ""
        disabled: false
    protoFileId: pf_3a1d3bd500e44890a703b667485f1eee
    protoMethodName: /user.UserService/CreateUser
    reflectionApi:
      enabled: false
      url: https://buf.build
      apiKey: ""
      module: buf.build/connectrpc/eliza
cookieJar:
  name: Default Jar
  meta:
    id: jar_db91d95c3c40d831a691e6f8aa6a46c2d4707c90
    created: 1750850528213
    modified: 1750850528213
environments:
  name: Base Environment
  meta:
    id: env_db91d95c3c40d831a691e6f8aa6a46c2d4707c90
    created: 1750850528210
    modified: 1750850528210
    isPrivate: false
```


