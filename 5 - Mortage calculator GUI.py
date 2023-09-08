"""
Assignment 5, by Leonardo Blas.
07/15/2019.
In this assignment we will reuse our modules' DemoGui class as a base to
construct the MortgageGui class. The purpose of this GUI is to calculate
financial properties of mortgages. Some of the changes performed to the
modules' provided code, as well as new code include:

New Code:
Body of the compute_show_ and update_answer() methods in the MortgageGui class.

Renamed:
MortgageData's ORIGINAL_DEFAULT_PRINC to ORIGINAL_DEFAULT_PRICE
"""

import locale
import tkinter as tk
import tkinter.messagebox as tkmb
from enum import Enum

import math

locale.setlocale(locale.LC_ALL, '')


def main():
    root_win = tk.Tk()
    demo_cls_ref = MortgageGui(root_win)
    demo_cls_ref.get_root().title("Calculator GUI")
    demo_cls_ref.get_root().mainloop()


class MortgageData:
    # class ("static") intended constants
    MIN_LOAN = 0
    MAX_LOAN = 100000000
    MIN_RATE = 0.0
    MAX_RATE = 25.0
    MIN_YRS = 0
    MAX_YRS = 100
    MIN_PMT = 0.
    MAX_PMT = MAX_LOAN / 10
    MIN_STRING_LENGTH = 1
    MAX_STRING_LENGTH = 50
    ORIGINAL_DEFAULT_PRICE = 200000.
    ORIGINAL_DEFAULT_RATE = 4.5
    ORIGINAL_DEFAULT_YEARS = 30
    ORIGINAL_DEFAULT_PMT = 1013.37

    # class attributes that will change over time
    default_principal = ORIGINAL_DEFAULT_PRICE
    default_rate = ORIGINAL_DEFAULT_RATE
    default_years = ORIGINAL_DEFAULT_YEARS
    default_payment = ORIGINAL_DEFAULT_PMT

    # initializer ("constructor") method -------------------------------
    def __init__(self,
                 principal=None,
                 rate=None,
                 years=None,
                 payment=None):

        # repair mutable defaults
        if principal is None:
            principal = self.default_principal
        if rate is None:
            rate = self.default_rate
        if years is None:
            years = self.default_years
        if payment is None:
            payment = self.default_payment

        # instance attributes
        if not self.set_principal(principal):
            self.principal = self.default_principal
        if not self.set_rate(rate):
            self.rate = self.default_rate
        if not self.set_years(years):
            self.years = self.default_years
        if not self.set_payment(payment):
            self.payment = self.default_payment

    # mutators -----------------------------------------------
    def set_principal(self, principal):
        if not self.valid_principal(principal):
            return False
        # else
        self.principal = principal
        return True

    def set_rate(self, rate):
        if not self.valid_rate(rate):
            return False
        # else
        self.rate = rate
        return True

    def set_years(self, years):
        if not self.valid_years(years):
            return False
        # else
        self.years = years
        return True

    def set_payment(self, payment):
        if not self.valid_payment(payment):
            return False
        # else
        self.payment = payment
        return True

    # accessors -----------------------------------------------
    def get_principal(self):
        return self.principal

    def get_rate(self):
        return self.rate

    def get_years(self):
        return self.years

    def get_payment(self):
        return self.payment

    # instance helpers -------------------------------
    def __str__(self):
        separator = " --- "
        loan_nice = locale.currency(self.principal, grouping=True)

        ret_str = ((separator
                    + "\n    loan amount: {}"
                    + "\n    annual rate: {:8.2f}%"
                    + "\n    duration: {} years.").
                   format(loan_nice, self.rate, self.years))
        return ret_str

    # static and class helpers -------------------------------
    @classmethod
    def valid_string(cls, the_str):
        if (type(the_str) != str
                or
                not
                (cls.MIN_STRING_LENGTH <= len(the_str)
                 <= cls.MAX_STRING_LENGTH)):
            return False
        # else
        return True

    @classmethod
    def valid_principal(cls, prin_in):
        if (
                (type(prin_in) != float and type(prin_in) != int)
                or
                not (cls.MIN_LOAN <= prin_in <= cls.MAX_LOAN)
        ):
            return False
        # else)
        return True

    @classmethod
    def valid_rate(cls, rate_in):
        if (
                (type(rate_in) != float and type(rate_in) != int)
                or
                not (cls.MIN_RATE <= rate_in <= cls.MAX_RATE)
        ):
            return False
        # else
        return True

    @classmethod
    def valid_years(cls, yrs_in):
        if (
                (type(yrs_in) != float and type(yrs_in) != int)
                or
                not (cls.MIN_YRS <= yrs_in <= cls.MAX_YRS)
        ):
            return False
        # else
        return True

    @classmethod
    def valid_payment(cls, pmt_in):
        if (
                (type(pmt_in) != float and type(pmt_in) != int)
                or
                not (cls.MIN_PMT <= pmt_in <= cls.MAX_PMT)
        ):
            return False
        # else
        return True

    # class mutators and accessors ----------------------------
    @classmethod
    def set_default_principal(cls, new_prin):
        if not cls.valid_principal(new_prin):
            return False
        # else
        cls.default_principal = new_prin
        return True

    @classmethod
    def set_default_rate(cls, new_rate):
        if not cls.valid_rate(new_rate):
            return False
        # else
        cls.default_rate = new_rate
        return True

    @classmethod
    def set_default_years(cls, new_years):
        if not cls.valid_years(new_years):
            return False
        # else
        cls.default_years = new_years
        return True

    @classmethod
    def set_default_payment(cls, new_pmt):
        if not cls.valid_payment(new_pmt):
            return False
        # else
        cls.default_payment = new_pmt
        return True

    @classmethod
    def get_default_principal(cls):
        return cls.default_principal

    @classmethod
    def get_default_years(cls):
        return cls.default_years

    @classmethod
    def get_default_rate(cls):
        return cls.default_rate

    @classmethod
    def get_default_payment(cls):
        return cls.default_payment


