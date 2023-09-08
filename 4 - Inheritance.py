"""
Assignment 3, by Leonardo Blas.
07/15/2019.
In this assignment we will reuse our Employee class, use it as a base class to
derive 2 other classes ProductionWorker and ShiftSupervisor, where
ShiftSupervisor will have an array of ProductionWorker objects attribute.
"""

from enum import Enum
import numpy as np
import random


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
                 number=DEFAULT_NUMBER):
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
        if type(name) == str:
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
        if (number > Employee.MIN_NUMBER) and (number < Employee.MAX_NUMBER):
            return True
        return False

    @number.setter
    def number(self, number):
        if self.valid_number(number):
            self._number = number
            return True
        self.determine_benefits()
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
        if self._number < Employee.BENEFIT_NUMBER:
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

    def to_string(self):
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
    MIN_PAY_RATE = 1
    MAX_PAY_RATE = 20
    MIN_HOURS_WORKED = 0
    MAX_HOURS_WORKED = 40

    def __init__(self,
                 name=Employee.DEFAULT_NAME,
                 number=Employee.DEFAULT_NUMBER,
                 shift=DEFAULT_SHIFT,
                 pay_rate=MIN_PAY_RATE,
                 hours_worked=MIN_HOURS_WORKED):
        """
        ProductionWorker's class constructor.
        :param name: string
        :param number: int
        :param shift: Shift class' enum
        :param pay_rate: double
        :param hours_worked: int
        """
        super().__init__(name, number)
        self._shift = shift
        self._pay_rate = pay_rate
        self._hours_worked = hours_worked
        if not self.valid_shift(shift):
            self._shift = ProductionWorker.DEFAULT_SHIFT
        if not self.valid_pay_rate(pay_rate):
            self._pay_rate = ProductionWorker.MIN_PAY_RATE
        if not self.valid_hours_worked(hours_worked):
            self._hours_worked = ProductionWorker.MIN_HOURS_WORKED

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        if not self.valid_shift(shift):
            self._shift = ProductionWorker.DEFAULT_SHIFT
            return
        shift_enum_map = ProductionWorker.Shift._value2member_map_
        if shift in ProductionWorker.Shift.__members__.keys():
            self._shift = shift
        elif shift in shift_enum_map:
            self._shift = shift_enum_map[shift]

    @property
    def pay_rate(self):
        return self._pay_rate

    @pay_rate.setter
    def pay_rate(self, pay_rate):
        if self.valid_pay_rate(pay_rate):
            self._pay_rate = pay_rate

    @property
    def hours_worked(self):
        return self._hours_worked

    @hours_worked.setter
    def hours_worked(self, hours_worked):
        if self.valid_hours_worked(hours_worked):
            self._hours_worked = hours_worked

    @classmethod
    def valid_shift(cls, shift):
        """
        Helper function for shift's setter.
        :param shift: Shift enum
        :return: bool
        """
        if (shift in ProductionWorker.Shift.__members__.keys()) \
                or (shift in ProductionWorker.Shift._value2member_map_) \
                or (shift in ProductionWorker.Shift):
            return True
        return False

    @classmethod
    def valid_pay_rate(cls, pay_rate):
        """
        Helper function for pay_rate's setter.
        :param pay_rate: double
        :return: bool
        """
        if (ProductionWorker.MIN_PAY_RATE <
                pay_rate < ProductionWorker.MAX_PAY_RATE):
            return True
        return False

    @classmethod
    def valid_hours_worked(cls, hours_worked):
        """
        Helper function for hours_worked's setter.
        :param hours_worked: int
        :return: bool
        """
        if (ProductionWorker.MIN_HOURS_WORKED <
                hours_worked < ProductionWorker.MAX_HOURS_WORKED):
            return True
        return False

    def gross_pay(self):
        return self._hours_worked * self._pay_rate

    def to_string(self):
        """
        Stringizer helper function.
        :return: str
        """
        return_string = 'WORKER:\n' + super().to_string()
        return_string += f'Shift: {self.shift}\n' \
            f'${self.pay_rate} per hour\n' \
            f'{self.hours_worked} hours this week\n' \
            f'Gross pay: {self.gross_pay()}\n'
        return return_string


