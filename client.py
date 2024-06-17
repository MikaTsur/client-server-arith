#client.py
import socket
import pickle
from utils import setup_logger


class Client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.logger = setup_logger('client_logger', 'client.log')

    def get_user_input(self):
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Enter the operation (add, subtract, multiply, divide): ")
        return {'num1': num1, 'num2': num2, 'operation': operation}

    def send_request(self, user_input):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                s.sendall(pickle.dumps(user_input))
                self.logger.info(f'Sent request: {user_input}')

                data = s.recv(1024)
                result = pickle.loads(data)
                self.logger.info(f'Received result: {result:.10f}')
                print(f"The result is: {result:.10f}")

            except EOFError:
                print("Error: Operation not allowed - Server did not send a valid response.")
            except Exception as e:
                print(f"Error: {e}")

    def run(self):
        self.logger.info('---- Client Start ----')
        while True:
            user_input = self.get_user_input()
            self.send_request(user_input)
            choice = input("Do you want to perform another operation? (yes/no): ")
            if choice.lower() != 'yes':
                break
        self.logger.info('---- Client Stop ----')


if __name__ == '__main__':
    client = Client()
    client.run()
