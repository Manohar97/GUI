from tkinter import *
import sys
import subprocess
import os
import fileinput
import configparser
from tkinter import filedialog
from tkinter import ttk


def execution(command):
    subprocess.call(command, shell=True)


class GuiWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.iconbitmap(self.dir_path + os.sep + "bluetooth.ico")
        self.title('Earbud Application')
        # self.geometry('1080x430')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        width = 1020
        height = 490
        # calculate position x and y coordinates
        x = (self.screen_width / 3.2) - (width / 2)
        y = (self.screen_height / 4.3) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.var = IntVar()

        self.notepad = ttk.Style()
        self.notepad.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [100, 10]},  "font": ('Calibri', '20', 'bold'),
                "map": {"background": [("selected", 'skyblue'),("!disabled", "white")],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        self.notepad.configure(self, foreground='white')
        self.notepad.theme_use("MyStyle")
        #"font": ('URW Gothic L', '11', 'bold')}} )
        self.notebook = ttk.Notebook(self)

        self.f1 = Frame(self.notebook, width=width, height=height)
        self.f2 = Frame(self.notebook, width=width, height=height)
        self.notebook.add(self.f1, text="Standard Setup")
        self.notebook.add(self.f2, text="DFU Setup")
        #notebook.grid(row=0, column=0, sticky="nw")
        # self.msg = Message(self, text="Please provide right paths in config file", aspect=1200)
        # self.msg.config(bg='light green', font=('Lucida Fax', 9, 'bold'))
        # self.msg.grid(row=0, column=1, padx=10, pady=3)
        self.browseToolkitLabel = LabelFrame(self, text='')
        self.encryption_label = LabelFrame(self, fg='blue', text='Unlock Encrypted Modules', font=('Helvetica', 11,
                                                                                                   'bold'))
        self.open_pydbg_label = LabelFrame(self, fg='blue', text='Utility', font=('Helvetica', 11, 'bold'))
        self.earbuddash_label = LabelFrame(self.f1, fg='blue', text='Open Sessions', font=('Helvetica', 11, 'bold'))
        self.earbuddash_label_dfu = LabelFrame(self.f2, fg='blue', text='Earbud Dash', font=('Helvetica', 11, 'bold'))
        self.session_label_dfu = LabelFrame(self.f2, fg='blue', text='Open sessions', font=('Helvetica', 11, 'bold'))

        #self.notebook.add(self.browseToolkitLabel, text="Generic")
        #self.notebook.add(self.encryption_label, text="Generic")
        #self.notebook.add(self.open_pydbg_label, text="Generic")
        #self.notebook.add(self.earbuddash_label_dfu, text="Generic")
        #self.notebook.add(self.session_label_dfu, text="Generic")

        self.browseToolkitLabel.place(x=3, y=55)
        self.encryption_label.place(x=3, y=180)
        self.open_pydbg_label.place(x=340, y=180)
        self.earbuddash_label_dfu.place(x=690, y=133)
        self.earbuddash_label.place(x=690, y=133)
        self.session_label_dfu.place(x=3, y=250)
        
        self.left_earbud_label = LabelFrame(self, fg='blue', text='Left Earbud', font=('Lucida Grande', 11, 'bold'))
        self.right_earbud_label = LabelFrame(self, fg='blue', text='Right Earbud', font=('Lucida Grande', 11, 'bold'))
        self.left_earbud_label.place(x=400, y=55)
        self.right_earbud_label.place(x=700, y=55)
        # self.left_earbud_label.grid_remove()
        # self.right_earbud_label.grid_remove()

        self.toolkit_button = Button(self.browseToolkitLabel, text="Browse ADK toolkit",
                                     command=self.toolkit_filedialog)
        self.toolkit_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="white",
                                   bg="navy", fg='white', font=('Helvetica', 11, 'bold'))
        self.toolkit_button.grid(column=2, row=0, padx=5, pady=5)
        self.toolkit_label = Label(self.browseToolkitLabel, text="")
        self.toolkit_label.grid(column=2, row=1)

        self.left_eb_trb_label = Label(self.left_earbud_label, text="TRB Port Number", font=('Times', 11))
        self.left_eb_trb_label.grid(column=0, row=3, padx=5, pady=5)

        self.left_eb_trb_val = Entry(self.left_earbud_label, width=10, font=('Helvetica', 11, 'bold'))
        self.left_eb_trb_val.grid(column=1, row=3, padx=5, pady=5)

        self.right_eb_trb_label = Label(self.right_earbud_label, text="TRB Port Number", font=('Times', 11))
        self.right_eb_trb_label.grid(column=1, row=0, padx=5, pady=5)

        self.right_eb_trb_val = Entry(self.right_earbud_label, width=10, font=('Helvetica', 11, 'bold'))
        self.right_eb_trb_val.grid(column=2, row=0, padx=5, pady=5)

        self.unlock_button = Button(self.encryption_label, text="Unlock TRB", command=self.unlock)
        # self.unlock_button.grid(row=2, column=0, padx=5, pady=3)
        self.unlock_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                  bg='navy', fg='white', font=('Helvetica', 11, 'bold'))
        self.encryption_label = Entry(self.encryption_label, width=35, font=('Helvetica', 11))
        # self.encryption_label.grid(column=0, row=3, padx=5, pady=5)

        self.pydbg_button_dfu = Button(self.session_label_dfu, text="Open cmds with pydbg sessions", command=self.open_cmds)
        # self.pydbg_button_dfu.grid(row=2, column=1, padx=80, pady=3)
        self.pydbg_button_dfu.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                 bg='navy', fg='white', font=('Helvetica', 11, 'bold'))

        self.pydbg_button = Button(self.earbuddash_label, text="Open cmds with pydbg sessions",
                                        command=self.get_default_elfpath)
        # self.pydbg_button.grid(row=2, column=1, padx=80, pady=3)
        self.pydbg_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                     bg='navy', fg='white', font=('Helvetica', 11, 'bold'))
        # self.open_pydbg_label = Radiobutton(self.open_pydbg_label, text='Before Upgrade', variable=self.var)
        # self.open_pydbg_label.grid(row=3, column=1, padx=80, pady=3)
        # self.open_pydbg_label = Radiobutton(self.open_pydbg_label, text='After Upgrade', variable=self.var)
        # self.open_pydbg_label.grid(column=1, row=4, padx=80, pady=3)

        self.dl_button = Button(self.open_pydbg_label, text="Open Dual logger prompt", command=self.dlcmd)
        # self.dl_button.grid(row=3, column=1, padx=80, pady=3)
        self.dl_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                              bg='navy', fg='white', font=('Helvetica', 11, 'bold'))

        self.flashimage_button = Button(self.open_pydbg_label, text="Flash Images", command=self.nvs_cmd_execution)
        # self.flashimage_button.grid(row=4, column=1, padx=80, pady=3)
        self.flashimage_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                      bg='navy', fg='white', font=('Helvetica', 11, 'bold'))

        # self.earbuddash_button = Button(self.earbuddash_label_dfu, text="Earbud Dash", command=self.earbuddash)
        # self.earbuddash_button.grid(row=5, column=1, padx=80, pady=3)
        # self.earbuddash_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
        #                              bg='navy',fg = 'white', font=('Helvetica', 11, 'bold'))
        self.earbuddash_button = Button(self.earbuddash_label, text="Open Earbud dash",
                                         command=self.before_upgrade)
        self.earbuddash_button.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                       bg='navy', fg='white', font=('Helvetica', 11, 'bold'))
        self.earbuddash_button1 = Button(self.earbuddash_label_dfu, text="Before upgrade image",
                                         command=self.before_upgrade)
        self.earbuddash_button1.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                       bg='navy', fg='white', font=('Helvetica', 11, 'bold'))
        # self.earbuddash_button1.grid(row=0, column=1, padx=20, pady=3)
        self.earbuddash_button2 = Button(self.earbuddash_label_dfu, text="After upgrade image", command=self.after_upgrade)
        # self.earbuddash_button2.grid(row=1, column=1, padx=10, pady=3)
        self.earbuddash_button2.config(width=30, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                       bg='navy', fg='white', font=('Helvetica', 11, 'bold'))

        self.session_button1 = Radiobutton(self.session_label_dfu, text="Before upgrade image", width=30, height=3,
                                          variable=self.var, value=1, command=self.get_before_elfpath,
                                          activebackground='green', activeforeground="black",
                                          font=('Helvetica', 10, 'bold'))
        # self.session_button1.grid()
        self.session_button2 = Radiobutton(self.session_label_dfu, text="After upgrade image", width=30, height=3,
                                          variable=self.var, value=2, command=self.get_after_elfpath,
                                          activebackground='green', activeforeground="black",
                                          font=('Helvetica', 10, 'bold'))
        # self.session_button2.grid()
        self.quit_button = Button(self, text="Quit", command=sys.exit)
        self.quit_button.place(x=825, y=435)
        self.quit_button.config(width=20, height=2, activebackground='Cornflowerblue', activeforeground="black",
                                bg="coral2", font=('Helvetica', 11, 'bold'))

        # self.left_earbud_label.grid_remove()
        # self.right_earbud_label.grid_remove()
        # self.left_eb_trb_label.grid_remove()
        # self.left_eb_trb_val.grid_remove()
        # self.right_eb_trb_label.grid_remove()
        # self.right_eb_trb_val.grid_remove()
        self.unlock_button.grid_remove()
        self.encryption_label.grid_remove()
        self.pydbg_button_dfu.grid_remove()
        self.pydbg_button.grid_remove()
        self.dl_button.grid_remove()
        self.flashimage_button.grid_remove()
        self.earbuddash_button.grid_remove()
        self.earbuddash_button1.grid_remove()
        self.earbuddash_button2.grid_remove()
        self.session_button1.grid_remove()
        self.session_button2.grid_remove()

        self.configuration = configparser.ConfigParser()
        self.cfg_file_path = self.dir_path + os.sep + "config_gui.ini"
        self.notebook.grid(row=0, column=0, sticky="nw")

        # self.find_path()

    def get_before_elfpath(self):
        self.pydbg_value = self.wanted_value("Earbud_elf file paths", "before_upgrade_elf_path")

    def get_after_elfpath(self):
        self.pydbg_value = self.wanted_value("Earbud_elf file paths", "after_upgrade_elf_path")

    def get_default_elfpath(self):
        self.pydbg_value = self.wanted_value("Earbud_elf file paths", "before_upgrade_elf_path")
        self.open_cmds()

    def toolkit_filedialog(self):
        """
        To browse ADK toolkit
        """
        toolkit_path = filedialog.askdirectory(initialdir="C:/qtil")

        if toolkit_path != '':
            self.toolkit_path = toolkit_path.replace('/', '\\')
            self.toolkit_label.configure(text=self.toolkit_path, fg='dark blue')
            self.update_config_gui_file("Parameters", 'toolkit_path', self.toolkit_path)
            if not self.toolkit_path == ' ':
                self.left_eb_trb_label.grid(column=0, row=3, padx=5, pady=5)
                self.left_eb_trb_val.grid(column=1, row=3, padx=5, pady=5)
                self.right_eb_trb_label.grid(column=1, row=0, padx=5, pady=5)
                self.right_eb_trb_val.grid(column=2, row=0, padx=5, pady=5)
                self.unlock_button.grid(row=2, column=0, padx=5, pady=3)
                self.encryption_label.grid(column=0, row=3, padx=5, pady=5)
                self.pydbg_button_dfu.grid(row=0, padx=20, pady=3)
                self.pydbg_button.grid(row=1, column=1, padx=20, pady=3)
                self.dl_button.grid(row=2, column=1, padx=20, pady=3)
                self.flashimage_button.grid(row=3, column=1, padx=20, pady=3)
                # self.earbuddash_button.grid(row=5, column=1, padx=80, pady=3)
                self.earbuddash_button.grid(row=4, column=1, padx=20, pady=3)
                self.earbuddash_button1.grid(row=0, column=1, padx=20, pady=3)
                self.earbuddash_button2.grid(row=1, column=1, padx=20, pady=3)
                self.session_button1.grid()
                self.session_button2.grid()

    def trb(self):
        """
        To update the TRB values to config file
        """
        self.scar_id_left = self.left_eb_trb_val.get().strip()
        self.scar_id_right = self.right_eb_trb_val.get().strip()
        if not len(self.scar_id_right) == 6:
            self.popup("Missed a digit in right trb value boss")
        if not len(self.scar_id_left) == 6:
            self.popup("Missed a digit in right trb value boss")
        self.update_config_gui_file("Parameters", "scar_id_left", self.scar_id_left)
        self.update_config_gui_file("Parameters", "scar_id_right", self.scar_id_right)

    def update_config_gui_file(self, section, config, value):
        """
        To update the config file
        """
        with fileinput.FileInput(self.cfg_file_path, inplace=True) as f:
            # self.configuration.set(section, config, value)
            # self.configuration.write(f)
            for line in f:
                if config in line:
                    print(line.replace(line.split('=')[1], ' ' + value))
                else:
                    print(line.strip('\n'))

    def load_cfg_file(self):
        """
        To load a existing config file
        """
        with open(self.cfg_file_path, 'r') as f:
            content = f.readlines()
            for line in content:
                if 'toolkit_path' in line:
                    if line.split('=')[1] != '\n':
                        self.toolkit_path = line.split('=')[1].split('\n')[0]
                        self.toolkit_label.configure(text=self.toolkit_path, fg='dark blue')
                        if not self.toolkit_path == ' ':
                            self.left_eb_trb_label.grid(column=0, row=3, padx=5, pady=5)
                            self.left_eb_trb_val.grid(column=1, row=3, padx=5, pady=5)
                            self.right_eb_trb_label.grid(column=1, row=0, padx=5, pady=5)
                            self.right_eb_trb_val.grid(column=2, row=0, padx=5, pady=5)
                            self.unlock_button.grid(row=2, column=0, padx=5, pady=3)
                            self.encryption_label.grid(column=0, row=3, padx=5, pady=5)
                            self.pydbg_button_dfu.grid()#row=2, column=1, padx=20, pady=3)
                            self.dl_button.grid(row=2, column=1, padx=20, pady=3)
                            self.flashimage_button.grid(row=3, column=1, padx=20, pady=3)
                            # self.earbuddash_button.grid(row=5, column=1, padx=80, pady=3)
                            self.earbuddash_button1.grid(row=0, column=1, padx=20, pady=3)
                            self.earbuddash_button2.grid(row=1, column=1, padx=20, pady=3)
                            self.session_button1.grid()
                            self.session_button2.grid()
                            self.pydbg_button.grid(row=1, column=1, padx=20, pady=3)
                            self.earbuddash_button.grid(row=4, column=1, padx=20, pady=3)

                if 'encryption_key' in line:
                    if line.split('=')[1] != '\n':
                        self.encryption_key = line.split('=')[1].split('\n')[0]
                        self.encryption_label.insert(0, self.encryption_key)

                if 'scar_id_left' in line:
                    if line.split('=')[1] != '\n':
                        self.scar_id_left = line.split('=')[1].split('\n')[0]
                        self.left_eb_trb_val.insert(0, self.scar_id_left)

                if 'scar_id_right' in line:
                    if line.split('=')[1] != '\n':
                        self.scar_id_right = line.split('=')[1].split('\n')[0]
                        self.right_eb_trb_val.insert(0, self.scar_id_right)

    def popup(self, text):
        """
        To show a pop-up to user that some work has done
        """

        def dest():
            if "config file was created" in text:
                sys.exit()
            pop.destroy()

        pop = Tk()
        pop.title("Task Status")
        if "IMAGES FLASHED" in text:
            msg = Label(pop, text=text, width=140, height=10, font=('Lucida Fax', 12))
            msg.pack()
            b = Button(pop, text="OK", command=dest, width=10, font=('Helvetica', 10, 'bold'))
            b.pack()
        else:
            msg = Label(pop, text=text, width=70, height=10, font=('Lucida Fax', 12))
            msg.pack()
            b = Button(pop, text="OK", command=dest, width=10, font=('Helvetica', 10, 'bold'))
            b.pack()
        pop.bell()
        pop.mainloop()

    def unlock(self):
        """
        To unlock the encrypted modules
        """
        self.trb()
        self.encryption_key = self.encryption_label.get().strip()
        toolkit_path = self.toolkit_path + os.sep + "tools\\bin"
        print(self.toolkit_path)
        if not len(self.encryption_key) == 32:
            self.popup("Oops! \nKey seems to be not entered Properly")
        self.update_config_gui_file("Parameters", "encryption_key", self.encryption_key)
        execution(
            r"{}\TransportUnlock -trb {} unlock {}".format(toolkit_path,
                                                           self.scar_id_left,
                                                           self.encryption_key))
        execution(
            r"{}\TransportUnlock -trb {} unlock {}".format(toolkit_path,
                                                           self.scar_id_right,
                                                           self.encryption_key))

    def open_cmds(self):
        """
        To open pydbg sessions from internal pydbg
        """
        self.trb()
        """ To open cmd prompts"""
        path = os.getenv("PYTHONPATH")
        if path is None:
            self.popup("PYTHONPATH is not present in environment variables")
            exit()
        if not os.path.isdir(path):
            self.popup("PYTHONPATH is not a valid directory")
            exit()
        if 'pylib' in path:
            path = path[: -len('pylib')]
        os.chdir(path)
        command1 = None
        command2 = None
        try:
            command1 = 'pydbg.py -d "trb:usb2trb:{}" -f   apps1:{}'.format(self.scar_id_left, self.pydbg_value)
            command2 = 'pydbg.py -d "trb:usb2trb:{}" -f   apps1:{}'.format(self.scar_id_right, self.pydbg_value)
            print(command1)
            execution('start; cmd /K {}'.format(command1))

            print(command2)
            execution('start; cmd /K {}'.format(command2))
        except AttributeError:
            print("Please select one of the option below session button")
        os.chdir(self.dir_path)

    def dlcmd(self):
        """
        To open dual_logger cmd prompt by updating log_setup.py file
        """
        dlcmd_path = self.wanted_value("Parameters", "dual_logger_file_path")
        flag = 0
        with open(dlcmd_path + "\\log_setup.py", "r") as inp:
            new_file_lines = []
            for line in inp:
                if "firmware_builds" in line and "apps1" in line and "apps0" in line and flag == 0:
                    # print(line)
                    # print(line.split(':',1))
                    if len(re.findall(r"'(.*?)'", line.split(':', 1)[1], re.DOTALL)) != 0:
                        l = re.findall(r"'(.*?)'", line.split(':', 1)[1], re.DOTALL)[0]
                        d = line.replace(l.split(',')[0].split(':', 1)[1],
                                         self.wanted_value("Earbud_elf file paths", "before_upgrade_elf_path"))
                        # print("1111111    ", d)
                        line = d
                    elif len(re.findall(r'"(.*?)"', line.split(':', 1)[1], re.DOTALL)) != 0:
                        l = re.findall(r'"(.*?)"', line.split(':', 1)[1], re.DOTALL)[0]
                        d = line.replace(l.split(',')[0].split(':', 1)[1],
                                         self.wanted_value("Earbud_elf file paths", "before_upgrade_elf_path"))
                        # print("2222222    ", d)
                        line = d
                    flag = 1

                if "firmware_builds" in line and "apps1" in line and 'apps0' not in line and flag == 0:
                    # print("44444444     ", line)
                    d = line.replace(line.split(':', 1)[1], "r'apps1:" + self.wanted_value
                     ("Earbud_elf file paths", "before_upgrade_elf_path")) + ",'" + '\n'
                    line = d
                    # print("555555     ", line)
                    flag = 1

                if "firmware_builds" not in line and "apps1" in line and "apps0" not in line and flag == 0:
                    d = line.replace(line, (len(line) - len(line.lstrip())) * ' ' + "r'apps1:" + self.wanted_value
                     ("Earbud_elf file paths", "before_upgrade_elf_path")) + ",'" + '\n'
                    line = d
                    # print("6666666     ", line)
                    flag = 1

                if "firmware_builds" not in line and "apps1" in line and "apps0" in line and 'log' not in line and flag == 0:
                    d = line.replace(line.split(',')[0].split(':', 1)[1],
                                     self.wanted_value("Earbud_elf file paths", "before_upgrade_elf_path"))
                    # print("77777777    ", d)
                    line = d
                    flag = 1

                new_file_lines.append(line)
                flag = 0

        with open(dlcmd_path + "\\log_setup.py", "w") as document1:
            document1.writelines(new_file_lines)
        path = 'cd ' + str(self.wanted_value("Parameters", "dual_logger_file_path"))
        """ To open dual_log cmd prompts from dual_logger path"""
        execution('start; cmd /K {}'.format(path))

    def nvs_cmd_execution(self):
        """ To flash images using NVS input commands"""
        self.trb()
        input = []
        input.append(str(self.wanted_value("Single Flash image files path", "left_path")))
        input.append(str(self.wanted_value("Single Flash image files path", "right_path")))
        nvs_cmds = ['identify', 'erase', 'burn']
        nvs_main_command = [r'\nvscmd.exe -trans "SPITRANS=TRB SPIPORT={}" -deviceid 4 0 '
                                .format(self.scar_id_left),  # Left
                            r'\nvscmd.exe -trans "SPITRANS=TRB SPIPORT={}" -deviceid 4 0 '
                                .format(self.scar_id_right)]  # Right
        toolkit_path = self.toolkit_path + os.sep + "tools\\bin"
        i = 0
        for item in nvs_main_command:
            for check in nvs_cmds:
                if 'burn' in check:
                    check += ' ' + input[i]
                    i += 1
                execution(toolkit_path + item + check)
        self.popup("IMAGES FLASHED\n\nLeft  image path : {} \nRight image path : {}".format(input[0], input[1]))

    def before_upgrade(self):
        """ Path of earbud.elf before Upgrade """
        self.earbuddash()
        command = self.earbud + str(self.wanted_value("Earbud_elf file paths", 'before_upgrade_elf_path'))
        execution(command)

    def after_upgrade(self):
        """ Path of earbud.elf after Upgrade """
        self.earbuddash()
        """ Path of elf file after upgrade """
        command = self.earbud + str(self.wanted_value("Earbud_elf file paths", 'after_upgrade_elf_path'))
        execution(command)

    def earbuddash(self):
        self.trb()
        self.earbud = r'py -2 {}\earbud_dash.py {} {} '.format(
            str(self.wanted_value("Parameters", "earbud_dash_file_path")),
            self.scar_id_left,
            self.scar_id_right)

    def config_gui_execute(self):
        """
        This one creates a new config file with default parameters.
        """
        if not os.path.exists(self.cfg_file_path):
            with open(self.cfg_file_path, "w") as file:
                self.configuration.add_section('Parameters')
                self.configuration.set("Parameters", "; You can update this from GUI part","")
                self.configuration.set("Parameters", "scar_id_left", "")
                self.configuration.set("Parameters", "scar_id_right", "")
                self.configuration.set("Parameters", "encryption_key", "")
                self.configuration.set("Parameters", "toolkit_path", "")
                self.configuration.set("Parameters", "; Fill the details from here", "")
                self.configuration.set("Parameters", "dual_logger_file_path", r"C:\all_apps\dual_logger")
                self.configuration.set("Parameters", "earbud_dash_file_path", r"C:\all_apps\earbud_dash")

                self.configuration.add_section('Earbud_elf file paths')
                self.configuration.set("Earbud_elf file paths", "before_upgrade_elf_path",
                                       r"C:\Aurplus1.2_RC2_CL3572152\QCC515X_QCC305X_SRC_1_0\Release\earbud\workspace\QCC5151-AA_DEV-BRD-R2-AA\image\earbud.elf")
                self.configuration.set("Earbud_elf file paths", "after_upgrade_elf_path",
                                       r"C:\Aurplus1.2_RC2_CL3572152\QCC515X_QCC305X_SRC_1_0\Release\earbud\workspace\QCC5151-AA_DEV-BRD-R2-AA\depend_debug_qcc515x_qcc305x\earbud.elf")

                self.configuration.add_section('Single Flash image files path')
                self.configuration.set("Single Flash image files path", "right_path",
                                       r"C:\Aurplus1.2_RC2_CL3572152\QCC515X_QCC305X_SRC_1_0\Release\earbud\workspace\QCC5151-AA_DEV-BRD-R2-AA\image\RightEn\output\flash_image.xuv")
                self.configuration.set("Single Flash image files path", "left_path",
                                       r"C:\Aurplus1.2_RC2_CL3572152\QCC515X_QCC305X_SRC_1_0\Release\earbud\workspace\QCC5151-AA_DEV-BRD-R2-AA\image\LeftEn\output\flash_image.xuv")
                self.configuration.write(file)
                self.popup("There is no config file\n So new config file was created\n\nPlease update the "
                           "'config_gui' file first")
        self.load_cfg_file()

    def isvalid_option(self, section, value):
        """
        To check the section or value is present in Config file
        """
        result = None
        try:
            result = self.configuration.get(section, value)
        except configparser.NoSectionError:
            self.popup(
                "There is no section: '{}' \n\n Please add the respective section "
                "or delete config file and re-run gui.exe".format(section))
        except configparser.NoOptionError:
            self.popup(
                'In config file\nthe section:" {} " -> value: " {} "is missing\n\n Please add the value in respective section '
                'or\n delete config file and re-run gui.exe for default config file'.format(section, value))
            exit()
        if not result:
            self.popup(
                "In config file\nthe section: {}\tthe value: {} is empty\nPlease provide a value".format(section,
                                                                                                         value))
            exit()
        return result

    def wanted_value(self, section, value):
        """
        To get the value from config file
        """
        try:
            with open(self.cfg_file_path, "r"):
                self.configuration.read(self.cfg_file_path)
                result = self.isvalid_option(section, value)
                return result

        except IOError:
            pass


'''
    def find_path(self):
        """ To find exact ADK path """
        path1 = r"C:\qtil"
        path2 = r"tools\bin"
        command = "dir " + path1 + " >> ref.txt"
        path_list = []
        execution(command)
        with open("ref.txt", "r+") as fd:
            for line in fd:
                if 'ADK_' in line:
                    path_list.append(line.split(" ")[-1].rstrip())
            if len(path_list) > 1:
                for i in enumerate(path_list, 1):
                    print(i)
                element = int(input("Which ADK you want:   "))
                path_main = os.path.join(path1, str(path_list[element - 1]), path2)
            else:
                path_main = os.path.join(path1, str(path_list[0]), path2)
        os.remove("ref.txt")
        self.path = path_main'''

main_window = GuiWindow()
main_window.config_gui_execute()
main_window.mainloop()
