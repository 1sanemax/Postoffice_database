import tkinter as tk
from tkinter import ttk
import mysql.connector as sql
from tkinter import messagebox
from Repository import save_transaction, save_to_admin_table 

trans_db_bool = False
def trans_db(area, pincode, person):
    database = sql.connect(
        host='localhost',
        user='root',
        passwd='admin',
        database='sample_import'
        )

    cur = database.cursor()
    cur.execute('SHOW tables')

    pincodes = tk.Toplevel()
    pincodes.geometry('800x600')
    pincodes.title('Select the locality and pincode')
    pincodes.config(bg='#fff2ab')
    pincodes.focus()

    def close_func():
        database.close()
        pincodes.destroy()
    def get_table(event):
        table = list_box.get('anchor')

        cur.execute('SET @table="{}"'.format(table))
        cur.execute('SET @a=CONCAT("SELECT * FROM ", @table)')
        cur.execute('PREPARE stmt FROM @a')
        cur.execute('EXECUTE stmt')

        ret_data = cur.fetchall()

        cur.execute('DEALLOCATE PREPARE stmt')

        database.close()
        list_box.forget()

        style = ttk.Style(pincodes)

        style.theme_use('default')
        style.configure('Treeview',
            background='white',
            foreground='black',
            rowheight=25,
            fieldbackground='white')

        style.map('Treeview',
            background=[('selected', 'yellow')],
            foreground=[('selected', 'black')])

        tree_frame = tk.Frame(pincodes)
        tree_frame.pack(pady=20)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')

        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
        tree.pack()

        tree_scroll.config(command=tree.yview)

        tree['columns'] = ("Area", "Pincode")

        tree.column("#0", stretch='no', width=0)
        tree.column("Area", anchor='center', width=220)
        tree.column("Pincode", anchor='center', width=160)

        tree.heading('#0', text='')
        tree.heading('Area', text='Area')
        tree.heading('Pincode', text='Pincode')

        tree.tag_configure('odd', background='white')
        tree.tag_configure('even', background='lightgreen')

        tree.config(takefocus=0)

        count = 0
        for i in ret_data:
            if count%2==0:
                tree.insert(parent='', index='end', iid=count, text='', values=(i[1], i[2]), tags=('even',))
            else:
                tree.insert(parent='', index='end', iid=count, text='', values=(i[1], i[2]), tags=('odd',))
            count+= 1

        def selection():
            global values
            values = tree.item(tree.focus(), 'values')

            if values=='':
                tk.messagebox.showerror('Error', 'Select an entry first')
                pincodes.focus()
                return

            else:
                pincodes.destroy()
                area.insert(0, values[0])
                pincode.insert(0, values[1])


        select_button = tk.Button(pincodes, text='Select corresponding entry',
            bg='lightblue', activebackground='lightblue',
            relief='solid', bd=1,
            command=selection)
        select_button.pack(pady=20, ipadx=8, ipady=2)


    list_table = []
    for i in cur.fetchall():
        if i!=('transaction_details',) and i!=('users_data',):
            list_table.append((i[0]).capitalize())

    pin_header = tk.Label(pincodes, text=f'Select {person}\'s district: ',
        font=('Arial black', 20), bg='#fff2ab')
    pin_header.pack(pady=5)

    lst_var = tk.StringVar(value=list_table)
    list_box = tk.Listbox(pincodes, listvariable=lst_var, cursor='hand2',
        height=15, width=45, justify='center',
        font=('default', 11),
        selectbackground='light green', selectforeground='black',
        selectmode='single')
    list_box.pack(padx=30, pady=40)
    list_box.bind('<<ListboxSelect>>', get_table)

    pincodes.protocol('WM_DELETE_WINDOW', close_func)

    pincodes.mainloop()

