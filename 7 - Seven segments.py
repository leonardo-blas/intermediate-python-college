"""
Assignment 7, by Leonardo Blas.
07/29/2019.
In this assignment we will create 3 classes, BooleanFunc, MultiSegmentLogic,
and SevenSegmentLogic, which is a child function from MultiSegmentLogic. The
purpose of the program is to implement a 7 Segment display logic like the
ones used for running simple 7 segments hardware displays with Raspberry Pi or
Arduino.
"""
import copy
import numpy as np


def main():
    """
    # ACT 1. Changed one line and added one line. It already was a pretty
    # complete testing main.
    bf_and = BooleanFunc(defining_list=[False, False, False, True])
    even_func_true = [0, 2, 4, 6, 8, 10, 12, 14]
    greater_9_func_true = [10, 11, 12, 13, 14, 15]  # >9 func using T to define
    greater_3_func_false = [0, 1, 2, 3]  # >3 func using F to define

    bf_a = BooleanFunc(10)
    bf_b = BooleanFunc(16)
    bf_c = BooleanFunc(16)

    print(
        "--- Testing constructors and mutators of AND, even, >9 and >3 -------"
    )
    bf_a.set_truth_table_using(True, even_func_true)
    bf_b.set_truth_table_using(True, greater_9_func_true)
    # Added a new method call.
    bf_c.set_truth_table_using(False, greater_3_func_false)
    bf_c.set_truth_table_using(True, greater_3_func_false)

    for func in [bf_and, bf_a, bf_b, bf_c]:
        print(func)

    print("--- Testing inputs that cover the allowable and illegal\n"
          "values for AND ---------------")
    for input_x in range(10):
        print(bf_and.eval(input_x))
        print("AND({}) = {}".format(input_x, bf_and.get_state()))

    print(
        "--- Testing deepcopy() on bf_a -> bf_b -------")
    print("--- bf_a and bf_b BEFORE modifying bf_a):\n")
    print(bf_a)
    print(bf_b)

    # Fixed this method call from original provided code. It was bugged.
    bf_b = copy.deepcopy(bf_a)

    bf_a.set_truth_table_using(True, [0, 1, 2, 7, 8, 9])
    print("--- bf_a and bf_b AFTER modifying bf_a):\n")
    print(bf_a)
    print(bf_b)
    """

    """
    # ACT 2. Changed one line. It already was a pretty complete testing main.
    my_12_seg = MultiSegmentLogic(12)

    print("As constructed -------------------")
    print(my_12_seg)

    try:
        my_12_seg.eval(1)
    except AttributeError as err:
        print("\nExpected ... " + str(err) + "\n")

    for k in range(12):
        my_12_seg.set_segment(k, BooleanFunc(
            defining_list=[True, False, True, False]))

    print(my_12_seg)

    print("Evaluating my_12_seg at 2 (which should be True) -----------",
          my_12_seg.eval(2))
    print("segs 3, 5 and, illegal, 29:   ",
          str(my_12_seg.get_val_of_seg(2)),
          str(my_12_seg.get_val_of_seg(5)),
          str(my_12_seg.get_val_of_seg(29)))
    """

    my_7_seg = SevenSegmentLogic()
    my_12_seg = MultiSegmentLogic(12)

    print("As constructed -------------------")
    print("FALSE MEANS TURNED ON")

    print(my_7_seg)

    try:
        my_12_seg.set_num_segs(12)  # should work
        my_7_seg.set_num_segs(8)  # should "throw"
    except ValueError as err:
        print("\nExpected ... " + str(err) + "\n")

    try:
        my_7_seg.eval(1)
    except AttributeError as err:
        print("\nNot Expected... " + str(err) + "\n")

    print("FALSE MEANS TURNED ON")

    for input_x in range(16):
        my_7_seg.eval(input_x)
        print("\n| ", end='')
        for k in range(7):
            print(str(my_7_seg.get_val_of_seg(k)) + " | ", end='')
        print()

    print("\nFALSE MEANS TURNED ON")


