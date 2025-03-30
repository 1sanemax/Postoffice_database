import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import mysql.connector as sql
from Repository import *
from Procedure_Module import *
import csv
import sys  # mod: Added for admin verification

# Add these functions at the top of Services_Module.py
def validate_phone_number(phone):
    """Validate phone number format"""
    return phone.isdigit() and len(phone) == 10

def validate_pincode(pincode):
    """Validate pincode format"""
    return pincode.isdigit() and len(pincode) == 6

def collect_common_fields(fields):
    """Collect common sender/receiver fields"""
    data = {
        'sender_name': fields['sender_name'].get().strip(),
        'sender_phone': fields['sender_phone'].get().strip(),
        'sender_address': fields['sender_address'].get().strip(),
        'sender_area': fields['sender_area'].get().strip(),
        'sender_pincode': fields['sender_pincode'].get().strip(),
        'receiver_name': fields['receiver_name'].get().strip(),
        'receiver_phone': fields['receiver_phone'].get().strip(),
        'receiver_address': fields['receiver_address'].get().strip(),
        'receiver_area': fields['receiver_area'].get().strip(),
        'receiver_pincode': fields['receiver_pincode'].get().strip()
    }
    
    # Validate common fields
    for field, value in data.items():
        if not value:
            raise ValueError(f"Please fill {field.replace('_', ' ')}")
    
    if not validate_phone_number(data['sender_phone']):
        raise ValueError("Invalid sender phone number")
    
    if not validate_phone_number(data['receiver_phone']):
        raise ValueError("Invalid receiver phone number")
    
    if not validate_pincode(data['sender_pincode']):
        raise ValueError("Invalid sender pincode")
    
    if not validate_pincode(data['receiver_pincode']):
        raise ValueError("Invalid receiver pincode")
    
    return data

