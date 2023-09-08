"""
Assignment 6 by Leonardo Blas.
07/25/2019.
In this assignment we will reuse our Employee, ProductionWorker and
ShiftSupervisor classes, where we'll implement multiple inheritance
on these last 2 classes, onto the new class Member401k.
When maxing the two remaining 401k objects' actual_match, they don't
change because mutators were designed to ignore bad input and preserve
the previous stored value.
"""
import random
import string
from enum import Enum

import numpy as np


class EmpNumError(Exception):
    pass


class NoSpaceInArray(Exception):
    pass


class Employee:
    DEFAULT_NAME = 'unidentified'
    MIN_NUMBER = 100
    MAX_NUMBER = 999
    DEFAULT_NUMBER = 999
    BENEFIT_NUMBER = 500

    def __init__(self,
                 name=DEFAULT_NAME,
                 number=DEFAULT_NUMBER,
                 **kwargs):
        """
        Employee class' constructor.
        :param name: string
        :param number: int
        """
        self._name = name
        self._number = number
        self._benefits = self.determine_benefits()
        if not self.valid_name(name):
            self._name = Employee.DEFAULT_NAME
        if not self.valid_number(number):
            self._number = Employee.DEFAULT_NUMBER

    @property
    def name(self):
        return self._name

    def valid_name(self, name):
        """
        Helper function for name's setter.
        :param name: str
        :return: bool
        """
        if type(name) is str:
            return True
        return False

    @name.setter
    def name(self, name):
        if self.valid_name(name):
            self._name = name
            return True
        return False

    @property
    def number(self):
        return self._number

    def valid_number(self, number):
        """
        Helper function for number's setter.
        :param number: int
        :return: bool
        """
        if type(number) is int \
                and Employee.MIN_NUMBER < number < Employee.MAX_NUMBER:
            return True
        return False

    @number.setter
    def number(self, number):
        if self.valid_number(number):
            self._number = number
            self.determine_benefits()
            return True
        return False

    @property
    def benefits(self):
        return self._benefits

    def determine_benefits(self):
        """
        Determine if employee objects are eligible for benefits.
        :param number: int
        :return: bool
        """
        if type(self._number) is int \
                and self._number < Employee.BENEFIT_NUMBER:
            self._benefits = True
            return True
        self._benefits = False
        return False

    def get_employee_number(self):
        """
        Helper function. Will raise exceptions if unexpected in input.
        :return: int
        """
        while True:
            try:
                number = int(input(
                    'Enter an employee\'s number.'
                    '\nMust be an int between 100 and 999.'))
            except ValueError:
                print('The input is not an integer. Please try again.')
                continue
            try:
                if not self.valid_number(int(number)):
                    raise EmpNumError
                return number
            except EmpNumError:
                print('The input is not between 100 and 999. Please try again.')
                continue

    def __str__(self):
        """
        Stringizer helper function.
        :return: str
        """
        if self.benefits:
            benefits_string = 'Benefits'
        else:
            benefits_string = 'No Benefits'
        return_string = f'{self.name} #{self.number} ({benefits_string})\n'
        return return_string


