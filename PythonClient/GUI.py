import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.ttk as ttk
from bson import ObjectId
import socket_connection
import socket


def tab1_contents(window, tab):
    drop_frame = tk.Frame(tab, pady=10) 
    drop_frame.pack()

    option1 = tk.StringVar(drop_frame)
    option1.set("Hotel")
    
    hotel_list = socket_connection.retrieve_hotels(global_socket, global_db)
    hotel_names = [d.get("name") for d in hotel_list]
    
    dropdown1 = tk.OptionMenu(drop_frame, option1, *hotel_names)
    dropdown1.pack(side="left")
    
    text_frame = tk.Frame(tab, pady=10) 
    text_frame.pack()
    
    field_label = tk.Label(text_frame, text="Field:")
    field_label.pack(side="left")
    field = tk.Entry(text_frame)
    field.pack(side="left")

    value_label = tk.Label(text_frame, text="Value:")
    value_label.pack(side="left")
    value = tk.Entry(text_frame)
    value.pack(side="left")

    # create the buttons
    button_frame = tk.Frame(tab, pady=10)
    button_frame.pack()

    update_button = tk.Button(button_frame, text="Update", command=lambda: update_command(option1.get(), field.get(), value.get()))
    update_button.pack(side="left", padx=10)
    
    def update_command(hotel, field, value):
        filter = str({'filter': {'name':hotel}, 'fields': {field:value}})
        res = socket_connection.query(global_socket, global_db, "hotels_db", "hotels", "update", filter)
        if res is not None:
            messagebox.showwarning("Message", res)
        
            
    def refresh_options(event):
        option1.set("Hotel")
        menu = dropdown1['menu']
        menu.delete(0, 'end')  # Remove all existing options
        
        hotel_list = socket_connection.retrieve_hotels(global_socket, global_db)
        hotel_names = [d.get("name") for d in hotel_list] # Get the updated list of hotel names
        for name in hotel_names:
            menu.add_command(label=name, command=tk._setit(option1, name))
    
    dropdown1.bind("<Button-1>", refresh_options)
    # tab.bind("<<NotebookTabChanged>>", refresh_options)

def tab2_contents(window, tab):
    text_frame = tk.Frame(tab, pady=10) 
    text_frame.pack()

    name_label = tk.Label(text_frame, text="Name:")
    name_label.pack(side="left")
    name = tk.Entry(text_frame)
    name.pack(side="left")

    button_frame = tk.Frame(tab, pady=10)
    button_frame.pack()

    add_button = tk.Button(button_frame, text="Add", command=lambda: add_command(name.get()))
    add_button.pack(side="left", padx=10)

    delete_button = tk.Button(button_frame, text="Delete", command=lambda: delete_command(name.get()))
    delete_button.pack(side="left", padx=10)
    
    def add_command(name):
        filter = str({'name': name})
        res = socket_connection.query(global_socket, global_db, "hotels_db", "hotels", "create", filter)
        if res is not None:
            messagebox.showwarning("Message", res)
            return
        else:
            messagebox.showinfo("Message", "No message received from the server")
        
    def delete_command(name):
        filter = str({'name': name})
        res = socket_connection.query(global_socket, global_db, "hotels_db", "hotels", "delete", filter)
        if res is not None:
            messagebox.showwarning("Message", res)
            return
        else:
            messagebox.showinfo("Message", "No message received from the server")

def tab3_contents(window, tab):
    hotel_list = socket_connection.retrieve_hotels(global_socket, global_db)
    
    # Upper treeview
    upper_frame = tk.Frame(tab)
    upper_frame.pack(fill='both', expand=True)

    upper_tree = ttk.Treeview(upper_frame, columns=('name'), selectmode='browse', show='headings')
    upper_tree.heading('#0', text='')
    upper_tree.column('#0', width=0)
    upper_tree.heading('name', text='Name')
    upper_tree.column('name', width=100)
    upper_tree.pack(fill='both', expand=True)

    # Lower treeview
    lower_frame = tk.Frame(tab)
    lower_frame.pack(fill='both', expand=True)

    lower_tree = ttk.Treeview(lower_frame, columns=('attribute', 'value'), selectmode='browse', show='headings')
    lower_tree.heading('#0', text='')
    lower_tree.column('#0', width=0)
    lower_tree.heading('attribute', text='Attribute')
    lower_tree.column('attribute', width=50)
    lower_tree.heading('value', text='Value')
    lower_tree.column('value', width=250)
    lower_tree.pack(fill='both', expand=True)

    # Function to populate the upper treeview with hotel names and document ids
    def populate_upper_tree(event):
        hotel_list = socket_connection.retrieve_hotels(global_socket, global_db)
        hotel_data = [(d.get("name"), d.get("_id")) for d in hotel_list]
        
        upper_tree.delete(*upper_tree.get_children())

        for i, (name, doc_id) in enumerate(hotel_data):
            upper_tree.insert(parent='', index='end', iid=i, values=(name, doc_id))

    def populate_lower_tree(event):
        selection = upper_tree.selection()
        hotel_list = socket_connection.retrieve_hotels(global_socket, global_db)
        if selection:
            sel = int(selection[0])
            hotel = hotel_list[sel]

            lower_tree.delete(*lower_tree.get_children())

            for i, (attribute, value) in enumerate(hotel.items()):
                lower_tree.insert(parent='', index='end', iid=i, values=(attribute, value))
                
    window.bind('<<NotebookTabChanged>>', populate_upper_tree)
    upper_tree.bind('<<TreeviewSelect>>', populate_lower_tree)