def setup_service_window(window, service_type, user):
    """Common setup for all service windows with complete field layout"""
    fields = {
        'sender_name': tk.Entry(window),
        'sender_phone': tk.Entry(window),
        'sender_address': tk.Entry(window),
        'sender_area': tk.Entry(window),
        'sender_pincode': tk.Entry(window),
        'receiver_name': tk.Entry(window),
        'receiver_phone': tk.Entry(window),
        'receiver_address': tk.Entry(window),
        'receiver_area': tk.Entry(window),
        'receiver_pincode': tk.Entry(window),
    }
    
    if service_type != 'Post':
        fields['weight'] = tk.Entry(window)
    
    # Create frames for organization
    header_frame = tk.Frame(window, bg='white')
    sender_frame = tk.Frame(window, bg='white', padx=10, pady=10)
    receiver_frame = tk.Frame(window, bg='white', padx=10, pady=10)
    service_frame = tk.Frame(window, bg='white', padx=10, pady=10)
    button_frame = tk.Frame(window, bg='white')
    
    # Pack all frames
    header_frame.pack(fill='x', padx=5, pady=5)
    sender_frame.pack(fill='x', padx=5, pady=5)
    receiver_frame.pack(fill='x', padx=5, pady=5)
    service_frame.pack(fill='x', padx=5, pady=5)
    button_frame.pack(fill='x', padx=5, pady=10)
    
    # Header
    tk.Label(header_frame, 
            text=f"{service_type} Service - Logged in as {user}",
            font=('Arial', 16, 'bold'),
            bg='white').pack()
    
    # Sender Fields
    tk.Label(sender_frame, text="Sender Details", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, sticky='w')
    
    labels = ['Name:', 'Phone:', 'Address:', 'Area:', 'Pincode:']
    for i, label in enumerate(labels, start=1):
        tk.Label(sender_frame, text=label, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
    
    fields['sender_name'].grid(row=1, column=1, sticky='ew', padx=5, pady=2)
    fields['sender_phone'].grid(row=2, column=1, sticky='ew', padx=5, pady=2)
    fields['sender_address'].grid(row=3, column=1, sticky='ew', padx=5, pady=2)
    fields['sender_area'].grid(row=4, column=1, sticky='ew', padx=5, pady=2)
    fields['sender_pincode'].grid(row=5, column=1, sticky='ew', padx=5, pady=2)
    
    # Receiver Fields
    tk.Label(receiver_frame, text="Receiver Details", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, sticky='w')
    
    for i, label in enumerate(labels, start=1):
        tk.Label(receiver_frame, text=label, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
    
    fields['receiver_name'].grid(row=1, column=1, sticky='ew', padx=5, pady=2)
    fields['receiver_phone'].grid(row=2, column=1, sticky='ew', padx=5, pady=2)
    fields['receiver_address'].grid(row=3, column=1, sticky='ew', padx=5, pady=2)
    fields['receiver_area'].grid(row=4, column=1, sticky='ew', padx=5, pady=2)
    fields['receiver_pincode'].grid(row=5, column=1, sticky='ew', padx=5, pady=2)
    
    # Service-Specific Fields
    if service_type == 'Parcel':
        tk.Label(service_frame, text="Parcel Details", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, sticky='w')
        
        # Weight
        tk.Label(service_frame, text="Weight (kg):", bg='white').grid(row=1, column=0, sticky='e', padx=5, pady=2)
        fields['weight'].grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Dimensions
        tk.Label(service_frame, text="Dimensions (LxWxH cm):", bg='white').grid(row=2, column=0, sticky='e', padx=5, pady=2)
        dim_frame = tk.Frame(service_frame, bg='white')
        dim_frame.grid(row=2, column=1, sticky='ew')
        
        length_entry = tk.Entry(dim_frame, width=5)
        width_entry = tk.Entry(dim_frame, width=5)
        height_entry = tk.Entry(dim_frame, width=5)
        
        length_entry.pack(side='left', padx=2)
        tk.Label(dim_frame, text="x", bg='white').pack(side='left')
        width_entry.pack(side='left', padx=2)
        tk.Label(dim_frame, text="x", bg='white').pack(side='left')
        height_entry.pack(side='left', padx=2)
        
        # Options
        options_frame = tk.Frame(service_frame, bg='white')
        options_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        fragile_var = tk.IntVar()
        speed_var = tk.IntVar()
        vpp_var = tk.IntVar()
        
        tk.Checkbutton(options_frame, text="Fragile", variable=fragile_var, bg='white').pack(side='left', padx=5)
        tk.Checkbutton(options_frame, text="Speed Delivery", variable=speed_var, bg='white').pack(side='left', padx=5)
        tk.Checkbutton(options_frame, text="VPP", variable=vpp_var, bg='white').pack(side='left', padx=5)
        
        fields.update({
            'length': length_entry,
            'width': width_entry,
            'height': height_entry,
            'fragile': fragile_var,
            'speed_delivery': speed_var,
            'vpp': vpp_var
        })
    
    elif service_type == 'Speedpost':
        tk.Label(service_frame, text="Weight (grams):", bg='white').grid(row=0, column=0, sticky='e', padx=5, pady=2)
        fields['weight'].grid(row=0, column=1, sticky='ew', padx=5, pady=2)
    
    # Submit Button
    submit_btn = tk.Button(button_frame, text="Submit", command=lambda: submit_handler(fields, service_type, user))
    submit_btn.pack(pady=10)
    
    return fields

def create_submit_button(window, service_type, user, fields):
    """Creates a standardized submit button for all services"""
    def submit_handler():
        try:
            # Common validation
            required_fields = ['sender_name', 'sender_phone', 'sender_address', 
                             'sender_area', 'sender_pincode', 'receiver_name',
                             'receiver_phone', 'receiver_address', 'receiver_area',
                             'receiver_pincode']
            
            for field in required_fields:
                if not fields[field].get().strip():
                    raise ValueError(f"Please fill {field.replace('_', ' ')}")

            # Prepare transaction data
            transaction_data = {
                'user_name': user,
                'service_type': service_type,
                'sender_name': fields['sender_name'].get().strip(),
                'sender_phone': fields['sender_phone'].get().strip(),
                'sender_address': fields['sender_address'].get().strip(),
                'sender_area': fields['sender_area'].get().strip(),
                'sender_pincode': fields['sender_pincode'].get().strip(),
                'receiver_name': fields['receiver_name'].get().strip(),
                'receiver_phone': fields['receiver_phone'].get().strip(),
                'receiver_address': fields['receiver_address'].get().strip(),
                'receiver_area': fields['receiver_area'].get().strip(),
                'receiver_pincode': fields['receiver_pincode'].get().strip(),
            }

            # Service-specific fields
            if service_type == 'Parcel':
                transaction_data.update({
                    'weight_kg': float(fields['weight'].get()),
                    'dimensions': f"{fields['length'].get()}x{fields['width'].get()}x{fields['height'].get()}",
                    'fragile': bool(fields['fragile'].get()),
                    'speed_delivery': bool(fields['speed_delivery'].get()),
                    'vpp': bool(fields['vpp'].get()),
                    'total_amount': window.calculated_amount
                })
            elif service_type == 'Speedpost':
                transaction_data.update({
                    'weight_kg': float(fields['weight'].get()) / 1000,  # convert grams to kg
                    'total_amount': window.calculated_amount
                })

            # Save to database
            if save_transaction(transaction_data):
                messagebox.showinfo("Success", f"{service_type} transaction saved successfully!")
                # Clear form
                for field in fields.values():
                    if isinstance(field, tk.Entry):
                        field.delete(0, tk.END)
                if hasattr(window, 'calculated_amount'):
                    del window.calculated_amount

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Create and return the submit button
    submit_btn = tk.Button(window, text="Submit Transaction", 
                          command=submit_handler,
                          bg='#4CAF50', fg='white',
                          font=('Arial', 12, 'bold'),
                          padx=20, pady=10)
    return submit_btn

def view_all_transactions():
    try:
        # Database connection
        db = sql.connect(
            host='localhost',
            user='root',
            passwd='admin',
            database='post_database'
        )
        cursor = db.cursor(dictionary=True)
        
        # Fetch data with explicit column selection
        cursor.execute("""
            SELECT 
                username, servicetype, 
                sendername, senderphonenumber,
                senderaddress, senderarea, senderpincode,
                recievername, recieverphonenumber,
                recieveraddress, recieverarea, recieverpincode,
                amount
            FROM admin
            ORDER BY amount DESC
        """)
        
        # Create admin window
        admin_window = tk.Toplevel()
        admin_window.title("Admin View")
        admin_window.geometry("1400x600")
        
        # Configure Treeview
        tree = ttk.Treeview(admin_window)
        
        # Define columns EXACTLY matching your SELECT query
        columns = [
            ("Username", 100),
            ("Service", 80),
            ("Sender", 120),
            ("Sender Phone", 100),
            ("Sender Address", 150),
            ("Sender Area", 100),
            ("Sender Pincode", 80),
            ("Receiver", 120),
            ("Receiver Phone", 100),
            ("Receiver Address", 150),
            ("Receiver Area", 100),
            ("Receiver Pincode", 80),
            ("Amount", 80)
        ]
        
        # Configure columns
        tree["columns"] = [col[0] for col in columns]
        for col_name, width in columns:
            tree.column(col_name, width=width, anchor='center')
            tree.heading(col_name, text=col_name)
        
        # Insert data
        for row in cursor.fetchall():
            tree.insert("", "end", values=(
                row['username'],
                row['servicetype'],
                row['sendername'],
                row['senderphonenumber'],
                row['senderaddress'],
                row['senderarea'],
                row['senderpincode'],
                row['recievername'],
                row['recieverphonenumber'],
                row['recieveraddress'],
                row['recieverarea'],
                row['recieverpincode'],
                f"₹{row['amount']:.2f}"  # Format amount as currency
            ))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(admin_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def security_timeout(window):  # mod: New function
    window.destroy()
    messagebox.showinfo("Session Expired", "Admin session timed out after 30 minutes")

def on_view_close(window, db):  # mod: New function
    if db.is_connected():
        db.close()
    window.destroy()

def export_transactions(transactions):  # mod: New function
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save transactions as"
        )
        if not filename:
            return
            
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['transaction_id', 'user_name', 'service_type',
                        'sender_area', 'receiver_area', 'total_amount', 'transaction_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
            
        messagebox.showinfo("Success", f"Transactions exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

def create_window(root, user, is_admin=False):  # mod: Added is_admin parameter
    counter_win = 0

    global win_user
    win_user = user

    global second
    second = tk.Tk()
    second.resizable(False, False)

    def back_func():
        root.iconify()
        root.deiconify()
        second.destroy()

    def close_func():
        root.destroy()
        second.destroy()

    second.protocol('WM_DELETE_WINDOW', close_func)

    global edit_users_data_bool
    edit_users_data_bool = False
    
    def edit_users_data():
        second.withdraw()

        third = tk.Toplevel()
        third.title('User details')
        third.configure(bg='#404040')

        win_width = 950
        win_height = 600

        screen_width = second.winfo_screenwidth()#1536
        screen_height = second.winfo_screenheight()#864

        x = (screen_width/2) - (win_width/2)
        y = (screen_height/2) - (win_height/2)

        third.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')

        database = sql.connect(
            host='localhost',
            user='root',
            passwd='admin',
            database='post_database'
            )

        my_sor = database.cursor()

        my_sor.execute('SELECT * FROM Users_data')

        data_users = my_sor.fetchall()

        style = ttk.Style(third)

        style.theme_use('default')
        style.configure('Treeview',
            background='white',
            foreground='black',
            rowheight=25,
            fieldbackground='white')

        style.map('Treeview',
            background=[('selected', 'yellow')],
            foreground=[('selected', 'black')])

        tree_frame = tk.Frame(third)
        tree_frame.pack(pady=20)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')

        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
        tree.pack()

        tree_scroll.config(command=tree.yview)

        tree['columns'] = ("ID", "Name", "Password", 'City', "Phone", "Address")

        tree.column("#0", stretch='no', width=0)
        tree.column("ID", anchor='center', width=70)
        tree.column("Name", anchor='center', width=160)
        tree.column("Password", anchor='center', width=160)
        tree.column("City", anchor='center', width=130)
        tree.column("Phone", anchor='center', width=90)
        tree.column("Address", anchor='center', width=200)

        tree.heading('#0', text='')
        tree.heading('ID', text='Id')
        tree.heading('Name', text='Name')
        tree.heading('Password', text='Password')
        tree.heading('City', text='City')
        tree.heading('Phone', text='Phone')
        tree.heading('Address', text='Address')

        tree.tag_configure('odd', background='white')
        tree.tag_configure('even', background='lightgreen')

        tree.config(takefocus=0)

        global count
        count = 0
        for i in data_users:
            if count%2==0:
                tree.insert(parent='', index='end', iid=count, text='', values=(i[0], i[1], i[2], i[3], i[4], i[5]), tags=('even',))
            else:
                tree.insert(parent='', index='end', iid=count, text='', values=(i[0], i[1], i[2], i[3], i[4], i[5]), tags=('odd',))
            count+= 1

        tmp_frame = tk.Frame(third, bd=0, bg='#a6a2a2')
        tmp_frame.pack(pady=10)


        def select_entry():

            username_entry.config(state='normal')
            userpassword_entry.config(state='normal')
            usercity_entry.config(state='normal')
            userphone_entry.config(state='normal')
            useraddress_entry.config(state='normal')

            delete_entry_boxes(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry)

            selected = tree.focus()#Returns iid

            values = tree.item(selected, 'values')#Returns values of the iid

            try:
                username_entry.insert(0, values[1])
                userpassword_entry.insert(0, values[2])
                usercity_entry.insert(0, values[3])
                userphone_entry.insert(0, values[4])
                useraddress_entry.insert(0, values[5])

            except IndexError:
                username_entry.insert(0, 'Enter username')
                userpassword_entry.insert(0, 'Enter password')
                usercity_entry.insert(0, 'Enter city')
                userphone_entry.insert(0, 'Enter phone number')
                useraddress_entry.insert(0, 'Enter address')

                username_entry.config(state='disabled')
                userpassword_entry.config(state='disabled')
                usercity_entry.config(state='disabled')
                userphone_entry.config(state='disabled')
                useraddress_entry.config(state='disabled')

                messagebox.showerror('Error', 'Select an element first!')

        def update_entry_user(event):
            selected = tree.focus()
            if len(selected)==0:
                messagebox.showerror('Error', 'Select an element first!')
                return

            try:
                values = tree.item(selected, 'values')
                bool_var = update_entry(win_user, event, username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry, values[0])

                if bool_var:
                    tree.item(selected, text='', values=(values[0], username_entry.get(), userpassword_entry.get(), usercity_entry.get(), userphone_entry.get(), useraddress_entry.get()))

                    delete_entry_boxes(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry)

                    username_entry.insert(0, 'Enter username')
                    userpassword_entry.insert(0, 'Enter password')
                    usercity_entry.insert(0, 'Enter city')
                    userphone_entry.insert(0, 'Enter phone number')
                    useraddress_entry.insert(0, 'Enter address')

                    username_entry.config(state='disabled')
                    userpassword_entry.config(state='disabled')
                    usercity_entry.config(state='disabled')
                    userphone_entry.config(state='disabled')
                    useraddress_entry.config(state='disabled')

            except IndexError:
                messagebox.showerror('Error', 'Fill in all parameters!')

            except ValueError:
                messagebox.showerror('Error', 'Fill valid information!')


        def add_entry():
            if username_entry['state']=='disabled':
                messagebox.showerror('Error', 'Please fill in all details!')

            else:
                global count

                userid_gen = username_entry.get()[0:4]
                userid_gen = userid_gen + str(count)

                if count%2==0:
                    tree.insert(parent='', index='end', iid=count, text='', values=(userid_gen, username_entry.get(), userpassword_entry.get(), usercity_entry.get(), userphone_entry.get(), useraddress_entry.get()), tags=('even',))

                elif count%2!=0:
                    tree.insert(parent='', index='end', iid=count, text='', values=(userid_gen, username_entry.get(), userpassword_entry.get(), usercity_entry.get(), userphone_entry.get(), useraddress_entry.get()), tags=('odd',))
                count+= 1

                database = sql.connect(
                    host='localhost',
                    user='root',
                    passwd='admin',
                    database='post_database'
                    )

                my_sor = database.cursor()

                sql_statement = "INSERT INTO Users_data VALUES('{}', '{}', '{}', '{}', {}, '{}')".format(userid_gen, username_entry.get(), userpassword_entry.get(), usercity_entry.get(), userphone_entry.get(), useraddress_entry.get())

                my_sor.execute(sql_statement)

                database.commit()
                database.close()

                delete_entry_boxes(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry)

                username_entry.insert(0, 'Enter username')
                userpassword_entry.insert(0, 'Enter password')
                usercity_entry.insert(0, 'Enter city')
                userphone_entry.insert(0, 'Enter phone number')
                useraddress_entry.insert(0, 'Enter address')

                username_entry.config(state='disabled')
                userpassword_entry.config(state='disabled')
                usercity_entry.config(state='disabled')
                userphone_entry.config(state='disabled')
                useraddress_entry.config(state='disabled')

        def delete_entry():
            global count

            database = sql.connect(
                host='localhost',
                user='root',
                passwd='admin',
                database='post_database'
                )

            my_sor = database.cursor()

            tmp_var = tree.selection()

            if not tmp_var:
                messagebox.showerror('Error', 'Select element(s) first!')

            else:

                for var in tmp_var:
                    values = tree.item(var, 'values')[0]
                    my_sor.execute("DELETE FROM Users_data WHERE user_id='{}'".format(values))
                    tree.delete(var)

                    count-= 1

            database.commit()
            database.close()

        global username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry

        username_entry = tk.Entry(tmp_frame, bd=0, bg='white')
        userpassword_entry = tk.Entry(tmp_frame, bd=0, bg='white')
        usercity_entry = tk.Entry(tmp_frame, bd=0, bg='white')
        userphone_entry = tk.Entry(tmp_frame, bd=0, bg='white')
        useraddress_entry = tk.Entry(tmp_frame, bd=0, bg='white')

        username_entry.bind('<Return>', update_entry_user)
        userpassword_entry.bind('<Return>', update_entry_user)
        usercity_entry.bind('<Return>', update_entry_user)
        userphone_entry.bind('<Return>', update_entry_user)
        useraddress_entry.bind('<Return>', update_entry_user)

        entry_func_repo(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry, 'white')

        username_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=0, column=0)
        userpassword_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=0, column=1)
        usercity_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=1, column=0)
        userphone_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=1, column=1)
        useraddress_entry.grid(padx=25, pady=10, ipadx=150, ipady=3, row=2, column=0, columnspan=2)

        widget_frame = tk.Frame(third, bd=0, bg='#404040')
        widget_frame.pack(pady=10)

        select_user = tk.Button(widget_frame, text='Select record', command=select_entry, relief='flat', cursor='hand2')
        select_user.grid(row=0, column=0, padx=10, pady=5)
        select_user.config(bg='white', activebackground='white')
        select_user.config(takefocus=0)

        add_user = tk.Button(widget_frame, text='Add record', command=add_entry, relief='flat', cursor='hand2')
        add_user.grid(row=0, column=1, padx=10, pady=5)
        add_user.config(bg='white', activebackground='white')
        add_user.config(takefocus=0)

        delete_user = tk.Button(widget_frame, text='Delete record', command=delete_entry, relief='flat', bg='white', cursor='hand2')
        delete_user.grid(row=0, column=2, padx=10, pady=5)
        delete_user.config(bg='white', activebackground='white')
        delete_user.config(takefocus=0)

        csv_save = tk.Button(widget_frame, text='Save data into a csv file', relief='flat', cursor='hand2')
        csv_save.grid(row=1, column=1, padx=10, pady=15)
        csv_save.config(bg='white', activebackgroun='white')
        csv_save.config(takefocus=0)

        def deiconify_win():
            second.iconify()
            second.deiconify()
            third.destroy()

        third.protocol('WM_DELETE_WINDOW', deiconify_win)

        database.close()

        third.mainloop()

        def selected_combo():
            pass

    if user=='root' or is_admin:  # mod: Added is_admin check
        win_width = 900
        win_height = 600

        screen_width = second.winfo_screenwidth()
        screen_height = second.winfo_screenheight()

        x = (screen_width/2) - (win_width/2)
        y = (screen_height/2) - (win_height/2)

        second.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')

        second.title('Logged in as administrator')
        second.config(bg='#404040')

        menubar = tk.Menu(second)
        second.config(menu=menubar)

        # mod: Reorganized menu structure
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Logout', command=back_func)
        file_menu.add_command(label='Exit', command=close_func)

        # mod: Added admin menu
        admin_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Admin', menu=admin_menu)
        admin_menu.add_command(label='View All Transactions', command=view_all_transactions)
        admin_menu.add_command(label='Edit User Data', command=edit_users_data)

        tk.Label(second, text='Choose what database to view: ', bg='#404040', 
                fg='white', font=('Arial Black', 20, 'bold')).pack(pady=20)

        data_user = tk.Button(second, text='Edit user data', bg='white', cursor='hand2', command=edit_users_data, padx=20)
        data_user.pack(pady=20, padx=100, ipadx=26)
        data_user.config(bg='white', activebackground='white')


        global selected_combo_bool
        selected_combo_bool = False

        def selected_combo(event):
            if trans_user_combo.get() == '< Select >':
                messagebox.showerror('Error', 'Choose database first')
                return

            second.withdraw()
            fourth = tk.Toplevel()
            fourth.config(bg='#404040')
            fourth.title(f'{trans_user_combo.get()} Transactions')
            
            # Window sizing
            win_width = 1500
            win_height = 600
            x = (second.winfo_screenwidth()/2) - (win_width/2)
            y = (second.winfo_screenheight()/2) - (win_height/2)
            fourth.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')
            # Add this right before your treeview creation code:
            def export_to_csv():
                try:
                    # Ask user for save location
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".csv",
                        filetypes=[("CSV files", "*.csv")],
                        title="Save transaction data as"
                    )
                    
                    if not file_path:  # User cancelled
                        return
                        
                    # Write to CSV
                    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        
                        # Write headers
                        headers = [
                            "User ID", "User Name", "Service Type",
                            "Sender Name", "Sender Phone", "Sender Address",
                            "Sender Area", "Sender Pincode",
                            "Receiver Name", "Receiver Phone", "Receiver Address",
                            "Receiver Area", "Receiver Pincode",
                            "Transaction Time", "Amount"
                        ]
                        writer.writerow(headers)
                        
                        # Write data
                        for row in data_retr:
                            writer.writerow([
                                row[0], row[1], row[2],  # User details
                                row[3], row[4], row[5], row[6], row[7],  # Sender
                                row[8], row[9], row[10], row[11], row[12],  # Receiver
                                row[13].strftime("%Y-%m-%d %H:%M:%S"),  # Formatted time
                                f"{row[14]:.2f}" if row[14] else "0.00"  # Amount
                            ])
                            
                    messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
                    
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")

            # Add to your existing button frame (create if needed)
            button_frame = tk.Frame(fourth, bg='#404040')
            button_frame.pack(fill='x', pady=(0, 10))
            
            # Back Button
            tk.Button(
                button_frame,
                text="← Back",
                command=lambda: [fourth.destroy(), second.deiconify()],
                bg='#f44336',
                fg='white'
            ).pack(side='left', padx=10)
            
            # Export CSV Button
            tk.Button(
                button_frame,
                text="Export to CSV",
                command=export_to_csv,
                bg='#4CAF50',
                fg='white',
                padx=15
            ).pack(side='right', padx=10)
            # Database connection
            try:
                db = sql.connect(
                    host='localhost',
                    user='root',
                    passwd='admin',
                    database='post_database'
                )
                cursor = db.cursor()
                
                # Fetch data with amount
                cursor.execute('''
                    SELECT 
                        user_id, user_name, service_type,
                        sender_name, sender_phone, sender_address, 
                        sender_area, sender_pincode,
                        receiver_name, receiver_phone, receiver_address,
                        receiver_area, receiver_pincode,
                        transaction_time, total_amount
                    FROM Transaction_details 
                    WHERE service_type=%s
                    ORDER BY transaction_time DESC
                ''', (trans_user_combo.get(),))
                
                data_retr = cursor.fetchall()

                # Create Treeview
                tree_frame = tk.Frame(fourth)
                tree_frame.pack(pady=20, fill='both', expand=True)
                
                # Add scrollbars
                y_scroll = ttk.Scrollbar(tree_frame, orient='vertical')
                x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
                
                # Configure Treeview
                tree = ttk.Treeview(
                    tree_frame,
                    columns=(
                        "User ID", "User Name", "Service Type",
                        "Sender Name", "Sender Phone", "Sender Address",
                        "Sender Area", "Sender Pincode",
                        "Receiver Name", "Receiver Phone", "Receiver Address",
                        "Receiver Area", "Receiver Pincode",
                        "Time", "Amount"
                    ),
                    yscrollcommand=y_scroll.set,
                    xscrollcommand=x_scroll.set,
                    selectmode='extended'
                )
                
                # Column configuration
                columns = [
                    ("User ID", 70, 'center'),
                    ("User Name", 120, 'center'),
                    ("Service Type", 100, 'center'),
                    ("Sender Name", 150, 'center'),
                    ("Sender Phone", 100, 'center'),
                    ("Sender Address", 150, 'center'),
                    ("Sender Area", 100, 'center'),
                    ("Sender Pincode", 80, 'center'),
                    ("Receiver Name", 150, 'center'),
                    ("Receiver Phone", 100, 'center'),
                    ("Receiver Address", 150, 'center'),
                    ("Receiver Area", 100, 'center'),
                    ("Receiver Pincode", 80, 'center'),
                    ("Time", 150, 'center'),
                    ("Amount", 100, 'e')  # Right-aligned for currency
                ]
                
                tree.column("#0", width=0, stretch=False)
                for col_name, width, anchor in columns:
                    tree.column(col_name, width=width, anchor=anchor)
                    tree.heading(col_name, text=col_name)
                
                # Style configuration
                tree.tag_configure('odd', background='white')
                tree.tag_configure('even', background='lightgreen')
                
                # Insert data with formatted amount
                for i, row in enumerate(data_retr):
                    values = (
                        row[0], row[1], row[2],  # User ID, Name, Service Type
                        row[3], row[4], row[5], row[6], row[7],  # Sender details
                        row[8], row[9], row[10], row[11], row[12],  # Receiver details
                        row[13].strftime("%Y-%m-%d %H:%M"),  # Formatted time
                        f"₹{row[14]:.2f}" if row[14] else "₹0.00"  # Formatted amount
                    )
                    tree.insert("", "end", values=values, tags=('even' if i%2==0 else 'odd',))
                
                # Pack widgets
                y_scroll.config(command=tree.yview)
                x_scroll.config(command=tree.xview)
                y_scroll.pack(side='right', fill='y')
                x_scroll.pack(side='bottom', fill='x')
                tree.pack(fill='both', expand=True)
                
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if 'db' in locals() and db.is_connected():
                    cursor.close()
                    db.close()
            
            def deiconify_win():
                second.deiconify()
                fourth.destroy()
            
                fourth.protocol('WM_DELETE_WINDOW', deiconify_win)

                tree_frame = tk.Frame(fourth)
                tree_frame.pack(pady=20)

                style = ttk.Style(tree_frame)

                style.theme_use('default')
                style.configure('Treeview',
                    background='white',
                    foreground='black',
                    rowheight=25,
                    fieldbackground='white')

                style.map('Treeview',
                    background=[('selected', 'yellow')],
                    foreground=[('selected', 'black')])

                tree_scroll = tk.Scrollbar(tree_frame)
                tree_scroll.pack(side='right', fill='y')

                tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
                tree.pack()

                tree_scroll.config(command=tree.yview)

                tree['columns'] = (
                    "User ID", "User Name", "Service Type",
                    "Sender Name", "Sender Phone", "Sender Address", 
                    "Sender Area", "Sender Pincode",
                    "Receiver Name", "Receiver Phone", "Receiver Address",
                    "Receiver Area", "Receiver Pincode",
                    "Time", "Amount"
                )
                
                # Set column widths and alignment
                columns_config = [
                    ("User ID", 70, 'center'),
                    ("User Name", 120, 'center'),
                    ("Service Type", 100, 'center'),
                    ("Sender Name", 150, 'center'),
                    ("Sender Phone", 100, 'center'),
                    ("Sender Address", 150, 'center'),
                    ("Sender Area", 100, 'center'),
                    ("Sender Pincode", 80, 'center'),
                    ("Receiver Name", 150, 'center'),
                    ("Receiver Phone", 100, 'center'),
                    ("Receiver Address", 150, 'center'),
                    ("Receiver Area", 100, 'center'),
                    ("Receiver Pincode", 80, 'center'),
                    ("Time", 150, 'center'),
                    ("Amount", 100, 'e')  # Right-aligned for currency
                ]
                
                for col_name, width, anchor in columns_config:
                    tree.column(col_name, width=width, anchor=anchor)
                    tree.heading(col_name, text=col_name)
                
                # Format amount as currency when inserting data
                for i in data_retr:
                    formatted_amount = f"₹{i[20]:.2f}"  # Assuming amount is at index 20
                    values = (
                        i[0], i[1], i[3],  # User ID, Name, Service Type
                        i[4], i[5], i[6], i[7], i[8],  # Sender details
                        i[9], i[10], i[11], i[12], i[13],  # Receiver details
                        i[21].strftime("%Y-%m-%d %H:%M"),  # Time
                        formatted_amount
                    )
                    if count%2 == 0:
                        tree.insert("", "end", values=values, tags=('even',))
                    else:
                        tree.insert("", "end", values=values, tags=('odd',))
                    count += 1

                def csv_file_dialog():
                    msg_var = messagebox.askokcancel('Caution', 'Existing data will be overwritten!')
                    #.csv and not *.csv. '' used not "" for .csv
                    if msg_var==1:
                        filename = filedialog.askopenfilename(parent=fourth, initialdir='D:', title='Select a file', filetypes=[("CSV files", '.csv')])
                        if filename!="":
                            file = open(filename, 'w')
                        else:
                            return
                        return file

                    else:
                        return

                def save_csv_all():
                    file_all = csv_file_dialog()
                    if file_all==None:
                        return
                    else:
                        writer = csv.writer(file_all)
                        writer.writerow(tree.columns())
                        writer.writerows(data_retr)
                        file_all.close()

                def save_csv_table():
                    file_table = csv_file_dialog()
                    if file_table==None:
                        return
                    else:
                        writer = csv.writer(file_table)


                another_frame = tk.Frame(fourth, bd=0, bg='white')
                another_frame.pack(pady=20)

                entry_label = tk.Label(another_frame, text='Enter search term: ', font=('default', 12), bg='white')
                entry_label.pack(pady=20, padx=10, side='left', anchor='nw')

                entry_stat = tk.Entry(another_frame, width=35, bg='#cecaca')
                entry_stat.pack(pady=20, padx=10, ipadx=4)
                entry_stat.bind('<Return>', stats_select)

                csv_btn_all = tk.Button(another_frame, text='Save all records as csv file: ', width=20, height=1,
                    bg='light blue', activebackground='light blue',
                    relief='solid', bd=1, command=save_csv_all)
                csv_btn_all.pack(pady=20)

                csv_btn_table = tk.Button(another_frame, text='Save all records as csv file: ', width=20, height=1,
                    bg='light blue', activebackground='light blue',
                    relief='solid', bd=1, command=save_csv_table)
                csv_btn_table.pack(pady=20)

                d_base.close()
                fourth.mainloop()

        trans_user_combo = ttk.Combobox(second, state='readonly', values=['< Select >','Post', 'Speedpost', 'Parcel'])
        trans_user_combo.current(0)
        trans_user_combo.bind('<<ComboboxSelected>>', selected_combo)
        trans_user_combo.pack(pady=20, padx=100)


    else:
        win_width = 600
        win_height = 500

        screen_width = second.winfo_screenwidth()#1536
        screen_height = second.winfo_screenheight()#864

        x = (screen_width/2) - (win_width/2)
        y = (screen_height/2) - (win_height/2)

        second.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')

        second.title(f'Logged in as {user}')
        second.config(bg='#fff2ab')

        def edit_details_win():
            welcome_label.config(text='Edit details', font=('Arial Black', 25))

            def rep_update_switch(event):
                global win_user
                win_user = username_entry.get()

                bool_var = update_entry(win_user, event, username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry, data_ret[0][0])

                if bool_var:
                    win_user = username_entry.get()

                    for widgets in tmp_frame.winfo_children():
                        widgets.destroy()
                    tmp_frame.forget()

                    second.title(f'Logged in as {win_user}')

                    welcome_label.config(text='Welcome', font=('Arial Black', 25))

                    tmp_frame_widgets()

            for widgets in tmp_frame.winfo_children():
                widgets.destroy()

            tmp_frame.pack(pady=30)

            database = sql.connect(
                host='localhost',
                user='root',
                passwd='admin',
                database='post_database'
                )

            my_sor = database.cursor()
            sql_statement = "SELECT * FROM Users_data WHERE user_name='{}'".format(win_user)
            my_sor.execute(sql_statement)

            data_ret = my_sor.fetchall()

            username_entry = tk.Entry(tmp_frame, bd=0, bg='#cecaca')
            userpassword_entry = tk.Entry(tmp_frame, bd=0, bg='#cecaca')
            usercity_entry = tk.Entry(tmp_frame, bd=0, bg='#cecaca')
            userphone_entry = tk.Entry(tmp_frame, bd=0, bg='#cecaca')
            useraddress_entry = tk.Entry(tmp_frame, bd=0, bg='#cecaca')

            username_entry.bind('<Return>', rep_update_switch)
            userpassword_entry.bind('<Return>', rep_update_switch)
            usercity_entry.bind('<Return>', rep_update_switch)
            userphone_entry.bind('<Return>', rep_update_switch)
            useraddress_entry.bind('<Return>', rep_update_switch)

            username_entry.insert(0, data_ret[0][1])
            userpassword_entry.insert(0, data_ret[0][2])
            usercity_entry.insert(0, data_ret[0][3])
            userphone_entry.insert(0, data_ret[0][4])
            useraddress_entry.insert(0, data_ret[0][5])

            username_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=0, column=0)
            userpassword_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=0, column=1)
            usercity_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=1, column=0)
            userphone_entry.grid(padx=25, pady=10, ipadx=50, ipady=3, row=1, column=1)
            useraddress_entry.grid(padx=25, pady=10, ipadx=150, ipady=3, row=2, column=0, columnspan=2)

            username_entry.focus()

            tmp_label = tk.Label(tmp_frame, text='Press <Return> key when done!', bg='white')
            tmp_label.grid(row=3, column=0, columnspan=2, padx=25, pady=10)

            database.commit()
            database.close()


        menubar = tk.Menu(second)
        second.config(menu=menubar)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Edit details', command=edit_details_win)

        edit_menu.add_separator()

        edit_menu.add_command(label='Logout', command=back_func)
        edit_menu.add_command(label='Exit', command=close_func)

        welcome_label = tk.Label(second, text='Welcome', font=('Arial Black', 25), bg='#fff2ab')
        welcome_label.pack(pady=15)

        tmp_frame = tk.Frame(second, bd=0, bg='white')

        def tmp_frame_widgets():
            tmp_frame.pack(padx=20, pady=30, anchor='nw')
            var = tk.IntVar(second)

            def clicked(value):

                if value==1:
                    post_proc(root, second, win_user)

                elif value==2:
                    speedpost_proc(root, second, win_user)

                elif value==3:
                    parcel_proc(root, second, win_user)

            tk.Radiobutton(tmp_frame, text='Post', variable=var, value=1, cursor='hand2',
                bg='#4dd2ff', activebackground='#4dd2ff',
                command=lambda: clicked(var.get())).grid(row=2, column=0, pady=20, padx=20, ipadx=40)

            tk.Radiobutton(tmp_frame, text='Speedpost', variable=var, value=2, cursor='hand2',
                bg='#4dd2ff', activebackground='#4dd2ff',
                command=lambda: clicked(var.get())).grid(row=2, column=1, pady=20, padx=20, ipadx=40)

            tk.Radiobutton(tmp_frame, text='Parcel', variable=var, value=3, cursor='hand2',
                bg='#4dd2ff', activebackground='#4dd2ff',
                command=lambda: clicked(var.get())).grid(row=2, column=2, pady=20, padx=20, ipadx=40)

            in_tmp_frame = tk.Frame(tmp_frame, bg='white', bd=0)
            in_tmp_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=15, sticky='W')

            tk.Label(in_tmp_frame, text='*', bg='white', fg='red').pack(side='left')
            tk.Label(in_tmp_frame, text='Our services are valid within Tamil Nadu only', bg='white').pack(side='left')
            
        tmp_frame_widgets()

    second.mainloop()