class MortgageCalc:
    def __init__(self):
        self.the_loan = MortgageData()
        self.clear()

    # static helper initializer ----------------------------------
    @staticmethod
    def zero_out_md_defaults():
        MortgageData.set_default_principal(0)
        MortgageData.set_default_rate(0)
        MortgageData.set_default_years(0)
        MortgageData.set_default_payment(0)

    # mutators/accessors -----------------------------------------
    """ note that mutators don't store data here, but in the_loan """

    def clear(self):
        self.set_principal(0)
        self.set_rate(0.0)
        self.set_years(0)
        self.set_payment(0.0)

    def set_principal(self, principal):
        return self.the_loan.set_principal(principal)

    def set_rate(self, rate):
        return self.the_loan.set_rate(rate)

    def set_years(self, years):
        return self.the_loan.set_years(years)

    def set_payment(self, payment):
        return self.the_loan.set_payment(payment)

    def get_principal(self):
        return self.the_loan.get_principal()

    def get_rate(self):
        return self.the_loan.get_rate()

    def get_years(self):
        return self.the_loan.get_years()

    def get_payment(self):
        return self.the_loan.get_payment()

    def compute_monthly_payment(self):
        """ mtg_data assumed to reference a MortgageData object """
        mtg_principal, mtg_annual_rate, mtg_years \
            = \
            self.the_loan.get_principal(), \
            self.the_loan.get_rate(), \
            self.the_loan.get_years()

        # convert years to months
        months = mtg_years * 12.

        # convert rate to decimal and months
        monthly_rate = mtg_annual_rate / (100. * 12.)

        # use formula to get result
        temp = (1 + monthly_rate) ** months
        payment = mtg_principal * monthly_rate * temp / (temp - 1)
        self.set_payment(payment)
        return True

    def compute_principal(self):
        """ mtg_data assumed to reference a MortgageData object """
        mtg_payment, mtg_annual_rate, mtg_years \
            = \
            self.the_loan.get_payment(), \
            self.the_loan.get_rate(), \
            self.the_loan.get_years()

        # convert years to months
        months = mtg_years * 12

        # convert rate to decimal and months
        monthly_rate = mtg_annual_rate / (100. * 12.)

        # use formula to get result
        temp = (1 + monthly_rate) ** months
        principal = mtg_payment * (temp - 1) / (monthly_rate * temp)
        self.set_principal(principal)
        return True

    def compute_years(self):
        """ mtg_data assumed to reference a MortgageData object """
        mtg_principal, mtg_annual_rate, mtg_payment \
            = \
            self.the_loan.get_principal(), \
            self.the_loan.get_rate(), \
            self.the_loan.get_payment()

        # convert rate to decimal and months
        monthly_rate = mtg_annual_rate / (100. * 12.)

        # use formula to get result
        temp = mtg_payment / (mtg_payment - (mtg_principal * monthly_rate))

        # use formula to get result (if unreasonable answer, exception)
        temp = mtg_payment / (mtg_payment - (mtg_principal * monthly_rate))
        try:
            months = math.log(temp, 1 + monthly_rate)
        except ValueError:
            return False

        # bad inputs -- pay too much after one month
        if months < 1:
            return False

        # convert months to years
        years = months / 12.

        self.set_years(years)
        return True

    def compute_rate(self):
        """ uses formula Monthly Pmt, M =  (i*P)/(1 - (1 + i)^(-n))
        solves for i using successive approx (newton's method)
        WARNING - floating accuracy gives incorrect alerts in
        the 14% - 20% range depending on the loan term.  """

        mtg_principal, mtg_years, mtg_payment \
            = \
            self.the_loan.get_principal(), \
            self.the_loan.get_years(), \
            self.the_loan.get_payment()

        # convert years to months
        months = mtg_years * 12

        # for short formulas
        p, n, m = mtg_principal, months, mtg_payment

        # nested functions, f(i) and f_primt(i) (latter f')
        def f(i):
            return m - m * ((1 + i) ** (-n)) - i * p

        def f_prime(i):
            return n * m * ((1 + i) ** (-n - 1)) - p

        # check for  pmt too small (0% rate won't work) or
        # too large (first monthly payment >= principal)
        if m * n < p:
            return False

        # loop until error is < EPSILON or fail after 100
        EPSILON = .000000001  # error tolerance
        INIT_INT_APPROX = .00417  # about 5%

        i = INIT_INT_APPROX
        found = False
        for k in range(100):
            i_prev = i
            i = i_prev - f(i_prev) / f_prime(i_prev)
            if abs(i - i_prev) < EPSILON and i > 0:
                found = True
                break

        # check for non-convergence of algorithm or incompat input
        # (also gives bad values if high % rates should be found)
        if not found or i < EPSILON or i > self.the_loan.MAX_RATE:
            return False

        monthly_dec_rate = i

        # convert mo dec rate to annual pct
        rate = monthly_dec_rate * (100. * 12.)
        self.set_rate(rate)
        return True


