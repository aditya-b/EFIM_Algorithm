from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
from time import sleep
import MiniProject

ip_global = None
op_global = None
util_global = None
trans_global = None
done = False


def start_background_thread():
    global ip_global, op_global, util_global, trans_global, done
    while ip_global is None or op_global is None or util_global is None or trans_global is None:
        sleep(5)
    MiniProject.preprocess_data(ip_global, op_global, util_global, trans_global)
    done = True


class GUI(Frame):
    def __init__(self, master=None, algo_thread=None):
        Frame.__init__(self, master)
        self.input_file = ''
        self.algo_thread = algo_thread
        self.master.title("EFIM Algorithm")
        self.master.geometry("600x700")
        self.master.config(bg="black")
        self.master.resizable(0, 0)
        self.grid()
        self.label_id = StringVar()
        self.label = ttk.Label(master, textvariable=self.label_id, font="Arial 18 bold")
        self.label.config(background="black", foreground="white")
        self.label_id2 = StringVar()
        self.label2 = ttk.Label(master, textvariable=self.label_id2, font="Arial 12 bold")
        self.label2.config(background="black", foreground="white", justify=LEFT, anchor=W, wraplength=450)
        self.label_id.set("EFIM Algorithm: High Utility Itemset Mining")
        self.label_id2.set("The problem of high-utility itemset mining is to "
                           "find the itemsets (group of items) that generate a high "
                           "profit in a database, when they are sold "
                           "together. \n\nThe user has to provide a value for a "
                           "threshold called “minutil” (the minimum utility threshold).\n\nA high-utility itemset mining algorithm "
                           "outputs all the high-utility itemsets, that is the itemsets "
                           "that generates at least “minutil” profit.\n")
        self.frame = Frame(master, relief=RAISED, bg="black")
        self.label_output_id = StringVar()
        self.label_output = ttk.Label(self.frame, textvariable=self.label_output_id, background="black",
                                      foreground="white", font="Arial 10 bold")
        self.label_output_id.set("Output File Name:")
        self.label_output.grid(row=1, column=0, padx=5, pady=5)
        self.label_opext_id = StringVar()
        self.label_opext = ttk.Label(self.frame, textvariable=self.label_opext_id, background="black",
                                     foreground="white", font="Arial 10 bold")
        self.label_opext_id.set(".csv")
        self.label_opext.grid(row=1, column=2, padx=5, pady=5)
        self.opfile_id = StringVar()
        self.opfile = ttk.Entry(self.frame, textvariable=self.opfile_id)
        self.label_input_id = StringVar()
        self.label_input = ttk.Label(self.frame, textvariable=self.label_input_id, background="black",
                                     foreground="white", font="Arial 10 bold")
        self.label_input_id.set("Input File(.csv):")
        self.label_input.grid(row=0, column=0, padx=5, pady=5)
        self.ipfile_id = StringVar()
        self.ipfile = ttk.Label(self.frame, textvariable=self.ipfile_id)
        self.ipfile.config(background="black", foreground="white", font="TimesNewRoman 10 bold")
        self.label_util_id = StringVar()
        self.label_util = ttk.Label(self.frame, textvariable=self.label_util_id, background="black",
                                    foreground="white", font="Arial 10 bold")
        self.label_util_id.set("Minimum Utility:")
        self.label_util.grid(row=5, column=0, padx=5, pady=5)
        self.util_id = StringVar()
        self.util = ttk.Entry(self.frame, textvariable=self.util_id)
        self.def_op_id = IntVar()
        self.def_trans_id = IntVar()
        self.label_trans = Label(self.frame, background="black", foreground="white", font="Arial 10 bold",
                                 text="Transactions File Name:")
        self.label_trans.grid(row=3, column=0, padx=5, pady=5)
        self.label_trans_ext = Label(self.frame, background="black", foreground="white", font="Arial 10 bold",
                                     text=".csv")
        self.label_trans_ext.grid(row=3, column=2, padx=5, pady=5)
        self.transfile_id = StringVar()
        self.entry_trans = ttk.Entry(self.frame, textvariable=self.transfile_id)
        self.entry_trans.grid(row=3, column=1, padx=5, pady=5)
        self.pb = ttk.Progressbar(master, orient="horizontal", mode="indeterminate", length=400)
        self.running = True

        def print_text():
            util = self.util_id.get()
            ip = self.input_file
            op = self.opfile_id.get()
            trans = self.transfile_id.get()
            if ip[-3:] != "csv":
                messagebox.showerror("Input File Error", "Select only .csv files!")
            elif op == '':
                messagebox.showerror("Output File Error", "Enter output file name or select 'Use Default' option!")
            elif util == '':
                messagebox.showerror("Utility Error", "Enter minimum utility!")
            elif trans == '':
                messagebox.showerror("Transactions File Error",
                                     "Enter transactions file name or select 'Use Default' option!")
            else:
                op = "/".join((ip.split("/"))[:-1]) + "/" + op + ".csv"
                trans = "/".join((ip.split("/"))[:-1]) + "/" + trans + ".csv"
                try:
                    global ip_global, op_global, util_global, trans_global, done
                    ip_global = ip
                    op_global = op
                    util_global = util
                    trans_global = trans
                    self.pb.start()
                    self.algo_thread.start()
                    self.after(500, lambda: self.checkThread(trans, op))
                except Exception as e:
                    messagebox.showerror("Error", "Message: " + str(e))
                    self.pb.destroy()

        def get_file_name():
            file_name = filedialog.askopenfilename()
            self.ipfile_id.set(file_name[:25] + '...')
            self.input_file = file_name

        def def_op_file():
            if self.def_op_id.get() == 1:
                self.opfile_id.set("Results")
            else:
                self.opfile_id.set("")

        def def_trans_file():
            if self.def_trans_id.get() == 1:
                self.transfile_id.set("Transactions")
            else:
                self.transfile_id.set("")

        self.check_trans = Checkbutton(self.frame, command=def_trans_file, text="Use Default (Transactions.csv)",
                                       onvalue=1,
                                       offvalue=0, bg="black", fg="white",
                                       selectcolor="black", variable=self.def_trans_id, activebackground="black",
                                       activeforeground="white")
        self.check_trans.grid(row=4, column=1, padx=5, pady=5)
        self.opfile_checkbox = Checkbutton(self.frame, command=def_op_file, text="Use Default (Results.csv)", onvalue=1,
                                           offvalue=0, bg="black", fg="white",
                                           selectcolor="black", variable=self.def_op_id, activebackground="black",
                                           activeforeground="white")
        self.opfile_checkbox.grid(row=2, column=1, padx=5, pady=5)
        self.button2 = ttk.Button(self.frame, command=get_file_name, text="Open File")
        self.button = ttk.Button(master, command=print_text, text="Get Itemsets")
        self.pack()
        self.label.pack(padx=5, pady=30)
        self.label2.pack(padx=5, pady=10)
        self.frame.pack(padx=5, pady=5)
        self.ipfile.grid(row=0, column=1, padx=5, pady=5)
        self.opfile.grid(row=1, column=1, padx=5, pady=5)
        self.util.grid(row=5, column=1, padx=5, pady=5)
        self.button.pack(padx=5, pady=5)
        self.button2.grid(row=0, column=2, padx=5, pady=5)
        self.pb.pack(padx=10, pady=20)


    def checkThread(self, trans, op):
        if self.algo_thread.isAlive():
            self.after(500, lambda: self.checkThread(trans, op))
            return
        else:
            self.pb.destroy()
            messagebox._show("Success",
                             "Transactions written to file " + trans + "\n\nResults written to file " + op)
            messagebox._show("Thank you!",
                                         "Thank you for using EFIM Algorithm!")
            self.master.destroy()



algorithm_thread = Thread(name="Algorithm Thread", target=start_background_thread)
frame = GUI(algo_thread=algorithm_thread)
frame.mainloop()