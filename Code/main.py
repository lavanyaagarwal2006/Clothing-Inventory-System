import tkinter as tk
import mysql.connector
import datetime

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='qwertyuiop@1234567890',
    database='store'
)
mycursor = mydb.cursor()

# Create a tkinter window
window = tk.Tk()
window.title("Inventory Management System")

# Function to update stock levels and database records
def update_stock(item_id, item_name, quantity, table, status_label):
    try:
        if table == 'inventory':
            # Insert into inventory table
            query = "INSERT INTO inventory (item_id, item_name, stock) VALUES (%s, %s, %s)"
            values = (item_id, item_name, quantity)
        elif table == 'sales':
            # Update stock in inventory table and record sales
            query = "UPDATE inventory SET stock = stock - %s WHERE item_id = %s"
            values = (quantity, item_id)
            mycursor.execute(query, values)

            # Record sale
            current_datetime = datetime.datetime.now()
            query_sales = "INSERT INTO sales (item_id, quantity, sale_date) VALUES (%s, %s, %s)"
            values_sales = (item_id, quantity, current_datetime)
            mycursor.execute(query_sales, values_sales)
        elif table == 'returns':
            # Update stock in inventory table and record returns
            query = "UPDATE inventory SET stock = stock + %s WHERE item_id = %s"
            values = (quantity, item_id)
            mycursor.execute(query, values)

            # Record return
            current_datetime = datetime.datetime.now()
            query_returns = "INSERT INTO returns (item_id, quantity, return_date) VALUES (%s, %s, %s)"
            values_returns = (item_id, quantity, current_datetime)
            mycursor.execute(query_returns, values_returns)

        # Commit the transaction
        mydb.commit()

        # Display success message
        status_label.config(text=f"Stock updated successfully for {table}!", fg="green")

        # Execute the SELECT query to display the updated table
        mycursor.execute(f"SELECT * FROM {table}")
        results = mycursor.fetchall()
        for row in results:
            print(row)

    except mysql.connector.Error as error:
        # Display error message
        status_label.config(text=f"Error updating stock for {table}: {str(error)}", fg="red")

# Function to handle the "Add to Inventory" option
def add_to_inventory():
    add_window = tk.Toplevel(window)
    add_window.title("Add to Inventory")

    # Create GUI elements for adding to inventory
    item_id_label = tk.Label(add_window, text="Item ID:")
    item_id_label.pack()
    item_id_entry = tk.Entry(add_window)
    item_id_entry.pack()

    item_name_label = tk.Label(add_window, text="Item Name:")
    item_name_label.pack()
    item_name_entry = tk.Entry(add_window)
    item_name_entry.pack()

    quantity_label = tk.Label(add_window, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(add_window)
    quantity_entry.pack()

    status_label = tk.Label(add_window, text="")
    status_label.pack()

    add_button = tk.Button(
        add_window, text="Add to Inventory",
        command=lambda: update_stock(
            item_id_entry.get(), item_name_entry.get(), int(quantity_entry.get()), 'inventory', status_label
        )
    )
    add_button.pack()

# Function to handle the "Make a Sale" option
def make_sale():
    sale_window = tk.Toplevel(window)
    sale_window.title("Make a Sale")

    # Create GUI elements for making a sale
    item_id_label = tk.Label(sale_window, text="Item ID:")
    item_id_label.pack()
    item_id_entry = tk.Entry(sale_window)
    item_id_entry.pack()

    quantity_label = tk.Label(sale_window, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(sale_window)
    quantity_entry.pack()

    status_label = tk.Label(sale_window, text="")
    status_label.pack()

    sale_button = tk.Button(
        sale_window, text="Make a Sale",
        command=lambda: update_stock(
            item_id_entry.get(), '', int(quantity_entry.get()), 'sales', status_label
        )
    )
    sale_button.pack()

# Function to handle the "Make a Return" option
def make_return():
    return_window = tk.Toplevel(window)
    return_window.title("Make a Return")

    # Create GUI elements for making a return
    item_id_label = tk.Label(return_window, text="Item ID:")
    item_id_label.pack()
    item_id_entry = tk.Entry(return_window)
    item_id_entry.pack()

    quantity_label = tk.Label(return_window, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(return_window)
    quantity_entry.pack()

    status_label = tk.Label(return_window, text="")
    status_label.pack()

    return_button = tk.Button(
        return_window, text="Make a Return",
        command=lambda: update_stock(
            item_id_entry.get(), '', int(quantity_entry.get()), 'returns', status_label
        )
    )
    return_button.pack()

# Function to handle the "Exit" option
def on_exit():
    window.destroy()

# Create a menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create a menu for inventory actions
inventory_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Inventory", menu=inventory_menu)
inventory_menu.add_command(label="Add to Inventory", command=add_to_inventory)

# Create a menu for sales actions
sales_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Sales", menu=sales_menu)
sales_menu.add_command(label="Make a Sale", command=make_sale)

# Create a menu for returns actions
returns_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Returns", menu=returns_menu)
returns_menu.add_command(label="Make a Return", command=make_return)

# Create an exit option in the menu
menu_bar.add_command(label="Exit", command=on_exit)

# Status label for messages
status_label = tk.Label(window, text="")
status_label.pack()

# Start the tkinter event loop
window.mainloop()

# Close the database connection
mycursor.close()
mydb.close()