class MortgageGui:
    """ refinement using dictionaries and lists for 4 ops  """

    # nested enum for operation choices -----------------------
    class MtgVars(Enum):
        PRIN = 1
        RATE = 2
        YEARS = 3
        PMT = 4

    unk_text = ['(error)', 'Principal ($)', 'Interest Rate (%)',
                'Term (Years)', 'Monthly Payment ($)']

    # some class constants for calculator
    INIT_UNKNOWN = MtgVars.YEARS
    TTL_CLR, WRK_CLR, ANS_CLR, OPT_CLR_RAD, OPT_CLR_FRM = \
        "lightgreen", "lightblue", "yellowgreen", \
        "dodgerblue", "mediumspringgreen"

    # constructor
    def __init__(self, mstr_rt=None):
        # mortgage calculator object (for computations)
        self.mtg_calc = MortgageCalc()
        # define state variables - values that affect the GUI behavior
        self.current_unknown = self.INIT_UNKNOWN  # operation (start w/PRIN)
        self.answer = 0  # val replaced in update_answer()
        self.options_win = None  # prevent > 1 ops win opened

        # ----- state variables for operation/option choices -------
        # some local vars to keep instructions simple
        unk_val_int = self.current_unknown.value
        unk_val_txt = self.unk_text[unk_val_int]
        unk_val_header_str = f'Enter your three loan requirements and I\'ll ' \
            f'compute the {unk_val_txt} from them.'

        # define state variables - values that affect the GUI behavior
        self.state_cur_unk_int = tk.IntVar()
        self.state_cur_unk_txt = tk.StringVar()
        self.state_cur_button_txt = tk.StringVar()
        self.state_cur_instr_txt = tk.StringVar()
        self.state_cur_ans = tk.StringVar()

        # load state variables with values
        self.state_cur_unk_int.set(unk_val_int)
        self.state_cur_unk_txt.set(unk_val_txt.title())  # up 1st let
        self.state_cur_button_txt.set("Show " + unk_val_txt.title())
        self.state_cur_ans.set(str(self.answer))
        self.state_cur_instr_txt.set(unk_val_header_str)

        # -------------- store root reference locally --------------
        if not self.set_root(mstr_rt):
            stand_in = tk.Tk()
            self.set_root(stand_in)

        # --------- a container frame and subframes ------------
        self.container = tk.Frame(self.root, bg=self.WRK_CLR, padx=5)
        self.title_frame = tk.Frame(self.container, bg=self.TTL_CLR)
        self.work_frame = tk.Frame(self.container, bg=self.WRK_CLR)
        self.answer_frame = tk.Frame(self.container, bg=self.ANS_CLR)

        # -------------- one message widget ------------------------
        self.msg_head = tk.Message(self.title_frame)
        self.msg_head.config(font=("times", 12, "bold"),
                             bg=self.TTL_CLR, width=300)
        self.msg_head.config(textvariable=self.state_cur_instr_txt)

        # ----------------- some label widgets -------------------
        principal_string = f'Principal:\n(dollars\n' \
            f'{MortgageData.MIN_LOAN} - {MortgageData.MAX_LOAN})'
        interest_string = f'Interest Rate:\n' \
            f'(in percent, but no % sign\n' \
            f'{MortgageData.MIN_RATE} - {MortgageData.MAX_RATE})'
        term_string = f'Term:\n(years, fractions okay\n' \
            f'{MortgageData.MIN_YRS} - {MortgageData.MAX_YRS})'
        payment_string = f'Monthly Payment: (dollars.cents\n' \
            f'{MortgageData.MIN_PMT} - {MortgageData.MAX_PMT})'
        self.lab_num_prin = tk.Label(self.work_frame, text=principal_string,
                                     padx=20, pady=10, bg=self.WRK_CLR)
        self.lab_num_rate = tk.Label(self.work_frame, text=interest_string,
                                     padx=20, pady=10, bg=self.WRK_CLR)
        self.lab_num_years = tk.Label(self.work_frame, text=term_string,
                                      padx=20, pady=10, bg=self.WRK_CLR)
        self.lab_num_payment = tk.Label(self.work_frame, text=payment_string,
                                        padx=20, pady=10, bg=self.WRK_CLR)
        self.lab_txt_answer = tk.Label(self.answer_frame, text="Answer:",
                                       padx=20, pady=10, bg=self.ANS_CLR)
        self.lab_num_answer = tk.Label(self.answer_frame,
                                       textvariable=self.state_cur_ans,
                                       padx=20, pady=10, bg=self.ANS_CLR)

        # ----------------- some entry widgets -------------------
        self.enter_prin = tk.Entry(self.work_frame)
        self.enter_prin.insert(0, str(MortgageData.get_default_principal()))
        self.enter_rate = tk.Entry(self.work_frame)
        self.enter_rate.insert(0, str(MortgageData.get_default_rate()))
        self.enter_years = tk.Entry(self.work_frame)
        self.enter_years.insert(0, MortgageData.get_default_years())
        self.enter_payment = tk.Entry(self.work_frame)
        self.enter_payment.insert(0, str(MortgageData.get_default_payment()))

        # ----------------- some button widgets -------------------
        self.but_quit = tk.Button(self.answer_frame, text="Quit",
                                  command=self.end_my_gui)
        self.but_comp_unknown = tk.Button(self.answer_frame,
                                          textvariable=
                                          self.state_cur_button_txt,
                                          command=self.update_answer)
        self.but_options = tk.Button(self.answer_frame, text="More Options",
                                     command=self.open_options_win)

        # ------- place widgets using pack and grid layout ---------
        self.container.pack(expand=True, fill=tk.BOTH)
        self.title_frame.pack(expand=True, fill=tk.BOTH)
        self.work_frame.pack(expand=True, fill=tk.BOTH)
        self.answer_frame.pack(expand=True, fill=tk.BOTH)

        self.msg_head.pack()

        self.lab_num_prin.grid(row=0, column=0, sticky=tk.E)
        self.lab_num_rate.grid(row=1, column=0, sticky=tk.E)
        self.lab_num_years.grid(row=0, column=2, sticky=tk.E)
        self.lab_num_payment.grid(row=1, column=2, sticky=tk.E)

        self.enter_prin.grid(row=0, column=1, sticky=tk.W)
        self.enter_rate.grid(row=1, column=1, sticky=tk.W)
        self.enter_years.grid(row=0, column=3, sticky=tk.W)
        self.enter_payment.grid(row=1, column=3, sticky=tk.W)

        self.lab_num_answer.pack(side=tk.RIGHT)
        self.lab_txt_answer.pack(side=tk.RIGHT)

        self.but_comp_unknown.pack(side=tk.RIGHT)
        self.but_options.pack(side=tk.RIGHT)
        self.but_quit.pack(side=tk.LEFT)

        #  ------ bind the close "x" to the quit handler, too -----
        self.root.protocol("WM_DELETE_WINDOW", self.end_my_gui)

        # ------ update the answer using init values for x and y ---
        self.update_answer()

    # mutators
    def set_root(self, rt):
        if MortgageGui.valid_tk_root(rt):
            self.root = rt
            return True
        # else
        return False

    def set_title(self, title):
        if type(title) is str:
            self.root.title = title
            return True
        # else
        return False

    # accessor
    def get_root(self):
        return self.root

    # static helper
    @staticmethod
    def valid_tk_root(am_i_a_root):
        if type(am_i_a_root) is tk.Tk:
            return True
        # else
        return False

    # event handlers
    def update_answer(self):
        RNG_ERR = " is out of range"
        try:
            if self.current_unknown != self.MtgVars.PRIN:
                val = float(self.enter_prin.get())
                if not self.mtg_calc.set_principal(val):
                    tkmb.showerror("Input Error", "PRINCIPAL" + RNG_ERR)
                    return
            if self.current_unknown != self.MtgVars.RATE:
                val = float(self.enter_rate.get())
                if not self.mtg_calc.set_rate(val):
                    tkmb.showerror("Input Error", "RATE" + RNG_ERR)
                    return
            if self.current_unknown != self.MtgVars.YEARS:
                val = float(self.enter_years.get())
                if not self.mtg_calc.set_years(val):
                    tkmb.showerror("Input Error", "YEARS" + RNG_ERR)
                    return
            if self.current_unknown != self.MtgVars.PMT:
                val = float(self.enter_payment.get())
                if not self.mtg_calc.set_payment(val):
                    tkmb.showerror("Input Error", "PAYMENT" + RNG_ERR)
                    return
        except (ValueError, TypeError, IndexError):
            tkmb.showerror("Input Error", "Please enter a valid "
                                          "number in all 3 editable entry "
                                          "fields")
            return
        try:
            if self.current_unknown == self.MtgVars.PRIN:
                self.compute_show_principal()
            elif self.current_unknown == self.MtgVars.RATE:
                self.compute_show_rate()
            elif self.current_unknown == self.MtgVars.YEARS:
                self.compute_show_years()
            elif self.current_unknown == self.MtgVars.PMT:
                self.compute_show_payment()
        except ZeroDivisionError:
            tkmb.showerror("Input Error", "Cannot divide by zero")
            return

    def end_my_gui(self):
        confirm_quit = "Are you sure you want to quit?"
        if (
                tkmb.askokcancel("End GUI", confirm_quit)
        ):
            self.root.destroy()  # close the window

    def open_options_win(self):
        # nested functions ------------------------------------
        def options_save():
            unk_val_int = self.state_cur_unk_int.get()
            unk_val_txt = self.unk_text[unk_val_int]
            unk_val_header_str = f'Enter your three loan requirements and ' \
                f'I\'ll compute the {unk_val_txt} from them.'

            # load state text with new values based on radio buttons
            self.state_cur_unk_int.set(unk_val_int)
            self.state_cur_unk_txt.set(unk_val_txt.title())  # up 1st let
            self.state_cur_button_txt.set("Show " + unk_val_txt.title())
            self.state_cur_ans.set(str(self.answer))
            self.state_cur_instr_txt.set(unk_val_header_str)

            # update the master int op state
            self.current_unknown = self.MtgVars(unk_val_int)  # an enum
            self.update_answer()
            self.options_win.destroy()
            self.options_win = None

        def options_cancel():
            # restore the radio button state var to master op
            self.state_cur_unk_int.set(self.current_unknown.value)
            self.options_win.destroy()
            self.options_win = None

        def about_info():
            # sample list of information - could be used for general output:
            credits = "Credits:\n Assignment 5, by Leonardo Blas." \
                      "\n Original Writer: Cheren Amadou"
            tkmb.showinfo("Credits", credits, parent=self.options_win)

        # end nested functions ------start def of open_options_win() ------

        # don't allow opening > 1 options win. if there, give it forcus
        if self.options_win:
            self.options_win.focus_force()
            return

        ops = [op for op in self.MtgVars]

        # spawn a child options window off root window:
        self.options_win = tk.Toplevel(self.root)

        # keeps option win above root even during possible about_win activity
        self.options_win.attributes("-topmost", True)

        # --------- container frame and subframes ------------
        container = tk.Frame(self.options_win, bg=self.OPT_CLR_FRM, padx=5)
        title_frame = tk.Frame(container, bg=self.OPT_CLR_FRM)
        work_frame = tk.Frame(container, bg=self.OPT_CLR_RAD)
        button_frame = tk.Frame(container, bg=self.OPT_CLR_FRM)

        # -------------- message widget for title ---------------
        instructions = 'Select an unknown value to\nbe computed from 3 others.'
        msg_head = tk.Message(title_frame, text=instructions)
        msg_head.config(font=("times", 10, "bold"),
                        bg=self.OPT_CLR_FRM, width=150)

        # -------------- radio btn widget for op ---------------
        op_buts = [
            tk.Radiobutton(work_frame,
                           text=ops[k].name, variable=self.state_cur_unk_int,
                           value=ops[k].value, padx=5, bg=self.OPT_CLR_RAD)
            for k in range(4)]

        # ----------------- some button widgets -------------------
        but_save = tk.Button(button_frame, text="Save",
                             command=options_save)
        but_cancel = tk.Button(button_frame, text="Cancel",
                               command=options_cancel)
        but_about = tk.Button(button_frame, text="About",
                              command=about_info)

        #  ------ bind the close "x" to the cancel handler, too -----
        self.options_win.protocol("WM_DELETE_WINDOW", options_cancel)

        # ------- place widgets using pack and grid layout ---------
        container.pack(expand=True, fill=tk.BOTH)
        title_frame.pack(expand=True, fill=tk.BOTH)
        work_frame.pack(expand=True, fill=tk.BOTH)
        button_frame.pack(expand=True, fill=tk.BOTH)

        msg_head.pack()

        for k in range(len(self.MtgVars.__members__.keys())):
            op_buts[k].pack(side=tk.LEFT, padx=20)

        but_save.pack(side=tk.LEFT, padx=20, pady=20)
        but_cancel.pack(side=tk.LEFT)
        but_about.pack(side=tk.RIGHT)

    def compute_show_principal(self):
        # Call compute method and set Entry to display answer.
        self.mtg_calc.compute_principal()
        self.answer = self.mtg_calc.get_principal()
        self.state_cur_ans.set(str(self.answer))
        self.enter_prin.delete(0, tk.END)
        self.enter_prin.insert(0, str(self.answer))

    def compute_show_rate(self):
        # Call compute method and set Entry to display answer.
        self.mtg_calc.compute_rate()
        self.answer = self.mtg_calc.get_rate()
        self.state_cur_ans.set(str(self.answer))
        self.enter_rate.delete(0, tk.END)
        self.enter_rate.insert(0, str(self.answer))

    def compute_show_years(self):
        # Call compute method and set Entry to display answer.
        self.mtg_calc.compute_years()
        self.answer = self.mtg_calc.get_years()
        self.state_cur_ans.set(str(self.answer))
        self.enter_years.delete(0, tk.END)
        self.enter_years.insert(0, str(self.answer))

    def compute_show_payment(self):
        # Call compute method and set Entry to display answer.
        self.mtg_calc.compute_monthly_payment()
        self.answer = self.mtg_calc.get_payment()
        self.state_cur_ans.set(str(self.answer))
        self.enter_payment.delete(0, tk.END)
        self.enter_payment.insert(0, str(self.answer))


# -------------- main program -------------------
if __name__ == "__main__":
    main()