class ShiftSupervisor(Employee):
    MIN_SALARY = 50000
    MAX_SALARY = 200000
    DEFAULT_SHIFT = ProductionWorker.Shift.DAY
    DEFAULT_POSITIONS = 10
    DEFAULT_NUMBER_OF_WORKERS = 0
    BONUS_THRESHOLD = 5
    BONUS_SALARY = 10000

    def __init__(self,
                 name=Employee.DEFAULT_NAME,
                 number=Employee.DEFAULT_NUMBER,
                 salary=MIN_SALARY,
                 shift=DEFAULT_SHIFT,
                 positions=DEFAULT_POSITIONS,
                 number_of_workers=DEFAULT_NUMBER_OF_WORKERS):
        """
        ProductionWorker's class constructor.
        :param name: string
        :param number: int
        :param salary: double
        :param shift: Shift class' enum
        :param positions: int
        :param number_of_workers: int
        """
        super().__init__(name, number)
        self._salary = salary
        self._shift = shift
        self._positions = np.empty(
            [1, self.validate_positions(positions)], dtype=ProductionWorker)
        self._number_of_workers = number_of_workers
        if not self.valid_salary(salary):
            self._salary = ShiftSupervisor.MIN_SALARY
        if not self.valid_shift(shift):
            self._shift = ShiftSupervisor.DEFAULT_SHIFT

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary):
        if self.valid_salary(salary):
            self._salary = salary

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        if not self.valid_shift(shift):
            self._shift = ProductionWorker.DEFAULT_SHIFT
            return
        shift_enum_map = ProductionWorker.Shift._value2member_map_
        if shift in ProductionWorker.Shift.__members__.keys():
            self._shift = shift
        elif shift in shift_enum_map:
            self._shift = shift_enum_map[shift]

    @property
    def positions(self):
        return self._positions

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

    def shift_valid(self, production_worker):
        """
        Check if the shift of an employee is valid.
        :param production_worker: ProductionWorker object
        :return:
        """
        if production_worker.shift == self._shift:
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

    def to_string(self):
        """
        Stringizer helper function.
        :return: str
        """
        return_string = 'SUPERVISOR:\n' + super().to_string()
        return_string += f'Shift: {self.shift}\n' \
            f'Salary: ${self.salary}\n' \
            f'{self.number_of_workers} workers in their shift\n'
        for worker in self.positions:
            if type(worker) is ProductionWorker:
                return_string += '\n' + worker.to_string()
        return return_string

    @classmethod
    def valid_salary(cls, salary):
        """
        Helper function for salary's setter.
        :param shift: double
        :return: bool
        """
        if (ShiftSupervisor.MIN_SALARY <
                salary < ShiftSupervisor.MAX_SALARY):
            return True
        return False

    @classmethod
    def valid_shift(cls, shift):
        """
        Helper function for shift's setter.
        :param shift: Shift enum
        :return: bool
        """
        if (shift in ProductionWorker.Shift.__members__.keys()) \
                or (shift in ProductionWorker.Shift._value2member_map_) \
                or (shift in ProductionWorker.Shift):
            return True
        return False

    @classmethod
    def validate_positions(cls, positions):
        """
        Extra security for setting our array's size.
        :param positions: int
        :return: int
        """
        if type(positions) == int and positions >= 0:
            return positions
        return ShiftSupervisor.DEFAULT_POSITIONS


