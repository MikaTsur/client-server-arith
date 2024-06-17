# client.py
import socket
import pickle
from utils import setup_logger


class Client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.logger = setup_logger('client_logger', 'client.log')

    def get_user_input(self):
        self.logger.info('---- Function get_user_input Enter ----')
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Enter the operation (add, subtract, multiply, divide): ")
        self.logger.info('---- Function get_user_input Exit ----')
        return {'num1': num1, 'num2': num2, 'operation': operation}

    def send_request(self, user_input):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(pickle.dumps(user_input))
            self.logger.info(f'Sent request: {user_input}')

            data = s.recv(1024)
            result = pickle.loads(data)
            self.logger.info(f'Received result: {result}')
            print(f"The result is: {result}")

    def run(self):
        self.logger.info('---- Client Start ----')
        user_input = self.get_user_input()
        self.send_request(user_input)
        self.logger.info('---- Client Stop ----')


if __name__ == '__main__':
    client = Client()
    client.run()