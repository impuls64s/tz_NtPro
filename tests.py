import unittest
from bank import parse_requets, validator


class Test_Bank(unittest.TestCase):

    def test_validator(self):
        self.assertEqual(validator('deposit', 'client', 'Oleg'), ('client', 'Oleg'))
        self.assertEqual(validator('deposit', 'amount', '1000'), ('amount', 1000))
        self.assertIsNone(validator('deposit', 'bad_flag', '1000'))
        self.assertIsNone(validator('withdraw', 'description', ''))
        self.assertEqual(validator('show_bank_statement', 'since', '2023-03-30 00:00:00'), ('since', '2023-03-30 00:00:00'))


    def test_parse_requets(self):
        valid_req = 'deposit --client="John Jones" --amount=100 --description="ATM Deposit"'
        valid_res = {'command': 'deposit', 'client': 'John Jones', 'amount': 100.0, 'description': 'ATM Deposit'}
        
        invalid_req = 'bad_command --client="John Jones" --amount=100 --description="ATM Deposit"'
        invalid_res = {}

        self.assertEqual(parse_requets(valid_req), valid_res)
        self.assertEqual(parse_requets(invalid_req), invalid_res)


if __name__ == '__main__':
    unittest.main()