def main():
    random_salary = \
        random.randint(ShiftSupervisor.MIN_SALARY, ShiftSupervisor.MAX_SALARY)
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
    # Creating array of supervisors
    supervisor = np.array(
        [ShiftSupervisor(),
         ShiftSupervisor('Sally', 456, 15000, ProductionWorker.Shift.NIGHT, 8),
         ShiftSupervisor(
             'John', 132, random_salary, ProductionWorker.Shift.SWING, 5)])
    print('-------------')
    print('SUPERVISOR[0]:')
    print('-------------\n')
    # Filling supervisor[0]
    for i in range(7):
        # Notice Python's mutator decorator makes it look like an overloaded
        # assignment operator.
        supervisor[0].positions = ProductionWorker(
            f'{random.choice(name_bank)} {random.choice(last_name_bank)}',
            random.randint(Employee.MIN_NUMBER, Employee.MAX_NUMBER),
            supervisor[0].shift,
            random.randint(min_pay_rate, max_pay_rate),
            random.randint(min_hours_worked, max_hours_worked))
    for i in range(2):
        # Notice Python's mutator decorator makes it look like an overloaded
        # assignment operator.
        supervisor[0].positions = ProductionWorker(
            f'{random.choice(name_bank)} {random.choice(last_name_bank)}',
            random.randint(Employee.MIN_NUMBER, Employee.MAX_NUMBER),
            ProductionWorker.Shift.NIGHT,
            random.randint(min_pay_rate, max_pay_rate),
            random.randint(min_hours_worked, max_hours_worked))
    # Calling bonus function.
    if supervisor[0].bonus():
        print('THIS SUPERVISOR RECEIVED A SALARY BONUS.\n')
    print(supervisor[0].to_string())
    print('-------------')
    print('SUPERVISOR[1]:')
    print('-------------\n')
    # Filling supervisor[1]
    for i in range(3):
        supervisor[1].positions = ProductionWorker(
            f'{random.choice(name_bank)} {random.choice(last_name_bank)}',
            random.randint(Employee.MIN_NUMBER, Employee.MAX_NUMBER),
            ProductionWorker.Shift.SWING,
            random.randint(min_pay_rate, max_pay_rate),
            random.randint(min_hours_worked, max_hours_worked))
    # Calling bonus function.
    if supervisor[1].bonus():
        print('THIS SUPERVISOR RECEIVED A SALARY BONUS.\n')
    print(supervisor[1].to_string())
    print('-------------')
    print('SUPERVISOR[2]:')
    print('-------------\n')
    # Filling supervisor[2]
    for i in range(6):
        supervisor[2].positions = ProductionWorker(
            f'{random.choice(name_bank)} {random.choice(last_name_bank)}',
            random.randint(Employee.MIN_NUMBER, Employee.MAX_NUMBER),
            ProductionWorker.Shift.SWING,
            random.randint(min_pay_rate, max_pay_rate),
            random.randint(min_hours_worked, max_hours_worked))
    supervisor[2].positions = ProductionWorker(
        f'{random.choice(name_bank)} {random.choice(last_name_bank)}',
        random.randint(Employee.MIN_NUMBER, Employee.MAX_NUMBER),
        ProductionWorker.Shift.DAY,
        random.randint(min_pay_rate, max_pay_rate),
        random.randint(min_hours_worked, max_hours_worked))
    if supervisor[2].bonus():
        print('THIS SUPERVISOR RECEIVED A SALARY BONUS.\n')
    print(supervisor[2].to_string())


if __name__ == "__main__":
    main()

"""
-------------
SUPERVISOR[0]:
-------------

THIS SUPERVISOR RECEIVED A SALARY BONUS.

SUPERVISOR:
unidentified #999 (No Benefits)
Shift: DAY
Salary: $60000
7 workers in their shift

WORKER:
Bart Krabs #223 (Benefits)
Shift: DAY
$1 per hour
3 hours this week
Gross pay: 3

WORKER:
Kim Simpsons #420 (Benefits)
Shift: DAY
$8 per hour
38 hours this week
Gross pay: 304

WORKER:
Patrick Tentacles #629 (No Benefits)
Shift: DAY
$1 per hour
23 hours this week
Gross pay: 23

WORKER:
Billy Krabs #842 (No Benefits)
Shift: DAY
$11 per hour
15 hours this week
Gross pay: 165

WORKER:
Spongebob Neutron #799 (No Benefits)
Shift: DAY
$7 per hour
6 hours this week
Gross pay: 42

WORKER:
Patrick Krabs #564 (No Benefits)
Shift: DAY
$8 per hour
11 hours this week
Gross pay: 88

WORKER:
Gary Star #702 (No Benefits)
Shift: DAY
$8 per hour
31 hours this week
Gross pay: 248

-------------
SUPERVISOR[1]:
-------------

SUPERVISOR:
Sally #456 (Benefits)
Shift: NIGHT
Salary: $50000
0 workers in their shift

-------------
SUPERVISOR[2]:
-------------

No space in array, ignoring addition of employee.

SUPERVISOR:
John #132 (Benefits)
Shift: SWING
Salary: $83311
5 workers in their shift

WORKER:
Homer Doo #650 (No Benefits)
Shift: SWING
$1 per hour
2 hours this week
Gross pay: 2

WORKER:
Patrick Star #615 (No Benefits)
Shift: SWING
$14 per hour
35 hours this week
Gross pay: 490

WORKER:
Billy the Snail #909 (No Benefits)
Shift: SWING
$1 per hour
0 hours this week
Gross pay: 0

WORKER:
Spongebob Neutron #258 (Benefits)
Shift: SWING
$7 per hour
24 hours this week
Gross pay: 168

WORKER:
Lisa SquarePants #496 (Benefits)
Shift: SWING
$4 per hour
21 hours this week
Gross pay: 84


Process finished with exit code 0

"""