class ProductionWorker(Employee):
    # Shift could be global, but making it a nested class, just in case.
    class Shift(Enum):
        DAY = 1
        SWING = 2
        NIGHT = 3

        def __str__(self):
            return self.name

    DEFAULT_SHIFT = Shift.DAY
    MIN_PAY_RATE = 1.
    MAX_PAY_RATE = 20.
    MIN_HOURS_WORKED = 0
    MAX_HOURS_WORKED = 40

    def __init__(self,
                 name=Employee.DEFAULT_NAME,
                 number=Employee.DEFAULT_NUMBER,
                 worker_shift=DEFAULT_SHIFT,
                 pay_rate=MIN_PAY_RATE,
                 hours_worked=MIN_HOURS_WORKED,
                 **kwargs):
        """
        ProductionWorker's class constructor.
        :param name: string
        :param number: int
        :param worker_shift: Shift class' enum
        :param pay_rate: double
        :param hours_worked: int
        """
        super().__init__(name, number, **kwargs)
        self._worker_shift = worker_shift
        self._pay_rate = pay_rate
        self._hours_worked = hours_worked
        if not self.valid_worker_shift(worker_shift):
            self._worker_shift = ProductionWorker.DEFAULT_SHIFT
        if not self.valid_pay_rate(pay_rate):
            self._pay_rate = ProductionWorker.MIN_PAY_RATE
        if not self.valid_hours_worked(hours_worked):
            self._hours_worked = ProductionWorker.MIN_HOURS_WORKED
        self._worker_monthly_pay = self.determine_worker_pay()

    @property
    def worker_shift(self):
        return self._worker_shift

    @classmethod
    def valid_worker_shift(cls, worker_shift):
        """
        Helper function for shift's setter.
        :param worker_shift: Shift enum
        :return: bool
        """
        member_map = ProductionWorker.Shift._value2member_map_
        if (worker_shift in ProductionWorker.Shift.__members__.keys()) \
                or worker_shift in member_map \
                or worker_shift in ProductionWorker.Shift:
            return True
        return False

    @worker_shift.setter
    def worker_shift(self, worker_shift):
        if not self.valid_worker_shift(worker_shift):
            self._worker_shift = ProductionWorker.DEFAULT_SHIFT
            return
        shift_enum_map = ProductionWorker.Shift._value2member_map_
        if worker_shift in ProductionWorker.Shift.__members__.keys():
            self._worker_shift = worker_shift
        elif worker_shift in shift_enum_map:
            self._worker_shift = shift_enum_map[worker_shift]

    @property
    def pay_rate(self):
        return self._pay_rate

    @classmethod
    def valid_pay_rate(cls, pay_rate):
        """
        Helper function for pay_rate's setter.
        :param pay_rate: double
        :return: bool
        """
        if (type(pay_rate) is float or type(pay_rate) is int) \
                and (ProductionWorker.MIN_PAY_RATE <
                     pay_rate < ProductionWorker.MAX_PAY_RATE):
            return True
        return False

    @pay_rate.setter
    def pay_rate(self, pay_rate):
        if self.valid_pay_rate(pay_rate):
            self._pay_rate = pay_rate
            self._worker_monthly_pay = self.determine_worker_pay()

    @property
    def hours_worked(self):
        return self._hours_worked

    @classmethod
    def valid_hours_worked(cls, hours_worked):
        """
        Helper function for hours_worked's setter.
        :param hours_worked: int
        :return: bool
        """
        if type(hours_worked) is int \
                and (ProductionWorker.MIN_HOURS_WORKED <
                     hours_worked < ProductionWorker.MAX_HOURS_WORKED):
            return True
        return False

    @hours_worked.setter
    def hours_worked(self, hours_worked):
        if self.valid_hours_worked(hours_worked):
            self._hours_worked = hours_worked

    @property
    def worker_monthly_pay(self):
        return self._worker_monthly_pay

    def determine_worker_pay(self):
        """
        Determine the worker's monthly payment.
        :return: double
        """
        return self.gross_pay() / 4

    def gross_pay(self):
        return self._hours_worked * self._pay_rate

    def __str__(self):
        """
        Stringizer helper function.
        :return: str
        """
        return_string = 'WORKER:\n' + super().__str__()
        return_string += f'Shift: {self.worker_shift}\n' \
            f'${self.pay_rate} per hour\n' \
            f'{self.hours_worked} hours this week\n' \
            f'Gross pay: {self.gross_pay()}\n'
        return return_string