def parcel_proc(root, second, user):
    main_win = tk.Toplevel()
    main_win.title('Parcel Service')
    main_win.resizable(False, False)
    main_win.config(bg='#fff2ab')

    # ========== CALCULATION LOGIC ========== #
    def calculate_parcel_charge(weight, dimensions, fragile=False, speed=False, vpp=False):
        """Calculate parcel charges with optional services"""
        # Base rate calculation
        base_rate = 100 + (max(0, weight - 1) * 50)  # ₹100 for 1kg + ₹50/kg thereafter
        
        # Apply service charges
        total = base_rate
        if fragile:
            total += base_rate * 0.05
        if speed:
            total += base_rate * 0.05
        if vpp:
            total += base_rate * 0.05
        
        # Add GST
        total *= 1.18  # 18% GST
        
        return round(total, 2)

    # ========== WIDGET CREATION ========== #
    # Main frames
    header_frame = tk.Frame(main_win, bg='#fff2ab')
    sender_frame = tk.LabelFrame(main_win, text="Sender Details", bg='white')
    receiver_frame = tk.LabelFrame(main_win, text="Receiver Details", bg='white')
    parcel_frame = tk.LabelFrame(main_win, text="Parcel Details", bg='white')
    button_frame = tk.Frame(main_win, bg='#fff2ab')

    # Grid layout
    header_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
    sender_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
    receiver_frame.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
    parcel_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    # Header
    tk.Label(header_frame, text="PARCEL SERVICE", font=('Arial Black', 18), bg='#fff2ab').pack()
    tk.Label(header_frame, text=f"User: {user}", font=('Arial', 10), bg='#fff2ab').pack()

    # ========== SENDER/RECEIVER FIELDS ========== #
    def create_address_fields(parent_frame):
        """Create standardized address fields"""
        fields = {}
        labels = ['Name:', 'Phone:', 'Address:', 'Area:', 'Pincode:']
        
        for i, text in enumerate(labels):
            tk.Label(parent_frame, text=text, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
            entry = tk.Entry(parent_frame, bg='#cecaca')
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            fields[text.replace(':', '').lower()] = entry
        
        # Pincode selection button
        btn = tk.Button(parent_frame, text='Select Area/Pincode',
                       command=lambda: trans_db(fields['area'], fields['pincode'], 
                                              'sender' if parent_frame == sender_frame else 'receiver'),
                       bg='lightblue')
        btn.grid(row=3, column=2, rowspan=2, padx=5)
        return fields

    sender_fields = create_address_fields(sender_frame)
    receiver_fields = create_address_fields(receiver_frame)

    # ========== PARCEL DETAILS ========== #
    # Weight
    tk.Label(parcel_frame, text="Weight (kg):", bg='white').grid(row=0, column=0, sticky='e', padx=5, pady=2)
    weight_entry = tk.Spinbox(parcel_frame, from_=0.1, to=25.0, increment=0.1, width=8)
    weight_entry.grid(row=0, column=1, sticky='w', padx=5, pady=2)

    # Dimensions
    tk.Label(parcel_frame, text="Dimensions (cm):", bg='white').grid(row=1, column=0, sticky='e', padx=5, pady=2)
    dim_frame = tk.Frame(parcel_frame, bg='white')
    dim_frame.grid(row=1, column=1, sticky='w')
    
    length_entry = tk.Entry(dim_frame, width=5)
    width_entry = tk.Entry(dim_frame, width=5)
    height_entry = tk.Entry(dim_frame, width=5)
    
    for widget in [length_entry, tk.Label(dim_frame, text="L x"), 
                  width_entry, tk.Label(dim_frame, text="W x"),
                  height_entry, tk.Label(dim_frame, text="H")]:
        widget.pack(side='left')

    # Service Options
    options_frame = tk.Frame(parcel_frame, bg='white')
    options_frame.grid(row=2, column=0, columnspan=2, pady=5)
    
    fragile_var = tk.IntVar()
    speed_var = tk.IntVar()
    vpp_var = tk.IntVar()
    
    tk.Checkbutton(options_frame, text="Fragile (+5%)", variable=fragile_var, bg='white').pack(side='left', padx=5)
    tk.Checkbutton(options_frame, text="Speed Delivery (+5%)", variable=speed_var, bg='white').pack(side='left', padx=5)
    tk.Checkbutton(options_frame, text="VPP (+5%)", variable=vpp_var, bg='white').pack(side='left', padx=5)

    # Amount Display
    amount_label = tk.Label(parcel_frame, text="Total Amount: ₹0.00", 
                           font=('Arial', 12, 'bold'), bg='white')
    amount_label.grid(row=3, column=0, columnspan=2, pady=10)

    # ========== BUTTONS ========== #
    def calculate_amount():
        try:
            weight = float(weight_entry.get())
            length = float(length_entry.get())
            width = float(width_entry.get())
            height = float(height_entry.get())
            
            if weight <= 0 or length <= 0 or width <= 0 or height <= 0:
                raise ValueError("All values must be positive numbers")
            
            total = calculate_parcel_charge(
                weight=weight,
                dimensions=(length, width, height),
                fragile=fragile_var.get(),
                speed=speed_var.get(),
                vpp=vpp_var.get()
            )
            
            main_win.calculated_amount = total
            amount_label.config(text=f"Total Amount: ₹{total:.2f}")
            submit_btn.config(state='normal')
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")

    def submit_parcel():
        try:
            # Validate required fields
            required_fields = {
                'sender': [sender_fields['name'], sender_fields['phone'], 
                        sender_fields['address'], sender_fields['area'], 
                        sender_fields['pincode']],
                'receiver': [receiver_fields['name'], receiver_fields['phone'],
                            receiver_fields['address'], receiver_fields['area'],
                            receiver_fields['pincode']]
            }
            
            for field_type, fields in required_fields.items():
                for field in fields:
                    if not field.get().strip():
                        raise ValueError(f"Please fill all {field_type} details")
            
            # Prepare transaction data
            transaction_data = {
                'user_name': user,
                'service_type': 'Parcel',
                'sender_name': sender_fields['name'].get().strip(),
                'sender_phone': sender_fields['phone'].get().strip(),
                'sender_address': sender_fields['address'].get().strip(),
                'sender_area': sender_fields['area'].get().strip(),
                'sender_pincode': sender_fields['pincode'].get().strip(),
                'receiver_name': receiver_fields['name'].get().strip(),
                'receiver_phone': receiver_fields['phone'].get().strip(),
                'receiver_address': receiver_fields['address'].get().strip(),
                'receiver_area': receiver_fields['area'].get().strip(),
                'receiver_pincode': receiver_fields['pincode'].get().strip(),
                'weight_kg': float(weight_entry.get()),
                'dimensions': f"{length_entry.get()}x{width_entry.get()}x{height_entry.get()}",
                'fragile': bool(fragile_var.get()),
                'speed_delivery': bool(speed_var.get()),
                'vpp': bool(vpp_var.get())
            }

            # Add calculated amount if available
            if hasattr(main_win, 'calculated_amount'):
                transaction_data['total_amount'] = main_win.calculated_amount
            else:
                raise ValueError("Please calculate the amount first!")
        
            # Save to both tables
            if save_transaction(transaction_data):
                # Also save to admin table
                admin_data = {
                    'username': user,
                    'servicetype': 'Parcel',
                    'sendername': sender_fields['name'].get().strip(),
                    'senderphonenumber': sender_fields['phone'].get().strip(),
                    'senderaddress': sender_fields['address'].get().strip(),
                    'senderarea': sender_fields['area'].get().strip(),
                    'senderpincode': sender_fields['pincode'].get().strip(),
                    'recievername': receiver_fields['name'].get().strip(),
                    'recieverphonenumber': receiver_fields['phone'].get().strip(),
                    'recieveraddress': receiver_fields['address'].get().strip(),
                    'recieverarea': receiver_fields['area'].get().strip(),
                    'recieverpincode': receiver_fields['pincode'].get().strip(),
                    'amount': main_win.calculated_amount
                }
                save_to_admin_table(admin_data)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    calc_btn = tk.Button(button_frame, text="Calculate Amount",
                        command=calculate_amount,
                        bg='#2196F3', fg='white')
    calc_btn.pack(side='left', padx=10, pady=5)

    submit_btn = tk.Button(button_frame, text="Submit Parcel",
                          command=submit_parcel,
                          state='disabled',
                          bg='#4CAF50', fg='white')
    submit_btn.pack(side='left', padx=10, pady=5)

    # ========== WINDOW MANAGEMENT ========== #
    def back_func():
        second.deiconify()
        main_win.destroy()

    def close_func():
        main_win.destroy()

    # Menu Bar
    menubar = tk.Menu(main_win)
    main_win.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Back", command=back_func)
    file_menu.add_command(label="Exit", command=close_func)

    main_win.mainloop()
    global amount_pending
    amount_pending = True
    

def post_proc(root, second, user):
    post_win = tk.Toplevel()
    post_win.title('Post Service')
    post_win.config(bg='#fff2ab')
    
    # Use grid exclusively for the main window
    post_win.grid_columnconfigure(0, weight=1)
    post_win.grid_columnconfigure(1, weight=1)
    
    # Create frames using grid
    header_frame = tk.Frame(post_win, bg='#fff2ab')
    header_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
    
    sen_frame = tk.LabelFrame(post_win, text="Sender Details", bg='white', padx=10, pady=10)
    sen_frame.grid(row=1, column=0, padx=15, pady=20, sticky='nsew')
    
    rec_frame = tk.LabelFrame(post_win, text="Receiver Details", bg='white', padx=10, pady=10)
    rec_frame.grid(row=1, column=1, padx=15, pady=20, sticky='nsew')
    
    button_frame = tk.Frame(post_win, bg='#fff2ab')
    button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
    
    # Configure frame internal grids
    sen_frame.grid_columnconfigure(1, weight=1)
    rec_frame.grid_columnconfigure(1, weight=1)
    
    # Header
    tk.Label(header_frame, text="Post Service", font=('Arial Black', 16), bg='#fff2ab').pack()
    tk.Label(header_frame, text=f"Logged in as: {user}", bg='#fff2ab').pack()
    
    # Sender Fields
    s_header_label = tk.Label(sen_frame, text="Sender's details", font=('Arial Black', 14), bg='white')
    s_header_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    
    labels = ['Name:', 'Phone:', 'Address:', 'Area:', 'Pincode:']
    sender_entries = []
    
    for i, text in enumerate(labels, start=1):
        tk.Label(sen_frame, text=text, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(sen_frame, bg='#cecaca')
        entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
        sender_entries.append(entry)
    
    # Add pincode button
    spin_frame = tk.Frame(sen_frame, bg='white')
    spin_frame.grid(row=5, column=2, padx=5)
    spin_button = tk.Button(spin_frame, text='Choose area/pincode', 
                          command=lambda: trans_db(sender_entries[3], sender_entries[4], 'sender'),
                          bg='lightblue', relief='solid')
    spin_button.pack(padx=5)
    
    # Receiver Fields
    r_header_label = tk.Label(rec_frame, text="Receiver's details", font=('Arial Black', 14), bg='white')
    r_header_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    
    receiver_entries = []
    for i, text in enumerate(labels, start=1):
        tk.Label(rec_frame, text=text, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(rec_frame, bg='#cecaca')
        entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
        receiver_entries.append(entry)
    
    # Add pincode button
    rpin_frame = tk.Frame(rec_frame, bg='white')
    rpin_frame.grid(row=5, column=2, padx=5)
    rpin_button = tk.Button(rpin_frame, text='Choose area/pincode', 
                          command=lambda: trans_db(receiver_entries[3], receiver_entries[4], 'receiver'),
                          bg='lightblue', relief='solid')
    rpin_button.pack(padx=5)
    
    # Submit Button
    submit_btn = tk.Button(button_frame, text="Submit Post", 
                          command=lambda: submit_post(),
                          bg='#4CAF50', fg='white',
                          font=('Arial', 12, 'bold'))
    submit_btn.pack(pady=10)
    
    def submit_post():
        try:
            transaction_data = {
                'user_name': user,
                'service_type': 'Post',
                'sender_name': sender_entries[0].get().strip(),
                'sender_phone': sender_entries[1].get().strip(),
                'sender_address': sender_entries[2].get().strip(),
                'sender_area': sender_entries[3].get().strip(),
                'sender_pincode': sender_entries[4].get().strip(),
                'receiver_name': receiver_entries[0].get().strip(),
                'receiver_phone': receiver_entries[1].get().strip(),
                'receiver_address': receiver_entries[2].get().strip(),
                'receiver_area': receiver_entries[3].get().strip(),
                'receiver_pincode': receiver_entries[4].get().strip(),
                'base_amount': 10.00,
                'total_amount': 10.00
            }
            
            if save_transaction(transaction_data):
                messagebox.showinfo("Success", "Post transaction saved!")
                # Clear form
                for entry in sender_entries + receiver_entries:
                    entry.delete(0, 'end')
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Menu functions
    def back_func():
        second.deiconify()
        post_win.destroy()
    
    def close_func():
        post_win.destroy()
    
    # Menu bar
    menubar = tk.Menu(post_win)
    post_win.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Back", command=back_func)
    file_menu.add_command(label="Exit", command=close_func)
    
    post_win.mainloop()

def speedpost_proc(root, second, user):
    speedpost_win = tk.Toplevel()
    speedpost_win.title('Speedpost Service')
    speedpost_win.config(bg='#fff2ab')
    
    # Use grid exclusively for the main window
    speedpost_win.grid_columnconfigure(0, weight=1)
    speedpost_win.grid_columnconfigure(1, weight=1)
    
    # Create frames using grid
    header_frame = tk.Frame(speedpost_win, bg='#fff2ab')
    header_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
    
    sen_frame = tk.LabelFrame(speedpost_win, text="Sender Details", bg='white', padx=10, pady=10)
    sen_frame.grid(row=1, column=0, padx=15, pady=20, sticky='nsew')
    
    rec_frame = tk.LabelFrame(speedpost_win, text="Receiver Details", bg='white', padx=10, pady=10)
    rec_frame.grid(row=1, column=1, padx=15, pady=20, sticky='nsew')
    
    service_frame = tk.LabelFrame(speedpost_win, text="Speedpost Details", bg='white', padx=10, pady=10)
    service_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky='ew')
    
    button_frame = tk.Frame(speedpost_win, bg='#fff2ab')
    button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
    
    # Configure frame internal grids
    sen_frame.grid_columnconfigure(1, weight=1)
    rec_frame.grid_columnconfigure(1, weight=1)
    service_frame.grid_columnconfigure(1, weight=1)
    
    # Header
    tk.Label(header_frame, text="Speedpost Service", font=('Arial Black', 16), bg='#fff2ab').pack()
    tk.Label(header_frame, text=f"Logged in as: {user}", bg='#fff2ab').pack()
    
    # Sender Fields (same as post_proc)
    labels = ['Name:', 'Phone:', 'Address:', 'Area:', 'Pincode:']
    sender_entries = []
    
    for i, text in enumerate(labels, start=1):
        tk.Label(sen_frame, text=text, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(sen_frame, bg='#cecaca')
        entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
        sender_entries.append(entry)
    
    # Sender Pincode Button
    spin_button = tk.Button(sen_frame, text='Choose area/pincode',
                          command=lambda: trans_db(sender_entries[3], sender_entries[4], 'sender'),
                          bg='lightblue', relief='solid')
    spin_button.grid(row=4, column=2, rowspan=2, padx=5)
    
    # Receiver Fields (same as post_proc)
    receiver_entries = []
    for i, text in enumerate(labels, start=1):
        tk.Label(rec_frame, text=text, bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(rec_frame, bg='#cecaca')
        entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
        receiver_entries.append(entry)
    
    # Receiver Pincode Button
    rpin_button = tk.Button(rec_frame, text='Choose area/pincode',
                          command=lambda: trans_db(receiver_entries[3], receiver_entries[4], 'receiver'),
                          bg='lightblue', relief='solid')
    rpin_button.grid(row=4, column=2, rowspan=2, padx=5)
    
    # Speedpost Specific Fields
    tk.Label(service_frame, text="Weight (grams):", bg='white').grid(row=0, column=0, sticky='e', padx=5, pady=2)
    weight_entry = tk.Entry(service_frame, bg='#cecaca')
    weight_entry.grid(row=0, column=1, sticky='w', padx=5, pady=2)
    
    tk.Label(service_frame, text="Delivery Priority:", bg='white').grid(row=1, column=0, sticky='e', padx=5, pady=2)
    priority_var = tk.StringVar(value="Standard")
    priorities = ["Standard", "Express", "Overnight"]
    priority_menu = tk.OptionMenu(service_frame, priority_var, *priorities)
    priority_menu.config(bg='#cecaca')
    priority_menu.grid(row=1, column=1, sticky='w', padx=5, pady=2)
    
    # Amount Calculation and Display
    amount_label = tk.Label(service_frame, text="Total Amount: ₹0.00", 
                           font=('Arial', 12, 'bold'), bg='white')
    amount_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Buttons
    calc_button = tk.Button(button_frame, text="Calculate Amount",
                          command=lambda: calculate_speedpost_charges(),
                          bg='#2196F3', fg='white')
    calc_button.pack(side='left', padx=10, pady=5)
    
    submit_button = tk.Button(button_frame, text="Submit Speedpost",
                            state='disabled',
                            command=lambda: submit_speedpost(),
                            bg='#4CAF50', fg='white')
    submit_button.pack(side='left', padx=10, pady=5)
    
    def calculate_speedpost_charges():
        try:
            weight = float(weight_entry.get())
            if weight <= 0:
                raise ValueError("Weight must be positive")
            
            # Base rate calculation
            base_rate = 50 + (weight * 0.5)  # ₹50 base + ₹0.50 per gram
            
            # Priority multiplier
            priority = priority_var.get()
            if priority == "Express":
                base_rate *= 1.5
            elif priority == "Overnight":
                base_rate *= 2.0
            
            # Add GST
            total_amount = round(base_rate * 1.18, 2)  # 18% GST
            
            # Update display
            amount_label.config(text=f"Total Amount: ₹{total_amount:.2f}")
            speedpost_win.calculated_amount = total_amount
            submit_button.config(state='normal')
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid weight: {str(e)}")
    
    def submit_speedpost():
        try:
            if not hasattr(speedpost_win, 'calculated_amount'):
                raise ValueError("Please calculate the amount first")
            
            transaction_data = {
                'user_name': user,
                'service_type': 'Speedpost',
                'sender_name': sender_entries[0].get().strip(),
                'sender_phone': sender_entries[1].get().strip(),
                'sender_address': sender_entries[2].get().strip(),
                'sender_area': sender_entries[3].get().strip(),
                'sender_pincode': sender_entries[4].get().strip(),
                'receiver_name': receiver_entries[0].get().strip(),
                'receiver_phone': receiver_entries[1].get().strip(),
                'receiver_address': receiver_entries[2].get().strip(),
                'receiver_area': receiver_entries[3].get().strip(),
                'receiver_pincode': receiver_entries[4].get().strip(),
                'weight_grams': float(weight_entry.get()),
                'delivery_priority': priority_var.get(),
                'base_amount': round(speedpost_win.calculated_amount / 1.18, 2),  # Pre-GST amount
                'total_amount': speedpost_win.calculated_amount
            }
            
            if save_transaction(transaction_data):
                messagebox.showinfo("Success", "Speedpost transaction saved!")
                # Clear form
                for entry in sender_entries + receiver_entries + [weight_entry]:
                    entry.delete(0, 'end')
                priority_var.set("Standard")
                amount_label.config(text="Total Amount: ₹0.00")
                submit_button.config(state='disabled')
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit: {str(e)}")
    
    # Menu functions
    def back_func():
        second.deiconify()
        speedpost_win.destroy()
    
    def close_func():
        speedpost_win.destroy()
    
    # Menu bar
    menubar = tk.Menu(speedpost_win)
    speedpost_win.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Back", command=back_func)
    file_menu.add_command(label="Exit", command=close_func)
    
    speedpost_win.mainloop()