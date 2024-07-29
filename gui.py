import tkinter as tk
from tkinter import messagebox
import sqlite3

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        self.root.geometry("800x600")

        # Create Frames
        self.create_product_frame()
        self.create_customer_frame()
        self.create_invoice_frame()

    def create_product_frame(self):
        frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        frame.place(x=20, y=20, width=350, height=200)

        tk.Label(frame, text="Product Management", font=("Arial", 15)).pack(side=tk.TOP, pady=10)

        tk.Label(frame, text="Product Name").place(x=20, y=60)
        self.product_name = tk.Entry(frame)
        self.product_name.place(x=150, y=60)

        tk.Label(frame, text="Product Price").place(x=20, y=100)
        self.product_price = tk.Entry(frame)
        self.product_price.place(x=150, y=100)

        tk.Button(frame, text="Add Product", command=self.add_product).place(x=150, y=140)

    def create_customer_frame(self):
        frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        frame.place(x=20, y=240, width=350, height=200)

        tk.Label(frame, text="Customer Management", font=("Arial", 15)).pack(side=tk.TOP, pady=10)

        tk.Label(frame, text="Customer Name").place(x=20, y=60)
        self.customer_name = tk.Entry(frame)
        self.customer_name.place(x=150, y=60)

        tk.Label(frame, text="Customer Phone").place(x=20, y=100)
        self.customer_phone = tk.Entry(frame)
        self.customer_phone.place(x=150, y=100)

        tk.Button(frame, text="Add Customer", command=self.add_customer).place(x=150, y=140)

    def create_invoice_frame(self):
        frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        frame.place(x=400, y=20, width=350, height=420)

        tk.Label(frame, text="Invoice Management", font=("Arial", 15)).pack(side=tk.TOP, pady=10)

        tk.Label(frame, text="Customer ID").place(x=20, y=60)
        self.invoice_customer_id = tk.Entry(frame)
        self.invoice_customer_id.place(x=150, y=60)

        tk.Label(frame, text="Product ID").place(x=20, y=100)
        self.invoice_product_id = tk.Entry(frame)
        self.invoice_product_id.place(x=150, y=100)

        tk.Label(frame, text="Quantity").place(x=20, y=140)
        self.invoice_quantity = tk.Entry(frame)
        self.invoice_quantity.place(x=150, y=140)

        tk.Button(frame, text="Add to Invoice", command=self.add_to_invoice).place(x=150, y=180)
        tk.Button(frame, text="Generate Invoice", command=self.generate_invoice).place(x=150, y=220)

        self.invoice_items = []

    def add_product(self):
        name = self.product_name.get()
        price = self.product_price.get()

        if not name or not price:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid price")
            return

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully")
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)

    def add_customer(self):
        name = self.customer_name.get()
        phone = self.customer_phone.get()

        if not name or not phone:
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Customer added successfully")
        self.customer_name.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)

    def add_to_invoice(self):
        customer_id = self.invoice_customer_id.get()
        product_id = self.invoice_product_id.get()
        quantity = self.invoice_quantity.get()

        if not customer_id or not product_id or not quantity:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()

        conn.close()

        if not customer:
            messagebox.showerror("Error", "Invalid customer ID")
            return

        if not product:
            messagebox.showerror("Error", "Invalid product ID")
            return

        self.invoice_items.append((customer_id, product_id, product[1], product[2], quantity))

        messagebox.showinfo("Success", "Item added to invoice")

    def generate_invoice(self):
        if not self.invoice_items:
            messagebox.showerror("Error", "No items in invoice")
            return

        invoice_text = "Invoice\n"
        invoice_text += "------------------------------\n"
        total_amount = 0

        for item in self.invoice_items:
            customer_id, product_id, product_name, product_price, quantity = item
            amount = product_price * quantity
            total_amount += amount
            invoice_text += f"{product_name} (x{quantity}): ${amount:.2f}\n"

        invoice_text += "------------------------------\n"
        invoice_text += f"Total: ${total_amount:.2f}\n"

        self.invoice_items = []

        # Show invoice in a new window
        invoice_window = tk.Toplevel(self.root)
        invoice_window.title("Invoice")
        invoice_window.geometry("300x400")
        tk.Label(invoice_window, text=invoice_text, justify=tk.LEFT).pack()

        # Save invoice as text file
        with open("invoice.txt", "w") as f:
            f.write(invoice_text)

        messagebox.showinfo("Success", "Invoice generated successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
