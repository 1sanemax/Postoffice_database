import tkinter as tk
import mysql.connector as sql
from tkinter import messagebox

def save_to_admin_table(data):
    """Saves to the admin table with correct columns"""
    try:
        db = sql.connect(
            host='localhost',
            user = '**',#replace with your username
	        passwd = '**',#replace with your password
            database='post_database'
        )
        cursor = db.cursor()
        
        query = """INSERT INTO admin 
                  (username, servicetype, sendername, senderphonenumber, 
                  senderaddress, senderarea, senderpincode, recievername, 
                  recieverphonenumber, recieveraddress, recieverarea, 
                  recieverpincode, amount)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            data['username'],
            data['servicetype'],  # This should already include the priority
            data['sendername'],
            data['senderphonenumber'],
            data['senderaddress'],
            data['senderarea'],
            data['senderpincode'],
            data['recievername'],
            data['recieverphonenumber'],
            data['recieveraddress'],
            data['recieverarea'],
            data['recieverpincode'],
            data.get('amount', 0)
        )
        cursor.execute(query, values)
        db.commit()
        return True
        
    except sql.Error as err:
        db.rollback()
        raise ValueError(f"Database error: {err.msg}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            
def save_transaction(transaction_data):
    """Save transaction with all required columns"""
    try:
        db = sql.connect(
            host='localhost',
            user = '**',#replace with your username
	        passwd = '**',#replace with your password
            database='post_database'
        )
        cursor = db.cursor()
        
        # Handle Speedpost priority - ensure consistent formatting
        service_type = transaction_data['service_type']
        if service_type == 'Speedpost' and 'delivery_priority' in transaction_data:
            service_type = f"Speedpost-{transaction_data['delivery_priority']}"
        
        # Insert into Transaction_details
        query = """INSERT INTO Transaction_details 
                  (user_id, user_name, service_type, 
                  sender_name, sender_phone, sender_address, sender_area, sender_pincode,
                  receiver_name, receiver_phone, receiver_address, receiver_area, receiver_pincode,
                  weight_kg, dimensions, fragile, speed_delivery, vpp, 
                  base_amount, total_amount, transaction_time)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
        
        values = (
            transaction_data.get('user_id', ''),
            transaction_data['user_name'],
            service_type,
            transaction_data['sender_name'],
            transaction_data['sender_phone'],
            transaction_data['sender_address'],
            transaction_data['sender_area'],
            transaction_data['sender_pincode'],
            transaction_data['receiver_name'],
            transaction_data['receiver_phone'],
            transaction_data['receiver_address'],
            transaction_data['receiver_area'],
            transaction_data['receiver_pincode'],
            transaction_data.get('weight_kg', 0),
            transaction_data.get('dimensions', ''),
            transaction_data.get('fragile', False),
            transaction_data.get('speed_delivery', False),
            transaction_data.get('vpp', False),
            transaction_data.get('base_amount', 0),
            transaction_data.get('total_amount', 0)
        )
        
        cursor.execute(query, values)
        db.commit()
        
        # Prepare data for admin table - ensure consistent service_type
        admin_data = {
            'username': transaction_data['user_name'],
            'servicetype': service_type,  # Use the formatted service type
            'sendername': transaction_data['sender_name'],
            'senderphonenumber': transaction_data['sender_phone'],
            'senderaddress': transaction_data['sender_address'],
            'senderarea': transaction_data['sender_area'],
            'senderpincode': transaction_data['sender_pincode'],
            'recievername': transaction_data['receiver_name'],
            'recieverphonenumber': transaction_data['receiver_phone'],
            'recieveraddress': transaction_data['receiver_address'],
            'recieverarea': transaction_data['receiver_area'],
            'recieverpincode': transaction_data['receiver_pincode'],
            'amount': transaction_data.get('total_amount', 0)
        }
        
        # Save to admin table
        save_to_admin_table(admin_data)
        
        return True
        
    except sql.Error as err:
        db.rollback()
        raise ValueError(f"Database error: {err.msg}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Add validation functions
def validate_phone_number(phone):
    return phone.isdigit() and len(phone) == 10

def validate_pincode(pincode):
    return pincode.isdigit() and len(pincode) == 6

def entry_func_repo(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry, bgcolor):

    def username_tab(event):
        if event.keysym=='Tab' and event.state!=9:
            userpassword_entry_bind(event)
            username_leave_bind(event)
        elif event.keysym=='Tab' and event.state==9:
            useraddress_entry_bind(event)
            username_leave_bind(event)

    def userpassword_tab(event):
        if event.keysym=='Tab'and event.state!=9:
            usercity_entry_bind(event)
            userpassword_leave_bind(event)
        elif event.keysym=='Tab' and event.state==9:
            username_entry_bind(event)
            userpassword_leave_bind(event)

    def usercity_tab(event):
        if event.keysym=='Tab' and event.state!=9:
            userphone_entry_bind(event)
            usercity_leave_bind(event)
        elif event.keysym=='Tab' and event.state==9:
            userpassword_entry_bind(event)
            usercity_leave_bind(event)

    def userphone_tab(event):
        if event.keysym=='Tab' and event.state!=9:
            useraddress_entry_bind(event)
            userphone_leave_bind(event)
        elif event.keysym=='Tab' and event.state==9:
            usercity_entry.focus()
            usercity_entry_bind(event)
            userphone_leave_bind(event)

    def useraddress_tab(event):
        if event.keysym=='Tab' and event.state!=9:
            username_entry_bind(event)
            useraddress_leave_bind(event)
        elif event.keysym=='Tab' and event.state==9:
            userphone_entry_bind(event)
            useraddress_leave_bind(event)

    def username_entry_bind(event):
        username_entry.configure(state='normal')
        if username_entry.get()=='Enter username':
            username_entry.delete(0, 'end')
        username_entry.configure(bg=bgcolor)
        username_entry.bind('<Tab>', username_tab)

    def userpassword_entry_bind(event):
        userpassword_entry.configure(state='normal')
        if userpassword_entry.get()=='Enter password':
            userpassword_entry.delete(0, 'end')
        userpassword_entry.configure(bg=bgcolor)
        userpassword_entry.bind('<Tab>', userpassword_tab)

    def useraddress_entry_bind(event):
        useraddress_entry.configure(state='normal')
        if useraddress_entry.get()=='Enter address':
            useraddress_entry.delete(0, 'end')
        useraddress_entry.configure(bg=bgcolor)
        useraddress_entry.bind('<Tab>', useraddress_tab)

    def usercity_entry_bind(event):
        usercity_entry.configure(state='normal')
        if usercity_entry.get()=='Enter city':
            usercity_entry.delete(0, 'end')
        usercity_entry.configure(bg=bgcolor)
        usercity_entry.bind('<Tab>', usercity_tab)

    def userphone_entry_bind(event):
        userphone_entry.configure(state='normal')
        if userphone_entry.get()=='Enter phone number':
            userphone_entry.delete(0, 'end')
        userphone_entry.configure(bg=bgcolor)
        userphone_entry.bind('<Tab>', userphone_tab)

    def username_leave_bind(event):
        if not username_entry.get():
            username_entry.insert(0, 'Enter username')
            username_entry.configure(state='disabled')

    def userpassword_leave_bind(event):
        if not userpassword_entry.get():
            userpassword_entry.insert(0, 'Enter password')
            userpassword_entry.configure(state='disabled')

    def useraddress_leave_bind(event):
        if not useraddress_entry.get():
            useraddress_entry.insert(0, 'Enter address')
            useraddress_entry.configure(state='disabled')

    def usercity_leave_bind(event):
        if not usercity_entry.get():
            usercity_entry.insert(0, 'Enter city')
            usercity_entry.configure(state='disabled')

    def userphone_leave_bind(event):
        if not userphone_entry.get():
            userphone_entry.insert(0, 'Enter phone number')
            userphone_entry.configure(state='disabled')


    username_entry.insert(0, 'Enter username')
    userpassword_entry.insert(0, 'Enter password')
    usercity_entry.insert(0, 'Enter city')
    userphone_entry.insert(0, 'Enter phone number')
    useraddress_entry.insert(0, 'Enter address')

    username_entry.configure(state='disabled')
    userpassword_entry.configure(state='disabled')
    usercity_entry.configure(state='disabled')
    userphone_entry.configure(state='disabled')
    useraddress_entry.configure(state='disabled')

    username_entry.bind('<Button-1>', username_entry_bind)
    userpassword_entry.bind('<Button-1>', userpassword_entry_bind)
    usercity_entry.bind('<Button-1>', usercity_entry_bind)
    userphone_entry.bind('<Button-1>', userphone_entry_bind)
    useraddress_entry.bind('<Button-1>', useraddress_entry_bind)

    username_entry.bind('<Leave>', username_leave_bind)
    userpassword_entry.bind('<Leave>', userpassword_leave_bind)
    usercity_entry.bind('<Leave>', usercity_leave_bind)
    userphone_entry.bind('<Leave>', userphone_leave_bind)
    useraddress_entry.bind('<Leave>', useraddress_leave_bind)

def delete_entry_boxes(username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry):
    username_entry.delete(0, 'end')
    userpassword_entry.delete(0, 'end')
    usercity_entry.delete(0, 'end')
    userphone_entry.delete(0, 'end')
    useraddress_entry.delete(0, 'end')

def update_entry(user, event, username_entry, userpassword_entry, usercity_entry, userphone_entry, useraddress_entry, id):

    database = sql.connect(
        host='localhost',
        user = '**',#replace with your username
	    passwd = '**',#replace with your password
        database='post_database'
        )

    my_sor = database.cursor()

    sql_statement = "UPDATE Users_data SET user_name='{}', password='{}', city='{}', phone_no={}, address='{}' WHERE user_id='{}'".format(username_entry.get(), userpassword_entry.get(), usercity_entry.get(), int(userphone_entry.get()), useraddress_entry.get(), id)
    bool_var = False

    try:
        if (len(username_entry.get())<8 or len(username_entry.get())>24) and user!='root':
            messagebox.showerror('Error', 'Error \nUsername must contain at least 8 characters\nand at most 25 characters!')

        elif (len(userpassword_entry.get())<8 or len(userpassword_entry.get())>20) and user!='root':
            messagebox.showerror('Error', 'Error \nPassword must contain at least 8 characters\nand at most 20 characters!')

        elif len(username_entry.get())==0 or len(userpassword_entry.get())==0 or len(usercity_entry.get())==0 or len(userphone_entry.get())==0 or len(useraddress_entry.get())==0:
            messagebox.showerror('Error', 'Fill valid information!')

        else:
            my_sor.execute(sql_statement)
            messagebox.showinfo('Success', 'Edited successfully')
            bool_var = True

    except sql.errors.IntegrityError:
        messagebox.showerror('Error', 'Username/Password already taken \nPlease enter new details')
        bool_var = False

    database.commit()
    database.close()

    return bool_var
