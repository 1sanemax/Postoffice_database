import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql
from PIL import ImageTk, Image
from Repository import entry_func_repo

#relheight, relwidth − Height and width as a float between 0.0 and 1.0,
#as a fraction of the height and width of the parent widget

""" This is a docstring"""

database = sql.connect(
    host='localhost',
    user='root',
    passwd='admin')

mycursor = database.cursor()
mycursor.execute('USE post_database')
mycursor.execute('''CREATE TABLE IF NOT EXISTS Users_data(
    user_id varchar(15),
    user_name varchar(25) UNIQUE,
    password varchar(20) UNIQUE,
    city varchar(30),
    phone_no bigint,
    address varchar(150),
    PRIMARY KEY(user_id)
    )''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS Transaction_details(
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id varchar(15),
    user_name varchar(25),
    service_type varchar(20),
    sender_name varchar(25),
    sender_phone varchar(15),
    sender_address varchar(150),
    sender_area varchar(100),
    sender_pincode varchar(10),
    receiver_name varchar(25),
    receiver_phone varchar(15),
    receiver_address varchar(150),
    receiver_area varchar(100),
    receiver_pincode varchar(10),
    weight_kg DECIMAL(10,2),
    dimensions varchar(50),
    fragile BOOLEAN,
    speed_delivery BOOLEAN,
    vpp BOOLEAN,
    base_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    transaction_time DATETIME
)''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS admin (
    username VARCHAR(50),
    servicetype VARCHAR(50),
    sendername VARCHAR(100),
    senderphonenumber VARCHAR(20),
    senderaddress TEXT,
    senderarea VARCHAR(100),
    senderpincode VARCHAR(20),
    recievername VARCHAR(100),
    recieverphonenumber VARCHAR(20),
    recieveraddress TEXT,
    recieverarea VARCHAR(100),
    recieverpincode VARCHAR(20),
    amount DECIMAL(10,2)
)''')

root = tk.Tk()
root.title('Login')
root.resizable(False, False)
root.config(bg='#fff2ab')

#display = 1920x1080
screen_width = root.winfo_screenwidth()#1536
screen_height = root.winfo_screenheight()#864

win_width = 500
win_height = 600

x = (screen_width/2) - (win_width/2)
y = (screen_height/2) - (win_height/2)

root.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')

