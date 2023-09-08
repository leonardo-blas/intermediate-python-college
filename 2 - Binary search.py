"""
Assignment 2, by Leonardo Blas.
07/08/2019.
In this assignment we will create an array of Employees and apply Binary
Search and sorting concepts on it. We'll also create a queue of Employees.
"""

from enum import Enum
import numpy as np
import random
import copy


class EmpNumError(Exception):
    pass


class Employee:
    # Shift could be global, but making it a nested class, just in case.
    class Shift(Enum):
        DAY = 1
        SWING = 2
        NIGHT = 3

        def __str__(self):
            return self.name
    DEFAULT_NAME = 'unidentified'
    MIN_NUMBER = 100
    MAX_NUMBER = 999
    DEFAULT_NUMBER = 999
    BENEFIT_NUMBER = 500
    DEFAULT_SHIFT = Shift.DAY

    def __init__(self,
                 name=DEFAULT_NAME,
                 number=DEFAULT_NUMBER,
                 shift=DEFAULT_SHIFT):
        """
        Employee class' constructor.
        :param name: string
        :param number: int
        :param shift: Shift class' enum
        """
        self._name = name
        self._number = number
        self._shift = shift
        self._benefits = self.determine_benefits()
        if not self._name(name):
            self._name = Employee.DEFAULT_NAME
        if not self.valid_number(number):
            self._number = Employee.DEFAULT_NUMBER
        if not self.valid_shift(shift):
            self._shift = Employee.DEFAULT_SHIFT

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
        else:
            self._number = Employee.DEFAULT_NUMBER
            return False

    @number.setter
    def number(self, number):
        if self.valid_number(number):
            self._number = number
            return True
        self.determine_benefits()
        return False

    @property
    def shift(self):
        return self._shift

    def valid_shift(self, shift):
        """
        Helper function for shift's setter.
        :param shift: Shift enum
        :return: bool
        """
        if (shift in Employee.Shift.__members__.keys()) \
                or (shift in Employee.Shift._value2member_map_)\
                or (shift in Employee.Shift):
            return True
        return False

    @shift.setter
    def shift(self, shift):
        if not self.valid_shift(shift):
            self._shift = Employee.DEFAULT_SHIFT
            return False
        shift_enum_map = Employee.Shift._value2member_map_
        if shift in Employee.Shift.__members__.keys():
            self._shift = shift
        elif shift in shift_enum_map:
            self._shift = shift_enum_map[shift]
        return True

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

    def to_string(self):
        """
        Stringizer helper function.
        :return: str
        """
        self.shift = self.shift
        if self.benefits:
            benefits_string = 'Benefits'
        else:
            benefits_string = 'No Benefits'
        return_string = f'{self.name} #{self.number} ({benefits_string})' \
            f'\nShift: {self.shift}\n'
        return return_string

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


# Class not required by specs but code looks neater this way
class EmployeeArrayUtilities:
    NOT_FOUND = -1

    @staticmethod
    def float_largest_to_top(data, array_size):
        """
        Float largest employee number to top.
        :param data: array of Employee objects
        :param array_size: size of array
        :return:
        """
        changed = False
        # notice we stop at array_size - 2 because of expr. k + 1 in loop
        for k in range(array_size - 1):
            if data[k].number > data[k + 1].number:
                data[k], data[k + 1] = data[k + 1], data[k]
                changed = True
        return changed

    @classmethod
    def array_sort(cls, data, array_size):
        """
        A bubble sort that uses helper function float_largest_to_top().
        :param data: array of Employee objects
        :param array_size: size of array
        :return:
        """
        for k in range(array_size):
            if not cls.float_largest_to_top(data, array_size - k):
                return

    @classmethod
    def array_search(cls, data, array_size, search_number):
        for k in range(array_size):
            if data[k].number == search_number:
                return k  # found match, return index
        return cls.NOT_FOUND

    @classmethod
    def get_numeric_input(cls, lower_bound, upper_bound, prompt):
        """
        Helper function. Will take and check for int input.
        :return: int
        """
        while True:
            try:
                number = int(input(prompt))
            except ValueError:
                print('The input is not an integer. Please try again.')
                continue
            try:
                if (number >= lower_bound) and (number <= upper_bound):
                    return number
                else:
                    raise EmpNumError
            except EmpNumError:
                print(f'The input is not between {lower_bound} and '
                      f'{upper_bound}. Please try again.')
                continue