class ShiftSupervisor(Employee):
    MIN_SALARY = 50000.
    MAX_SALARY = 200000.
    DEFAULT_SHIFT = ProductionWorker.Shift.DAY
    DEFAULT_POSITIONS = 10
    DEFAULT_NUMBER_OF_WORKERS = 0
    BONUS_THRESHOLD = 5
    BONUS_SALARY = 10000.

    def __init__(self,
                 name=Employee.DEFAULT_NAME,
                 number=Employee.DEFAULT_NUMBER,
                 salary=MIN_SALARY,
                 supervisor_shift=DEFAULT_SHIFT,
                 positions=DEFAULT_POSITIONS,
                 number_of_workers=DEFAULT_NUMBER_OF_WORKERS,
                 **kwargs):
        """
        ProductionWorker's class constructor.
        :param name: string
        :param number: int
        :param salary: double
        :param supervisor_shift: Shift class' enum
        :param positions: int
        :param number_of_workers: int
        """
        super().__init__(name, number, **kwargs)
        self._salary = salary
        self._supervisor_shift = supervisor_shift
        self._positions = np.empty(
            [1, self.validate_positions(positions)], dtype=ProductionWorker)
        self._number_of_workers = number_of_workers
        self._supervisor_monthly_pay = self.determine_supervisor_pay()
        if not self.valid_salary(salary):
            self._salary = ShiftSupervisor.MIN_SALARY
        if not self.valid_supervisor_shift(supervisor_shift):
            self._supervisor_shift = ShiftSupervisor.DEFAULT_SHIFT

    @property
    def salary(self):
        return self._salary

    @classmethod
    def valid_salary(cls, salary):
        """
        Helper function for salary's setter.
        :param shift: double
        :return: bool
        """
        if (type(salary) is float or type(salary) is int) \
                and (ShiftSupervisor.MIN_SALARY <
                     salary < ShiftSupervisor.MAX_SALARY):
            return True
        return False

    @salary.setter
    def salary(self, salary):
        if self.valid_salary(salary):
            self._salary = salary
            self._supervisor_monthly_pay = self.determine_supervisor_pay()

    @property
    def supervisor_shift(self):
        return self._supervisor_shift

    @classmethod
    def valid_supervisor_shift(cls, supervisor_shift):
        """
        Helper function for shift's setter.
        :param supervisor_shift: Shift enum
        :return: bool
        """
        if type(supervisor_shift) is ProductionWorker.Shift \
                and (supervisor_shift in ProductionWorker.Shift.__members__.keys()) \
                or (supervisor_shift in ProductionWorker.Shift._value2member_map_) \
                or (supervisor_shift in ProductionWorker.Shift) \
                and supervisor_shift is not None:
            return True
        return False

    @supervisor_shift.setter
    def supervisor_shift(self, supervisor_shift):
        if not self.valid_supervisor_shift(supervisor_shift):
            self._supervisor_shift = ProductionWorker.DEFAULT_SHIFT
            return
        shift_enum_map = ProductionWorker.Shift._value2member_map_
        if supervisor_shift in ProductionWorker.Shift.__members__.keys():
            self._supervisor_shift = supervisor_shift
        elif supervisor_shift in shift_enum_map:
            self._supervisor_shift = shift_enum_map[supervisor_shift]

    @property
    def positions(self):
        return self._positions

    @classmethod
    def validate_positions(cls, positions):
        """
        Extra security for setting our array's size.
        :param positions: int
        :return: int
        """
        if type(positions) is int \
                and positions >= 0:
            return positions
        return ShiftSupervisor.DEFAULT_POSITIONS

    @positions.setter
    # Notice Python's mutator decorator makes it look like an overloaded
    # assignment operator.
    def positions(self, production_worker):
        if not self.shift_valid(production_worker):
            return
        try:
            if self.positions.size <= self._number_of_workers:
                raise NoSpaceInArray
        except NoSpaceInArray:
            print('No space in array, ignoring addition of employee.\n')
            return
        # Appending ProductionWorker objects to the end of the array.
        self._positions = np.append(self._positions, production_worker)
        # Deleting ProductionWorker objects from the beginning of the array.
        self._positions = np.delete(self._positions, 0)
        self._number_of_workers += 1

    @property
    def number_of_workers(self):
        return self._number_of_workers

    @property
    def supervisor_monthly_pay(self):
        return self._supervisor_monthly_pay

    def determine_supervisor_pay(self):
        """
        Determine the supervisor's monthly payment.
        :return: double
        """
        return self._salary / 12

    def shift_valid(self, production_worker):
        """
        Check if the shift of an employee is valid.
        :param production_worker: ProductionWorker object
        :return:
        """
        if type(production_worker) is ProductionWorker.Shift \
                and type(self.supervisor_shift) is ProductionWorker.Shift \
                and production_worker.worker_shift == self._supervisor_shift:
            return True
        return False

    def bonus(self):
        """
        Determine if supervisor gets or not a bonus and return a flag.
        :return: bool
        """
        # Could develop bonus into an attribute, but specs don't ask for this.
        future_salary = self._salary + ShiftSupervisor.BONUS_SALARY
        if self._number_of_workers > ShiftSupervisor.BONUS_THRESHOLD and \
                future_salary < ShiftSupervisor.MAX_SALARY:
            self._salary += ShiftSupervisor.BONUS_SALARY
            return True
        return False

    def __str__(self):
        """
        Stringizer helper function.
        :return: str
        """
        return_string = 'SUPERVISOR:\n' + super().__str__()
        return_string += f'Shift: {self.supervisor_shift}\n' \
            f'Salary: ${self.salary}\n' \
            f'{self.number_of_workers} workers in their shift\n'
        for worker in self.positions:
            if type(worker) is ProductionWorker:
                return_string += '\n' + worker.__str__()
        return return_string