def submit_signup(event):
    try:
        # Validate all fields are filled
        if not all([username_entry.get(), userpassword_entry.get(), 
                   useraddress_entry.get(), usercity_entry.get(), 
                   userphone_entry.get()]):
            messagebox.showerror('Error', 'Please enter all required details!')
            return

        # Validate username length
        if not 8 <= len(username_entry.get()) <= 24:
            messagebox.showerror('Error', 'Username must be 8-24 characters!')
            return

        # Validate password
        if not 8 <= len(userpassword_entry.get()) <= 20:
            messagebox.showerror('Error', 'Password must be 8-20 characters!')
            return
        if ' ' in userpassword_entry.get():
            messagebox.showerror('Error', 'Password cannot contain spaces!')
            return

        # Validate phone number
        try:
            phone = int(userphone_entry.get())
            if len(userphone_entry.get()) != 10:  # Assuming 10-digit numbers
                raise ValueError
        except ValueError:
            messagebox.showerror('Error', 'Invalid phone number!')
            return

        # Database operations
        database = sql.connect(
            host='localhost',
            user='root',
            passwd='admin',
            database='post_database')  # Connect directly to the database
            
        mycursor = database.cursor()

        # Get row count safely
        mycursor.execute("SELECT COUNT(*) FROM Users_data")
        count_row = mycursor.fetchone()[0]
        userid_gen = username_entry.get()[:4] + str(count_row)

        # Use parameterized query to prevent SQL injection
        sql_statement = """INSERT INTO Users_data 
                          (user_id, user_name, password, city, phone_no, address) 
                          VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (userid_gen, username_entry.get(), userpassword_entry.get(), 
                 usercity_entry.get(), phone, useraddress_entry.get())

        try:
            mycursor.execute(sql_statement, values)
            database.commit()
            messagebox.showinfo('Success', 'Account created successfully!')
            master.destroy()
            
        except sql.Error as err:
            database.rollback()
            if err.errno == 1062:  # Duplicate entry error
                messagebox.showerror('Error', 'Username/Password already exists!')
            else:
                messagebox.showerror('Database Error', f'Error: {err.msg}')
                
    except Exception as e:
        messagebox.showerror('System Error', f'Unexpected error: {str(e)}')
        print(f"DEBUG: Full error - {repr(e)}")  # For debugging
        
    finally:
        if 'database' in locals() and database.is_connected():
            mycursor.close()
            database.close()

sign_up_win_bool = False

def sign_up_win():

    global sign_up_win_bool
    if sign_up_win_bool==False:
        sign_up_win_bool=True
    else:
        return

    global master
    master = tk.Toplevel()
    master.title('Sign-up')

    win_width = 800
    win_height = 700

    x = (screen_width/2) - (win_width/2)
    y = (screen_height/2) - (win_height/2)

    master.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')
    master.resizable(False, False)
    master.config(bg='#fff2ab')

    my_canvas2 = tk.Canvas(master, width=400, height=240, highlightthickness=0, bg='#fff2ab')
    my_canvas2.place(x=400, y=180, anchor='center')
    my_canvas2.create_image(200, 120, image=bg_img, anchor='center')


    signup_label = tk.Label(master, text='Sign-Up', font=('Arial Black', 40), bg='#fff2ab')
    signup_label.place(x=400, y=30, anchor='center')

    signup_frame = tk.Label(master, bd=0, bg='white')
    signup_frame.place(x=400, y=380, width=700, height=200, anchor='center')

    signup_label = tk.Label(signup_frame, text='Credentials', font=('Arial Black', 20), bg='white')
    signup_label.place(x=350, y=25, anchor='center')

    global username_entry, userpassword_entry, useraddress_entry, usercity_entry, userphone_entry

    username_entry = tk.Entry(signup_frame, bd=0)
    userpassword_entry = tk.Entry(signup_frame, bd=0)
    usercity_entry = tk.Entry(signup_frame, bd=0)
    userphone_entry = tk.Entry(signup_frame, bd=0)
    useraddress_entry = tk.Entry(signup_frame, bd=0)

    bgcolor = '#cecaca'

    entry_func_repo(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry, bgcolor)

    username_entry.bind('<Return>', submit_signup)
    userpassword_entry.bind('<Return>', submit_signup)
    usercity_entry.bind('<Return>', submit_signup)
    userphone_entry.bind('<Return>', submit_signup)
    useraddress_entry.bind('<Return>', submit_signup)

    username_entry.place(x=50, y=60, width=250, height=25)
    userpassword_entry.place(x=400, y=60, width=250, height=25)
    usercity_entry.place(x=50, y=97, width=250, height=25)
    userphone_entry.place(x=400, y=97, width=250, height=25)
    useraddress_entry.place(x=50, y=135, width=600, height=25)

    msg_label_signup1 = tk.Label(master, text='Instructions', font=('Calibri', '11', 'bold', 'underline'), bg='#fff2ab').place(x=100, y=500)
    msg_label_signup1 = tk.Label(master, text='1. Please enter username with atleast 8 characters not exceeding 25 characters', bg='#fff2ab').place(x=120, y=530)
    msg_label_signup1 = tk.Label(master, text='2. Please enter password with atleast 8 characters not exceeding 20 characters', bg='#fff2ab').place(x=120, y=550)
    msg_label_signup1 = tk.Label(master, text='3. Kindly check your details before submitting', bg='#fff2ab').place(x=120, y=570)
    msg_label_signup1 = tk.Label(master, text='4. Press \'Return\' key when finished', bg='#fff2ab').place(x=120, y=590)

def enable_user(event):
    user_entry.configure(state='normal')
    if user_entry.get()=='Enter Username':
        user_entry.delete(0, 'end')
    user_entry.configure(bg='#cecaca')

def enable_pass(event):
    pass_entry.configure(state='normal')
    if pass_entry.get()=='Enter Password':
        pass_entry.delete(0, 'end')
    pass_entry.configure(bg='#cecaca')
    if check_var.get()=='off':
        pass_entry.config(show='*')
    elif check_var.get()=='on':
        pass_entry.config(show='')


def mouse_user(event):
    if not user_entry.get():
        user_entry.insert(0, 'Enter Username')
        user_entry.configure(state='disabled')

def mouse_pass(event):
    if not pass_entry.get():
        pass_entry.insert(0, 'Enter Password')
        pass_entry.configure(state='disabled')
        pass_entry.config(show='')

def user_tab(event):
    enable_pass(event)
    mouse_user(event)

def pass_tab(event):
    enable_user(event)
    mouse_pass(event)


def submit_login(event):
    global root

    database = sql.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'admin')

    mycursor = database.cursor()
    mycursor.execute('USE post_database')
    
    # ===== ADD THIS ADMIN CHECK FIRST =====
    username = user_entry.get()
    password = pass_entry.get()
    
    # Hardcoded admin credentials (change these!)
    if username == 'admin':
        if password != 'Admin@123':  # Change to your secure password
            messagebox.showerror('Error', 'Invalid admin credentials')
            database.close()
            return
        else:
            # Admin login successful
            user_entry.delete(0, 'end')
            pass_entry.delete(0, 'end')
            root.withdraw()
            import Services_Module
            Services_Module.create_window(root, username, is_admin=True)
            database.close()
            return
    # ===== END ADMIN CHECK =====

    sql_statement = "SELECT * FROM Users_data WHERE user_name=%s"
    var = (user_entry.get(),)

    var_user = user_entry.get()

    mycursor.execute(sql_statement, var)
    tmp_data = mycursor.fetchall()

    if not tmp_data:
        messagebox.showerror('Error', 'Invalid credentials')

    else:
        for tmp_var in tmp_data:
            if pass_entry.get()==tmp_var[2] and user_entry.get()==tmp_var[1]:
                user_entry.delete(0, 'end')
                pass_entry.delete(0, 'end')

                mouse_user(event)
                mouse_pass(event)
                root.withdraw()

                import Services_Module
                Services_Module.create_window(root, var_user)

            else:
                messagebox.showerror('Error', 'Username and password do not match!')
    database.close()


bg_img = tk.PhotoImage(file='User_login_logo.png')
tmp_canvas = tk.Canvas(root, width=100, height=3)

#highlightthickness removes the border
my_canvas1 = tk.Canvas(root, width=300, height=280, bg='#fff2ab', highlightthickness=0, relief='ridge')
my_canvas1.place(x=100, y=10)

#the first 2 parameters are coordinates
#"anchor" at center means that the center of the image will be
#placed at the specified coordinates
#coordinates within canvas
my_canvas1.create_image(150, 170, image=bg_img, anchor='center')
my_canvas1.create_text(150, 25, text='Login', font=('Arial Black', 40), anchor='center')

frame = tk.LabelFrame(root, width=350, height=220, bg='white', bd=0)
frame.place(x=75, y=300, anchor='nw')

user_entry = tk.Entry(frame, bd=0)
user_entry.place(x=50, y=50, anchor='nw', width=250, height=25)
user_entry.insert(0, 'Enter Username')
user_entry.configure(state='disabled')
user_entry.bind('<Button-1>', enable_user)
user_entry.bind('<Leave>', mouse_user)
user_entry.bind('<Tab>', user_tab)
user_entry.bind('<Return>', submit_login)

pass_entry = tk.Entry(frame, bd=0)
pass_entry.place(x=50, y=100, anchor='nw', width=250, height=25)
pass_entry.insert(0, 'Enter Password')
pass_entry.configure(state='disabled')
pass_entry.bind('<Button-1>', enable_pass)
pass_entry.bind('<Leave>', mouse_pass)
pass_entry.bind('<Tab>', pass_tab)
pass_entry.bind('<Return>', submit_login)


sign_up = tk.Button(frame,
    text='Don\'t have an account?',bd=0,
    bg='white', activebackground='white',
    command=sign_up_win,
    fg='#f71919',
    cursor='hand2',
    activeforeground='#f71919',
    takefocus=0)
sign_up.place(x=50, y=170, anchor='nw')


def show_passwd_func():
    if check_var.get()=='on':
        pass_entry.configure(show='')
    elif check_var.get()=='off':
        if pass_entry.get()!='Enter Password':
            pass_entry.configure(show='*')

check_var = tk.StringVar()
show_password = tk.Checkbutton(frame, text='Show password',
    bg='white', activebackground='white',
    variable=check_var,
    onvalue='on', offvalue='off',
    command=show_passwd_func,
    takefocus=0)

#the takefocus=0 attribute disables the focus option
#for the given widget
show_password.place(x=47, y=125, anchor='nw')
show_password.deselect()

database.commit()
database.close()

root.mainloop()