class MyQueue:
    # class ("static") members and intended constants
    MAX_SIZE = 100000
    DEFAULT_SIZE = 10
    EMPTY_QUEUE_RETURN_ALERT = "** attempt to remove from empty queue **"
    ORIG_DEFAULT_ITEM = Employee()
    default_item = ORIG_DEFAULT_ITEM

    def __init__(self, capacity=DEFAULT_SIZE, default_item=None):
        self.tos = 0
        self.stk = []
        if not self.set_capacity(capacity):
            self.capacity = MyQueue.DEFAULT_SIZE
        if default_item is not None:
            self.default_item = default_item
        self.clear()

    def set_capacity(self, capacity):
        if not MyQueue.valid_capacity(capacity):
            return False
        self.capacity = capacity
        self.clear()
        return True

    def add(self, item_to_add):
        """
        Add items to the queue.
        :param item_to_add: arbitrary type
        :return: boolean
        """
        if self.tos == self.capacity:
            return False
        elif type(item_to_add) != type(self.default_item):
            return False
        self.stk.insert(0, item_to_add)
        self.tos += 1
        return True

    def remove(self):
        """
        Remove items from the queue.
        :return: arbitrary type
        """
        if self.tos == 0:
            return self.EMPTY_QUEUE_RETURN_ALERT
        self.tos -= 1
        return self.stk[self.tos]

    def clear(self):
        self.stk = [copy.deepcopy(self.default_item)
                    for k in range(self.capacity)]
        self.tos = 0

    def get_capacity(self):
        return self.capacity

    @classmethod
    def valid_capacity(cls, test_capacity):
        if not (0 <= test_capacity <= cls.MAX_SIZE):
            return False
        else:
            return True

    @classmethod
    def set_default_item(cls, new_default):
        cls.default_item = new_default


def main():
    # Creating lists of names and last names
    name_bank = ['Patrick', 'Spongebob', 'Gary', 'Eugene', 'Homer', 'Billy',
                 'Sandy', 'Lisa', 'Bart', 'Marge', 'Kim', 'Mandy', 'Timmy']
    last_name_bank = ['Star', 'SquarePants', 'the Snail', 'Krabs', 'Simpsons',
                      'Cheeks', 'Possible', 'Turner', 'Neutron', 'Doo',
                      'Tentacles']
    # Creating random array of 20 employees
    array_size = 20
    employee_array = np.array(
        [Employee(
            f'{random.choice(name_bank)} {random.choice(last_name_bank)}',
            random.randint(Employee.MIN_NUMBER, Employee.MAX_NUMBER),
            random.randint(1, 3))  # 1-3 are valid Shift values
            for i in range(array_size)])
    # Printing unsorted array
    for i in range(array_size):
        print(employee_array[i].to_string)
    # Sorting and printing array
    print('\n**********Sorting and printing array**********\n\n')
    EmployeeArrayUtilities.array_sort(employee_array, array_size)
    for i in range(array_size):
        print(employee_array[i].to_string)
    # Creating queue
    employee_queue = MyQueue()
    # Asking for user input for adding employees to the queue
    while True:
        input_number = EmployeeArrayUtilities.get_numeric_input(
            Employee.MIN_NUMBER,
            Employee.MAX_NUMBER,
            'Enter an existing employee\'s numbers to add them to the queue.\n'
        )
        found_status = EmployeeArrayUtilities.array_search(
            employee_array,
            array_size,
            input_number)
        if found_status == EmployeeArrayUtilities.NOT_FOUND:
            print('Employee not found.')
        else:
            employee_queue.add(employee_array[found_status])
        input_decision = EmployeeArrayUtilities.get_numeric_input(
            0,
            1,
            'Do you want to add more employees to the queue? '
            '1 for yes, 0 for no\n'
        )
        if input_decision == 0:
            break
    print('\n\n**********Printing queue**********\n\n')
    for employee in range(employee_queue.tos):
        print(employee_queue.remove().to_string())


