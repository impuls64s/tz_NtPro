from database import Database
from prettytable import PrettyTable
import datetime


CLI = {
    'deposit': ['client', 'amount', 'description'],
    'withdraw': ['client', 'amount', 'description'],
    'show_bank_statement': ['client', 'since', 'till']
}


def print_table(data):
    mytable = PrettyTable()
    mytable.field_names = ["Date",
                           "Description",
                           "Withdrawals",
                           "Deposits",
                           "Balance"
                           ]
    mytable.add_rows(data)
    wit = dep = 0
    for n in data:
        wit += n[2]
        dep += n[3]

    mytable.add_row(['', '', '', '', ''])
    mytable.add_row(['', 'Totals', wit, dep, dep-wit])
    print(mytable)


def validator(cmd, key, value):
    flags = CLI.get(cmd)

    if key and value and key in flags:
        if key == 'amount':
            try:
                float(value)
                return key, float(value)
            except ValueError:
                print(f'[-] Amount is not a number - {value}')

        elif key in ('since', 'till'):
            try:
                datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                return key, value
            except Exception:
                print(f'[-] Invalid date - {key}:{value}\n')
        else:
            return key, value


def parse_requests(req):
    req_lst = req.split('--')  # Разделяем строку на отдельные части по --
    req_cmd = req_lst[0].strip()  # Определяем переданную команду
    req_args = req_lst[1:]  # Определяем аргументы запроса

    # Проверка на существующую команду и нужное кол-во аргументов
    if (CLI.get(req_cmd) is None) or (len(req_args) != 3):
        print(f'[-] Invalid command or number of arguments: {len(req_args)}\n')
        return {}

    value = {'command': req_cmd}
    for req_arg in req_args:
        arg_key = req_arg.split('=')[0]
        arg_value = req_arg.split('=')[1].strip().replace('"', '')
        valid_data = validator(req_cmd, arg_key, arg_value)

        if valid_data:
            value[valid_data[0]] = valid_data[1]
        else:
            print(f'[-] Invalid arguments or values present: {arg_key}\n')
            return {}
    return value


def main():
    db = Database(filename='db.sqlite3')
    db.create_table()
    print('Service started!\n')
    
    while True:
        request = input('> ')
        if request == 'exit':
            break
        try:
            response = parse_requests(request)
            cmd_response = response.get('command')
            match cmd_response:
                
                case 'deposit':
                    db.deposit(response)
                    print('[+] Deposit operation was successful!\n')
                
                case 'withdraw':
                    db.withdraw(response)
                    print('[+] Withdraw operation was successful!\n')
                
                case 'show_bank_statement':
                    data = db.show_bank_statement(response)
                    print_table(data)
   
        except Exception as ex:
            print(f'[-] Error possibly invalid request - {ex}\n')
        finally:
            db.close()
    print('Good bye!!!')


if __name__ == '__main__':
    main()