class Member401k(ProductionWorker, ShiftSupervisor):
    DEFAULT_ACCOUNT = 'qqq999'
    NUMBER_OF_LETTERS = 3
    MIN_AMOUNT = 0.
    MAX_AMOUNT = 5000.
    MIN_MATCH = 0.
    MAX_PERCENTAGE_MATCH = 0.05
    MIN_MONTHLY_PAY = 0.

    def __init__(self,
                 account=DEFAULT_ACCOUNT,
                 amount=MIN_AMOUNT,
                 **kwargs):
        super().__init__(**kwargs)
        self._account = account + str(self.number)
        self._amount = amount
        self._maximum_match = self.max_match(**kwargs)
        self._actual_match = self.actual_max(amount)
        # Member designed by client:
        self._monthly_pay = self.determine_pay(**kwargs)
        if not self.valid_account(account):
            self._account = Member401k.DEFAULT_ACCOUNT
        if not self.valid_amount(amount):
            self._amount = Member401k.MIN_AMOUNT

    @property
    def account(self):
        return self._account

    def valid_account(self, account):
        """
        Helper function for account's setter.
        :param account: str
        :return: bool
        """
        if type(account) is str \
                and len(account) is Member401k.NUMBER_OF_LETTERS:
            return True
        return False

    @account.setter
    def account(self, account):
        if self.valid_account(account):
            self._account = account + str(self.number)
            return True
        return False

    @property
    def amount(self):
        return self._amount

    @classmethod
    def valid_amount(cls, amount):
        """
        Helper function for name's setter.
        :param amount: float
        :return: bool
        """
        if (type(amount) is float or type(amount) is int) \
                and Member401k.MIN_AMOUNT <= amount <= Member401k.MAX_AMOUNT:
            return True
        return False

    @amount.setter
    def amount(self, amount):
        if self.valid_amount(amount):
            self._amount = amount
            self._actual_match = self.actual_max(amount)
            return True
        return False

    @property
    def maximum_match(self):
        return self._maximum_match

    def max_match(self, **kwargs):
        """
        Determine max_match.
        :param kwargs: kwargs
        :return: double
        """
        if 'pay_rate' in kwargs:
            return (self.gross_pay() * 4) \
                   * Member401k.MAX_PERCENTAGE_MATCH
        if 'salary' in kwargs:
            return (self.salary / 12) \
                   * Member401k.MAX_PERCENTAGE_MATCH
        return Member401k.MIN_MATCH

    @property
    def actual_match(self):
        return self._actual_match

    def actual_max(self, amount):
        """
        Determine actual_match.
        :param amount: double
        :return: double
        """
        if self.valid_amount(amount) and self.maximum_match < amount:
            return amount
        return self._maximum_match

    @property
    def monthly_pay(self):
        return self._monthly_pay

    def determine_pay(self, **kwargs):
        """
        Helper function to determine the monthly pay of employees.
        :param kwargs: kwargs
        :return: double
        """
        if 'pay_rate' in kwargs:
            return self.gross_pay() * 4
        if 'salary' in kwargs:
            return self.salary / 12
        return Member401k.MIN_MONTHLY_PAY

    def __str__(self):
        """
        Stringizer helper function.
        :return: str
        """
        # Selecting Employee Class' __str__()
        return_string = super().__self_class__.__mro__[3].__str__(self)
        return_string += f'Account #{self.account}\n' \
            f'Monthly pay: {round(self.monthly_pay, 2)}\n' \
            f'Amount Contributed: {round(self.amount, 2)}\n' \
            f'Max match: ${round(self.maximum_match, 2)}\n' \
            f'Actual match: ${round(self.actual_match, 2)}\n'
        return return_string