if __name__ == "__main__":
    main()


"""
Gary Doo #247 (Benefits)
Shift: DAY

Kim the Snail #282 (Benefits)
Shift: SWING

Lisa Neutron #547 (No Benefits)
Shift: DAY

Marge Simpsons #701 (No Benefits)
Shift: NIGHT

Mandy Star #621 (No Benefits)
Shift: NIGHT

Sandy Cheeks #393 (Benefits)
Shift: NIGHT

Patrick the Snail #787 (No Benefits)
Shift: DAY

Lisa Possible #957 (No Benefits)
Shift: SWING

Gary Tentacles #146 (Benefits)
Shift: SWING

Bart Neutron #607 (No Benefits)
Shift: DAY

Billy Tentacles #136 (Benefits)
Shift: NIGHT

Gary Simpsons #428 (Benefits)
Shift: SWING

Bart Simpsons #286 (Benefits)
Shift: SWING

Bart Neutron #187 (Benefits)
Shift: SWING

Mandy Krabs #181 (Benefits)
Shift: NIGHT

Kim Doo #658 (No Benefits)
Shift: SWING

Kim Cheeks #981 (No Benefits)
Shift: NIGHT

Spongebob Star #336 (Benefits)
Shift: NIGHT

Marge Turner #337 (Benefits)
Shift: NIGHT

Timmy Cheeks #118 (Benefits)
Shift: SWING


**********Sorting and printing array**********


Timmy Cheeks #118 (Benefits)
Shift: SWING

Billy Tentacles #136 (Benefits)
Shift: NIGHT

Gary Tentacles #146 (Benefits)
Shift: SWING

Mandy Krabs #181 (Benefits)
Shift: NIGHT

Bart Neutron #187 (Benefits)
Shift: SWING

Gary Doo #247 (Benefits)
Shift: DAY

Kim the Snail #282 (Benefits)
Shift: SWING

Bart Simpsons #286 (Benefits)
Shift: SWING

Spongebob Star #336 (Benefits)
Shift: NIGHT

Marge Turner #337 (Benefits)
Shift: NIGHT

Sandy Cheeks #393 (Benefits)
Shift: NIGHT

Gary Simpsons #428 (Benefits)
Shift: SWING

Lisa Neutron #547 (No Benefits)
Shift: DAY

Bart Neutron #607 (No Benefits)
Shift: DAY

Mandy Star #621 (No Benefits)
Shift: NIGHT

Kim Doo #658 (No Benefits)
Shift: SWING

Marge Simpsons #701 (No Benefits)
Shift: NIGHT

Patrick the Snail #787 (No Benefits)
Shift: DAY

Lisa Possible #957 (No Benefits)
Shift: SWING

Kim Cheeks #981 (No Benefits)
Shift: NIGHT

Enter an existing employee's numbers to add them to the queue.
136
Do you want to add more employees to the queue? 1 for yes, 0 for no
1
Enter an existing employee's numbers to add them to the queue.
547
Do you want to add more employees to the queue? 1 for yes, 0 for no
1
Enter an existing employee's numbers to add them to the queue.
787
Do you want to add more employees to the queue? 1 for yes, 0 for no
1
Enter an existing employee's numbers to add them to the queue.
286
1
Do you want to add more employees to the queue? 1 for yes, 0 for no
Enter an existing employee's numbers to add them to the queue.
982
Employee not found.
Do you want to add more employees to the queue? 1 for yes, 0 for no
0


**********Printing queue**********


Billy Tentacles #136 (Benefits)
Shift: NIGHT

Lisa Neutron #547 (No Benefits)
Shift: DAY

Patrick the Snail #787 (No Benefits)
Shift: DAY

Bart Simpsons #286 (Benefits)
Shift: SWING


Process finished with exit code 0

"""