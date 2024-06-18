import http.client
import json
from utils import setup_logger


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.logger = setup_logger('client_logger', 'client.log')

    def get_user_input(self):
        while True:
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                operation = input("Enter the operation (add, subtract, multiply, divide): ").strip().lower()
                if operation not in ('add', 'subtract', 'multiply', 'divide'):
                    raise ValueError("Invalid operation")
                return {'num1': num1, 'num2': num2, 'operation': operation}
            except ValueError as e:
                print(f"Invalid input: {e}")

    def send_request(self, user_input):
        conn = http.client.HTTPConnection(self.host, self.port)
        headers = {'Content-type': 'application/json'}

        try:
            conn.request('POST', '/', json.dumps(user_input), headers)
            response = conn.getresponse()
            response_data = json.loads(response.read().decode())

            if 'error' in response_data:
                self.logger.error(response_data['error'])
                print(response_data['error'])
            else:
                result = response_data['result']
                self.logger.info(f'Received result: {result:.10f}')
                print(f"The result is: {result:.10f}")

        except Exception as e:
            self.logger.error(f'Error: {e}')
            print(f"Error: {e}")
        finally:
            conn.close()

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