class BooleanFunc:
    # static members and intended constants
    MAX_TABLE_SIZE = 65536  # that's 16 binary inputs
    MIN_TABLE_SIZE = 2  # that's 1 binary input
    DEFAULT_TABLE_SIZE = 4
    DEFAULT_FUNC = DEFAULT_TABLE_SIZE * [False]

    def __init__(self,
                 table_size=None,
                 defining_list=None,
                 eval_return_if_error=False):
        if not table_size and not defining_list:
            # passed neither list nor size
            table_size = self.DEFAULT_TABLE_SIZE
            defining_list = self.DEFAULT_FUNC
        elif table_size and not defining_list:
            # passed size but no list
            self.valid_table_size(table_size)  # raises, no return
            defining_list = table_size * [False]
        elif not table_size:
            # passed list but no size
            self.valid_defining_list(defining_list)  # raises, no return
            table_size = len(defining_list)
        else:
            # passed both list and size
            self.valid_defining_list(defining_list)
            if len(defining_list) != table_size:
                raise ValueError("Table size does not match list length"
                                 " in constructor.")
                # sanitize bools (e.g. (1.32, "hi", -99)->True,
        # (0.0, "", 0)->False)
        eval_return_if_error = bool(eval_return_if_error)
        defining_list = [bool(item) for item in defining_list]
        # assign instance members
        self.table_size = table_size
        self.truth_table = np.array(defining_list, dtype=bool)
        self.eval_return_if_error = eval_return_if_error
        self.state = eval_return_if_error

    def get_state(self):
        return self.state

    @classmethod
    def valid_table_size(cls, size):
        if not isinstance(size, int):
            raise TypeError("Table size must be an int.")
        if not (cls.MIN_TABLE_SIZE <= size <= cls.MAX_TABLE_SIZE):
            raise ValueError("Bad table size passed to constructor"
                             " (legal range: {}-{}).".
                             format(cls.MIN_TABLE_SIZE, cls.MAX_TABLE_SIZE))

    @classmethod
    def valid_defining_list(cls, the_list):
        if not isinstance(the_list, list):
            raise ValueError("Bad type in constructor. defining_list must be"
                             " type list.")
        if not (cls.MIN_TABLE_SIZE <= len(the_list) <= cls.MAX_TABLE_SIZE):
            raise ValueError("Bad list passed to constructor"
                             " (its length is outside legal range: {}-{}).".
                             format(cls.MIN_TABLE_SIZE, cls.MAX_TABLE_SIZE))

    def eval(self, input):
        """
        State field mutator.
        :param input: int
        :return: bool
        """
        if type(input) is int \
                and 0 <= input < self.table_size:
            self.state = self.truth_table[input]
        else:
            self.state = self.eval_return_if_error
        return self.state

    def set_truth_table_using(self,
                              rarer_value,
                              inputs_that_produce_rarer_val):
        """
        Set the truth table using an array of positions and a boolean value.
        :param rarer_value: bool
        :param inputs_that_produce_rarer_val: int list
        :return: bool
        """
        if self.table_size <= len(inputs_that_produce_rarer_val) <= 0:
            return False
        sanitized_list = []
        for i in inputs_that_produce_rarer_val:
            if type(i) is int \
                    and 0 <= i < self.table_size:
                sanitized_list.append(i)
        if len(sanitized_list) < 0:
            return False
        for i in range(self.table_size - 1):
            self.truth_table[i] = not rarer_value
        for i in sanitized_list:
            self.truth_table[i] = rarer_value
        return True

    def __str__(self):
        ret_str = "truth_table: " + str(self.truth_table) \
                  + "\nsize = " + str(self.table_size) \
                  + "\nerror return = " + str(self.eval_return_if_error) \
                  + "\ncurrent state = " + str(self.state) + "\n"
        return ret_str


class MultiSegmentLogic:
    MAX_SEGS = 1000
    MIN_SEGS = 1
    DEFAULT_SEGS = 7

    def __init__(self, num_segs=DEFAULT_SEGS):
        self.num_segs = num_segs
        self.segs = copy.deepcopy([BooleanFunc() for i in range(num_segs)])
        if not self.valid_num_segs(num_segs):
            self.num_segs = self.DEFAULT_SEGS
            self.segs = copy.deepcopy(
                [BooleanFunc() for i in range(self.DEFAULT_SEGS)])

    def valid_num_segs(self, num_segs):
        """
        Helper function for num_segs' mutator.
        :param num_segs: int
        :return: bool
        """
        if type(num_segs) is int \
                and 0 <= num_segs < self.MAX_SEGS:
            return True
        return False

    def set_num_segs(self, num_segs):
        """
        num_segs' mutator.
        :param num_segs: int
        :return: no return
        """
        if self.valid_num_segs(num_segs):
            self.num_segs = num_segs
            self.segs = copy.deepcopy([BooleanFunc() for i in range(num_segs)])

    def set_segment(self, seg_num, func_for_this_seg):
        """
        Deep copy for an element of segs.
        :param seg_num: int
        :param func_for_this_seg: BooleanFunc
        :return: bool
        """
        if type(func_for_this_seg) is BooleanFunc \
                and 0 <= seg_num:
            self.segs[seg_num] = copy.deepcopy(func_for_this_seg)

    def eval(self, input):
        """
        Mutator for segs.
        :param input: int
        :return: bool
        """
        if type(input) is not int or input < 0:
            return
        try:
            for i in self.segs:
                i.eval(input)
                if i is None:
                    raise AttributeError(
                        "None value detected. Bailing on dep copy.")
        except AttributeError:
            return False

    def get_val_of_seg(self, seg_num):
        """
        Get val of every segment.
        :param seg_num: int
        :return: boolean
        """
        if self.valid_num_segs(seg_num) \
                and seg_num < len(self.segs):
            return self.segs[seg_num].get_state()
        return False

    def __str__(self):
        ret_str = "\nsegs = \n"
        for booleanFunc in self.segs:
            ret_str += booleanFunc.__str__() + "\n"
        return ret_str


