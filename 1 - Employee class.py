"""
Assignment 1, by Leonardo Blas.
07/05/2019.
In this assignment we will create an Employee class that we'll use in future
assignments.
"""

from enum import Enum


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
        if not self.valid_name(name):
            self._name = Employee.DEFAULT_NAME
        if not self.valid_number(number):
            self._number = Employee.DEFAULT_NUMBER
        if not self.valid_shift(shift):
            self._shift = Employee.DEFAULT_SHIFT
        self._benefits = self.determine_benefits()
        self._number = number
        self._shift = shift
        self._benefits = self.determine_benefits()

    @property
    def name(self):
        return self._name

    @classmethod
    def valid_name(cls, name):
        """
        Helper function for name's setter.
        :param name: str
        :return: bool
        """
        if type(name) == str:
            return False
        return True

    @name.setter
    def name(self, name):
        if not self.valid_name(name):
            return
        self._name = name

    @property
    def number(self):
        return self._number

    @classmethod
    def valid_number(cls, number):
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
        self.determine_benefits()

    @property
    def shift(self):
        return self._shift

    @classmethod
    def valid_shift(cls, shift):
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
        shift_enum_map = Employee.Shift._value2member_map_
        if shift in Employee.Shift.__members__.keys():
            self._shift = shift
        elif shift in shift_enum_map:
            self._shift = shift_enum_map[shift]

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


def main():
    emp1 = Employee()
    print(emp1.to_string())
    emp2 = Employee('Tom Jones', 374, Employee.Shift.DAY)
    print(emp2.to_string())
    emp3 = Employee('Tim Smith', 99877, Employee.Shift.SWING)
    print(emp3.to_string())
    emp4 = Employee()
    emp4.name = input('Enter an employee\'s name.')
    emp4.number = emp4.get_employee_number()
    emp4.shift = int(input(
        'Enter an employee\'s shift.'
        '\nMust be an int: 1 for DAY, 2 for SWING, 3 for NIGHT.'))
    print(emp4.to_string())


if __name__ == "__main__":
    main()


"""
unidentified #999 (No Benefits)
Shift: DAY

Tom Jones #374 (Benefits)
Shift: DAY

Tim Smith #999 (No Benefits)
Shift: SWING

Enter an employee's name.Homer Simpsons
Enter an employee's number.
Must be an int between 100 and 999.0
The input is not between 100 and 999. Please try again.
Enter an employee's number.
Must be an int between 100 and 999.no
The input is not an integer. Please try again.
Enter an employee's number.
Must be an int between 100 and 999.123 Evergeen
The input is not an integer. Please try again.
Enter an employee's number.
Must be an int between 100 and 999.123
Enter an employee's shift.
Must be an int: 1 for DAY, 2 for SWING, 3 for NIGHT.3
Homer Simpsons #123 (No Benefits)
Shift: NIGHT


Process finished with exit code 0

"""