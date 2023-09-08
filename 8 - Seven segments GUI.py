"""
Assignment 8, by Leonardo Blas.
08/01/2019.
In this assignment we will implement our previously created program,
Assignment 7, into a GUI, using tkinter and the canvas widget.
"""
import tkinter as tk
import tkinter.messagebox as tkmb

import sev_seg_logic as ssl


def main():
    root_win = tk.Tk()
    demo_cls_ref = SevenSegmentGUI(root_win)
    demo_cls_ref.get_root().title("Seven Segment Display")
    demo_cls_ref.get_root().mainloop()


class SevenSegmentGUI:
    INITIAL_DIG = 0
    INITIAL_CAN_WIDTH = 150
    INITIAL_CAN_HEIGHT = 200
    HILITE_PAD = 0
    BAD_USER_INPUT = -1
    ERROR_INT = 14  # Matches with E
    MIN_INPUT = 0
    MAX_INPUT = 15

    # constructor
    def __init__(self, mstr_rt=None):
        self.digit_to_show = self.INITIAL_DIG
        self.cnv_w = self.INITIAL_CAN_WIDTH
        self.cnv_h = self.INITIAL_CAN_HEIGHT
        self.sev_seg_logic = ssl.SevenSegmentLogic()

        # -------------- store root reference locally --------------
        if not self.set_root(mstr_rt):
            stand_in = tk.Tk()
            self.set_root(stand_in)

        # --------- a container frame and subframes ----------------
        self.container = tk.Frame(self.root, bg="lightblue",
                                  padx=10, pady=10)
        self.title_frame = tk.Frame(self.container, bg="lightgreen")
        self.work_frame = tk.Frame(self.container, bg="lightblue")
        self.canvas_frame = tk.Frame(self.container, bg="black",
                                     padx=3, pady=3)

        # -------------- one message widget ------------------------
        header = "Enter a hex digit to display on the 7-seg display." \
                 " (0, ..., 9, A, ...,  F)"
        self.msg_head = tk.Message(self.title_frame, text=header)
        self.msg_head.config(font=("times", 12, "bold"),
                             bg="lightgreen", width=300)

        # ----------------- some label widgets ------------------
        self.lab_digit = tk.Label(self.work_frame, text="Digit:",
                                  padx=20, pady=10, bg="lightblue")

        # ----------------- some entry widgets ------------------
        self.enter_digit = tk.Entry(self.work_frame)
        self.enter_digit.insert(0, str(self.digit_to_show))
        self.enter_digit.bind('<Return>', self.update_canvas)

        # ----------------- the canvas widget ------------------
        self.canvas = tk.Canvas(
            self.canvas_frame, width=self.cnv_w, height=self.cnv_h, \
            bg="dark green", highlightthickness=self.HILITE_PAD)

        # ------- place widgets using pack and grid layout ---------
        self.container.pack(expand=True, fill=tk.BOTH)
        self.canvas_frame.pack(side="right", expand=True, fill=tk.BOTH)
        self.title_frame.pack(expand=True, fill=tk.BOTH)
        self.work_frame.pack(expand=True, fill=tk.BOTH)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.msg_head.pack(expand=True, fill=tk.BOTH)

        self.lab_digit.grid(row=0, column=0, sticky=tk.E)
        self.enter_digit.grid(row=0, column=1, sticky=tk.W)

        # -- update dimensions when resized (including 1st time)  --
        self.canvas.bind('<Configure>', self.resize_can)

    # mutators
    def set_root(self, rt):
        if self.valid_tk_root(rt):
            self.root = rt
            return True
        # else
        return False

    def set_title(self, title):
        if type(title) == str:
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
        if type(am_i_a_root) == tk.Tk:
            return True
        # else
        return False

    # bound event handler gets new dimensions and redraws when resized
    def resize_can(self, event):
        # without 2 * hilight pad, get runaway wnidow
        self.cnv_w = float(event.width) - (2 * self.HILITE_PAD)
        self.cnv_h = float(event.height) - (2 * self.HILITE_PAD)

        # change the size, then redraw everything (alt: Canvas's scale())
        self.canvas.configure(width=self.cnv_w, height=self.cnv_h)
        self.update_canvas()

    @classmethod
    def convert_hex_char_to_int(cls, input):
        """
        Converts string input into hexadecimal ints from 0 to 15.
        :param input: str
        :return: int
        """
        hex_base = 16
        if type(input) is str \
                and len(input) is 1:
            try:
                int_input = int(input, hex_base)
            except ValueError:
                return cls.BAD_USER_INPUT
            if cls.MIN_INPUT <= int_input <= cls.MAX_INPUT:
                return int_input
        return cls.BAD_USER_INPUT

    # canvas updater
    def update_canvas(self, *args):
        """
        Implementation of the canvas widget and functionality.
        :param args:
        :return: no return
        """
        self.canvas.delete("all")
        CLICK = .02
        CAP = .0175
        LEN = .3
        TL_X = .35
        TL_Y = .15
        SLANT = .04
        v_fun = self.draw_vert_seg
        h_fun = self.draw_horiz_seg
        xyfunc_list = [
            # top horiz (seg_a)
            (TL_X + CLICK, TL_Y, h_fun),
            # upper right vert (seg_b)
            (TL_X + LEN + (2 * CAP) + (2 * CLICK), TL_Y, v_fun),
            # lower right vert (seg_c)
            (TL_X - SLANT + LEN + (2 * CAP) + (2 * CLICK),
             TL_Y + LEN + (2 * CAP), v_fun),
            # bottom horiz (seg_d)
            (TL_X - (2 * SLANT) + CLICK, TL_Y + (2 * LEN) + (4 * CAP), h_fun),
            # lower left vert (seg_e)
            (TL_X - SLANT, TL_Y + LEN + (2 * CAP), v_fun),
            # upper left vert (seg_f)
            (TL_X, TL_Y, v_fun),
            # middle horiz (seg_g)
            (TL_X - SLANT + CLICK, TL_Y + LEN + (2 * CAP), h_fun)
        ]
        simulated_user_str = self.enter_digit.get()
        user_int = self.convert_hex_char_to_int(simulated_user_str)
        if user_int == self.BAD_USER_INPUT:
            tkmb.showerror('Error',
                           "Single (Hex) Digits (as a string) Only, Please.")
            self.sev_seg_logic.eval(self.ERROR_INT)
            for k in range(7):
                if self.sev_seg_logic.get_val_of_seg(k):
                    xyfunc_list[k][2](xyfunc_list[k][0], xyfunc_list[k][1],
                                      LEN, CAP, SLANT)
        else:
            self.sev_seg_logic.eval(user_int)
            for k in range(7):
                if self.sev_seg_logic.get_val_of_seg(k):
                    xyfunc_list[k][2](xyfunc_list[k][0], xyfunc_list[k][1],
                                      LEN, CAP, SLANT)

    def draw_vert_seg(self, x, y, len, end, slant):
        # tall, narrow hexagon
        points = [
            x * self.cnv_w,
            y * self.cnv_h,
            (x - end) * self.cnv_w,
            (y + end) * self.cnv_h,
            (x - end - slant) * self.cnv_w,
            (y + end + len) * self.cnv_h,
            (x - slant) * self.cnv_w,
            (y + len + (2 * end)) * self.cnv_h,
            (x + end - slant) * self.cnv_w,
            (y + end + len) * self.cnv_h,
            (x + end) * self.cnv_w,
            (y + end) * self.cnv_h
        ]
        self.canvas.create_polygon(points, fill='greenyellow', width=0)

    def draw_horiz_seg(self, x, y, len, end, dummy=None):
        """ last param is to make signature match draw_vert_seg()
        for next phase -- horiz segs don't have slants """
        # long, thin hexagon
        points = [
            x * self.cnv_w,
            y * self.cnv_h,
            (x + end) * self.cnv_w,
            (y + end) * self.cnv_h,
            (x + end + len) * self.cnv_w,
            (y + end) * self.cnv_h,
            (x + len + (2 * end)) * self.cnv_w,
            y * self.cnv_h,
            (x + end + len) * self.cnv_w,
            (y - end) * self.cnv_h,
            (x + end) * self.cnv_w,
            (y - end) * self.cnv_h
        ]
        self.canvas.create_polygon(points, fill='greenyellow', width=0)


# -------------- main program -------------------
if __name__ == "__main__":
    main()