class SevenSegmentLogic(MultiSegmentLogic):
    SEVEN_SEGMENTS = 7
    PATTERNS = 16

    def __init__(self):
        super().__init__(self.SEVEN_SEGMENTS)
        self.empty = False
        self.generate()

    def set_num_segs(self, num_segs):
        """
        Override set_num_segs such that num_segs is always 7.
        :param num_segs: int
        :return: no return
        """
        if num_segs is not self.SEVEN_SEGMENTS:
            raise ValueError
        super(SevenSegmentLogic, self).set_num_segs(num_segs)

    def generate(self):
        """
        Helper function to generate our logic.
        :return: none
        """
        seven_boolean_func_list = [BooleanFunc(self.PATTERNS)
                                   for i in range(self.SEVEN_SEGMENTS)]
        if not self.empty:
            # Manual set-up.
            rows = [
                [1, 4, 11, 13],
                [5, 6, 11, 12, 14, 15],
                [2, 12, 14, 15],
                [1, 4, 7, 9, 10, 15],
                [1, 3, 4, 5, 7, 9],
                [1, 2, 3, 7, 13],
                [0, 1, 12]]
            # Setting up such that negative means turned on.
            for i in range(len(seven_boolean_func_list)):
                seven_boolean_func_list[i].set_truth_table_using(True, rows[i])
            self.empty = True
        for i in range(len(seven_boolean_func_list)):
            self.set_segment(i, seven_boolean_func_list[i])


if __name__ == "__main__":
    main()

"""
# ACT 1

--- Testing constructors and mutators of AND, even, >9 and >3 -------
truth_table: [False False False  True]
size = 4
error return = False
current state = False

truth_table: [ True False  True False  True False  True False  True False]
size = 10
error return = False
current state = False

truth_table: [False False False False False False False False False False  True  True
  True  True  True  True]
size = 16
error return = False
current state = False

truth_table: [ True  True  True  True False False False False False False False False
 False False False False]
size = 16
error return = False
current state = False

--- Testing inputs that cover the allowable and illegal
values for AND ---------------
False
AND(0) = False
False
AND(1) = False
False
AND(2) = False
False
AND(3) = False
False
AND(4) = False
False
AND(5) = False
False
AND(6) = False
False
AND(7) = False
False
AND(8) = False
False
AND(9) = False
--- Testing deepcopy() on bf_a -> bf_b -------
--- bf_a and bf_b BEFORE modifying bf_a):

truth_table: [ True False  True False  True False  True False  True False]
size = 10
error return = False
current state = False

truth_table: [False False False False False False False False False False  True  True
  True  True  True  True]
size = 16
error return = False
current state = False

--- bf_a and bf_b AFTER modifying bf_a):

truth_table: [ True  True  True False False False False  True  True  True]
size = 10
error return = False
current state = False

truth_table: [ True False  True False  True False  True False  True False]
size = 10
error return = False
current state = False


Process finished with exit code 0

# ACT 2

As constructed -------------------

segs = 
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  
False  False  False  False  

PARENT EVAL : False

segs = 
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  
True   False  True   False  

PARENT EVAL : True
Evaluating my_12_seg at 2 (which should be True) ----------- True
segs 3, 5 and, illegal, 29:    False False False

Process finished with exit code 0

# ACT 3

As constructed -------------------
FALSE MEANS TURNED ON

segs = 
truth_table: [False  True False False  True False False False False False False  True
 False  True False False]
size = 16
error return = False
current state = False

truth_table: [False False False False False  True  True False False False False  True
  True False  True  True]
size = 16
error return = False
current state = False

truth_table: [False False  True False False False False False False False False False
  True False  True  True]
size = 16
error return = False
current state = False

truth_table: [False  True False False  True False False  True False  True  True False
 False False False  True]
size = 16
error return = False
current state = False

truth_table: [False  True False  True  True  True False  True False  True False False
 False False False False]
size = 16
error return = False
current state = False

truth_table: [False  True  True  True False False False  True False False False False
 False  True False False]
size = 16
error return = False
current state = False

truth_table: [ True  True False False False False False False False False False False
  True False False False]
size = 16
error return = False
current state = False



Expected ... 

FALSE MEANS TURNED ON

| False | False | False | False | False | False | True | 

| True | False | False | True | True | True | True | 

| False | False | True | False | False | True | False | 

| False | False | False | False | True | True | False | 

| True | False | False | True | True | False | False | 

| False | True | False | False | True | False | False | 

| False | True | False | False | False | False | False | 

| False | False | False | True | True | True | False | 

| False | False | False | False | False | False | False | 

| False | False | False | True | True | False | False | 

| False | False | False | True | False | False | False | 

| True | True | False | False | False | False | False | 

| False | True | True | False | False | False | True | 

| True | False | False | False | False | True | False | 

| False | True | True | False | False | False | False | 

| False | True | True | True | False | False | False | 

FALSE MEANS TURNED ON

Process finished with exit code 0


"""
