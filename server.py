#server.py
import socket
import pickle
import threading
import signal
import sys
from utils import setup_logger
from abc import ABC, abstractmethod

# Setup logger
logger = setup_logger('server_logger', 'server.log')

class AbstractOperation(ABC):
    @abstractmethod
    def operate(self, num1, num2):
        pass

class AddOperation(AbstractOperation):
    def operate(self, num1, num2):
        return num1 + num2

class SubtractOperation(AbstractOperation):
    def operate(self, num1, num2):
        return num1 - num2

class MultiplyOperation(AbstractOperation):
    def operate(self, num1, num2):
        return num1 * num2

class DivideOperation(AbstractOperation):
    def operate(self, num1, num2):
        if num2 == 0:
            raise ValueError("Division by zero is not allowed")
        return num1 / num2

def get_operation(operation):
    if operation == 'add':
        return AddOperation()
    elif operation == 'subtract':
        return SubtractOperation()
    elif operation == 'multiply':
        return MultiplyOperation()
    elif operation == 'divide':
        return DivideOperation()
    else:
        raise ValueError("Unsupported operation")

def handle_client_request(conn):
    try:
        data = conn.recv(1024)
        if data:
            request = pickle.loads(data)
            logger.info(f'Received request: {request}')
            operation = get_operation(request['operation'])
            result = operation.operate(request['num1'], request['num2'])
            conn.sendall(pickle.dumps(round(result, 10)))  # Round result to 10 decimal places
            logger.info(f'Sent result: {result}')
    except Exception as e:
        logger.error(f'Error handling client request: {e}')
        conn.sendall(pickle.dumps(f'Error: {e}'))

def handle_client(conn, addr):
    with conn:
        logger.info(f'Connected by {addr}')
        handle_client_request(conn)

def signal_handler(sig, frame):
    logger.info('---- Server Shutdown ----')
    global running
    running = False

def main():
    global s, running
    logger.info('---- Server Start ----')
    signal.signal(signal.SIGINT, signal_handler)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 65432))
    s.listen()
    logger.info('Server listening on port 65432')

    running = True
    while running:
        try:
            s.settimeout(1)  # Set a timeout for the accept method
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            logger.error(f'Error accepting connections: {e}')
            break

    s.close()
    logger.info('---- Server Stop ----')

if __name__ == '__main__':
    main()