def tab4_contents(window, tab):
    pass
    upper_frame = tk.Frame(tab)
    upper_frame.pack(fill='both', expand=True)

    upper_tree = ttk.Treeview(upper_frame, columns=('name', 'checkin', 'checkout', 'roomtype'), selectmode='browse', show='headings')
    upper_tree.heading('#0', text='')
    upper_tree.column('#0', width=0)
    upper_tree.heading('name', text='Guest Name')
    upper_tree.column('name', width=80)
    upper_tree.heading('checkin', text='Check-In')
    upper_tree.column('checkin', width=80)
    upper_tree.heading('checkout', text='Check-Out')
    upper_tree.column('checkout', width=80)
    upper_tree.heading('roomtype', text='Room Type')
    upper_tree.column('roomtype', width=80)
    upper_tree.pack(fill='both', expand=True)
    
    def populate_upper_tree():
        reservation_list = socket_connection.query(global_socket, global_db, "hotels_db", "grand_hotel_reservations", "read", "")
        reservation_data = [(d.get("guest_name"), d.get("checkin_date"), d.get("checkout_date"), d.get("room_type")) for d in reservation_list]
        
        upper_tree.delete(*upper_tree.get_children())

        for i, (name, checkin, checkout, roomtype) in enumerate(reservation_data):
            upper_tree.insert(parent='', index='end', iid=i, values=(name, checkin, checkout, roomtype))
    
    populate_upper_tree()

def tab5_contents(window, tab):
    dbs_list = ['MongoDB', 'MySQL']
    
    # create the Migrate button
    migrate_frame = tk.Frame(tab)
    migrate_frame.pack()
    migrate_button = tk.Button(migrate_frame, text="Migrate MySQL to MongoDB", pady=10, command=lambda: migrate_command())
    migrate_button.pack()
    
    # create the DB selection dropdown menu and the "Set" button
    db_frame = tk.Frame(tab)
    db_frame.pack(pady=10)
    selected_db_label = tk.Label(db_frame, text="Selected DB: ")
    selected_db_label.pack(side=tk.LEFT)
    selected_db_var = tk.StringVar()
    selected_db_var.set(dbs_list[0])
    db_dropdown = tk.OptionMenu(db_frame, selected_db_var, *dbs_list)
    db_dropdown.pack(side=tk.LEFT)
    set_button = tk.Button(db_frame, text="Set", padx=10, command=lambda: set_command(selected_db_var.get()))
    set_button.pack(side=tk.LEFT, padx=10)

    # create the selected DB label
    selected_db_frame = tk.Frame(tab)
    selected_db_frame.pack()
    selected_db_label = tk.Label(selected_db_frame, text="Selected DB: ")
    selected_db_label.pack(side=tk.LEFT)
    selected_db_value = tk.Label(selected_db_frame, textvariable='')
    selected_db_value.pack(side=tk.LEFT, padx=5)
    
    
    def migrate_command():
        socket_connection.migration_query(global_socket, 'mysql', 'mongodb', 'hotels_db', 'hotels', 'migrate')
        messagebox.showwarning("Message", 'migration request sent')
    
    def set_command(selected_db):
        global global_db
        global_db = str(selected_db).lower()
        selected_db_value.config(text=selected_db)

    
global_socket = None
global_db = "mongodb"

def main():
    HOST = '127.0.0.1'
    PORT = 8080
    global global_socket
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        global_socket = s
        
        window = tk.Tk()
        window.title("SJHBP- Hotel Booking Platform")
        notebook = ttk.Notebook(window)
        notebook.pack()

        tabs = {'Add Field': tab1_contents, 'Add Hotel': tab2_contents, 'Hotel View': tab3_contents, 'Reservations': tab4_contents, 'Migrate': tab5_contents}

        for t in tabs:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=t)
            tabs[t](window, tab)
            
        window.mainloop()


if __name__ == "__main__":
    main()