def main():
    print('MRO: ', Member401k.__mro__, '\n')
    min_pay_rate = ProductionWorker.MIN_PAY_RATE
    max_pay_rate = 30  # Requested by specs.
    min_hours_worked = ProductionWorker.MIN_HOURS_WORKED
    max_hours_worked = ProductionWorker.MAX_HOURS_WORKED
    # Random ProductionWorker objects generation
    name_bank = ['Patrick', 'Spongebob', 'Gary', 'Eugene', 'Homer', 'Billy',
                 'Sandy', 'Lisa', 'Bart', 'Marge', 'Kim', 'Mandy', 'Timmy']
    last_name_bank = ['Star', 'SquarePants', 'the Snail', 'Krabs', 'Simpsons',
                      'Cheeks', 'Possible', 'Turner', 'Neutron', 'Doo',
                      'Tentacles']
    # Creating 401k Production Workers
    # Creating 3 401k objects with actual_match > max
    print('*****FIRST DISPLAYING:*****\n')
    worker_list = []
    for i in range(3):
        worker_list.append(
            Member401k(
                name=f'{random.choice(name_bank)}'
                f' {random.choice(last_name_bank)}',
                number=random.randint(
                    Employee.MIN_NUMBER, Employee.MAX_NUMBER),
                worker_shift=ProductionWorker.Shift.NIGHT,
                pay_rate=random.randint(
                    ProductionWorker.MIN_PAY_RATE,
                    ProductionWorker.MAX_HOURS_WORKED),
                hours_worked=random.randint(
                    ProductionWorker.MIN_HOURS_WORKED,
                    ProductionWorker.MAX_HOURS_WORKED),
                # Line of code that makes actual_max > max
                amount=Member401k.MAX_AMOUNT + 1,
                account=str(random.choice(string.ascii_lowercase)) \
                        + str(random.choice(string.ascii_lowercase)) \
                        + str(random.choice(string.ascii_lowercase)))
        )
        print(f'WORKER #{i}:')
        print(worker_list[i])
    # Creating 401k Supervisors
    # Creating 2 401k objects with actual_match < max
    supervisor_list = []
    for i in range(2):
        supervisor_list.append(
            Member401k(
                name=f'{random.choice(name_bank)}'
                f' {random.choice(last_name_bank)}',
                number=random.randint(
                    Employee.MIN_NUMBER, Employee.MAX_NUMBER),
                salary=random.randint(
                    ShiftSupervisor.MIN_SALARY, ShiftSupervisor.MAX_SALARY),
                supervisor_shift=ProductionWorker.Shift.NIGHT,
                positions=random.randint(
                    0, ShiftSupervisor.DEFAULT_POSITIONS),
                amount=random.randint(
                    Member401k.MIN_AMOUNT, Member401k.MAX_AMOUNT),
                account=str(random.choice(string.ascii_lowercase)) \
                        + str(random.choice(string.ascii_lowercase)) \
                        + str(random.choice(string.ascii_lowercase)))
        )
        print(f'SUPERVISOR #{i}:')
        print(supervisor_list[i])

    print('*****SECOND DISPLAYING:***\n')
    # Modifying 2 401k objects such that actual_max > max
    for supervisor in supervisor_list:
        # Line of code that makes actual_max > max
        supervisor.amount = Member401k.MAX_AMOUNT + 1,
    # Printing 401k objects in the same previous order
    for worker in worker_list:
        print(worker)
    for supervisor in supervisor_list:
        print(supervisor)

    # Testing limits of 401k attributes:
    print('\nTESTING LIMITS OF 401K ATTRIBUTES:\n')
    print('MIN LIMITS:')
    test = Member401k(
        amount=Member401k.MIN_AMOUNT - 1,
        account=''
    )
    print('TEST:')
    print(test)
    print('MAX LIMITS:')
    test = Member401k(
        amount=Member401k.MAX_AMOUNT + 1,
        account='abcde'
    )
    print('TEST:')
    print(test)


