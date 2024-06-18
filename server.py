from http.server import BaseHTTPRequestHandler, HTTPServer
import json
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


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data.decode('utf-8'))

        logger.info(f'Received request: {request}')

        try:
            operation = get_operation(request['operation'])
            result = operation.operate(request['num1'], request['num2'])
            response = {'result': round(result, 10)}
        except Exception as e:
            response = {'error': str(e)}
            logger.error(f'Error handling request: {e}')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
        logger.info(f'Sent response: {response}')


def run(server_class=HTTPServer, handler_class=RequestHandler, host='127.0.0.1', port=65432):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    logger.info('Starting server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
