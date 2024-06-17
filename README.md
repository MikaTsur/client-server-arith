# Simple Arithmetic Client-Server Application

This project implements a simple client-server system using two Python processes to perform basic arithmetic operations. The client sends two numbers and an arithmetic operation to the server, which performs the operation and returns the result to the client.

## Repository

You can find the project repository on GitHub: [client-server-arith](https://github.com/MikaTsur/client-server-arith)

## Requirements

- Python 3.x

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/MikaTsur/client-server-arith.git
    cd client-server-arith
    ```

2. (Optional) Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

### Start the Server

1. Open a terminal and navigate to the project directory.
2. Run the server:
    ```sh
    python server.py
    ```

### Start the Client

1. Open another terminal and navigate to the project directory.
2. Run the client:
    ```sh
    python client.py
    ```

### Perform Operations

1. Follow the prompts in the client terminal to enter two numbers and an arithmetic operation (`add`, `subtract`, `multiply`, `divide`).
2. The server will perform the operation and return the result, which will be displayed by the client.

### Shut Down the Server

1. Go to the terminal where the server is running.
2. Press `Ctrl+C` to gracefully shut down the server.

## Logging

Both the client and the server have independent logging mechanisms. Logs are stored in `client.log` and `server.log` respectively. Each major function/method is logged with "Enter" and "Exit" records.

## Files

- `server.py`: Server-side implementation that performs arithmetic operations.
- `client.py`: Client-side implementation that interacts with the user and communicates with the server.
- `utils.py`: Utility functions, including logger setup.
- `requirements.txt`: Project dependencies.

## Example

```sh
# Start the server
$ python server.py
2024-06-17 12:00:00 - server_logger - INFO - ---- Server Start ----
2024-06-17 12:00:10 - server_logger - INFO - Server listening on port 65432

# Start the client
$ python client.py
Enter the first number: 10
Enter the second number: 5
Enter the operation (add, subtract, multiply, divide): add
The result is: 15.0000000000
Do you want to perform another operation? (yes/no): no

# Shut down the server (press Ctrl+C in the server terminal)
2024-06-17 12:01:00 - server_logger - INFO - ---- Server Shutdown ----