if __name__ == "__main__":
    main()

"""
MRO:  (<class '__main__.Member401k'>, <class '__main__.ProductionWorker'>, <class '__main__.ShiftSupervisor'>, <class '__main__.Employee'>, <class 'object'>) 

*****FIRST DISPLAYING:*****

WORKER #0:
Marge Doo #309 (Benefits)
Account #hjn309
Monthly pay: 24.0
Amount Contributed: 0.0
Max match: $1.2
Actual match: $1.2

WORKER #1:
Bart Tentacles #830 (No Benefits)
Account #sxa830
Monthly pay: 128.0
Amount Contributed: 0.0
Max match: $6.4
Actual match: $6.4

WORKER #2:
Homer Cheeks #389 (Benefits)
Account #rxn389
Monthly pay: 4.0
Amount Contributed: 0.0
Max match: $0.2
Actual match: $0.2

SUPERVISOR #0:
Marge Krabs #248 (Benefits)
Account #dex248
Monthly pay: 16584.92
Amount Contributed: 3552
Max match: $829.25
Actual match: $3552

SUPERVISOR #1:
Homer Cheeks #747 (No Benefits)
Account #jji747
Monthly pay: 11405.08
Amount Contributed: 1594
Max match: $570.25
Actual match: $1594

*****SECOND DISPLAYING:***

Marge Doo #309 (Benefits)
Account #hjn309
Monthly pay: 24.0
Amount Contributed: 0.0
Max match: $1.2
Actual match: $1.2

Bart Tentacles #830 (No Benefits)
Account #sxa830
Monthly pay: 128.0
Amount Contributed: 0.0
Max match: $6.4
Actual match: $6.4

Homer Cheeks #389 (Benefits)
Account #rxn389
Monthly pay: 4.0
Amount Contributed: 0.0
Max match: $0.2
Actual match: $0.2

Marge Krabs #248 (Benefits)
Account #dex248
Monthly pay: 16584.92
Amount Contributed: 3552
Max match: $829.25
Actual match: $3552

Homer Cheeks #747 (No Benefits)
Account #jji747
Monthly pay: 11405.08
Amount Contributed: 1594
Max match: $570.25
Actual match: $1594


TESTING LIMITS OF 401K ATTRIBUTES:

MIN LIMITS:
TEST:
unidentified #999 (No Benefits)
Account #qqq999
Monthly pay: 0.0
Amount Contributed: 0.0
Max match: $0.0
Actual match: $0.0

MAX LIMITS:
TEST:
unidentified #999 (No Benefits)
Account #qqq999
Monthly pay: 0.0
Amount Contributed: 0.0
Max match: $0.0
Actual match: $0.0


Process finished with exit code 0
"""