import tkinter as tk
from tkinter import messagebox
import ttkthemes as ttk
from ttkthemes import ThemedStyle
from tkinter import PhotoImage
from PIL import Image,ImageTk
import time

from Database import InventoryDatabase

class System:
    def __init__(self):
        self.window = tk.Tk()
        

        self.window.geometry("1368x800")
        self.window.title('Inventory Management System')
        self.style=ThemedStyle(self.window)
        self.style.set_theme("plastik")
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        self.db_manager=InventoryDatabase()
        self.operations = self.create_operations()
        
        self.inventory_data=self.get_inventory()
        self.product=None
        
        self.name_entry=self.create_name_entry()
        
        self.background_image=self.create_image_background()
        self.footer=self.create_footer()
        


		
        
        
    def  get_inventory(self):
        return self.db_manager.get_products()     
        
        
    def search_product(self,name):
            product=self.db_manager.get_product_by_name(name)
            if product:
                return product[0]
            else:
                messagebox.showerror("Error", f"product {name} not found")
                return None
            
    def create_name_entry(self):
        name_entry = tk.Entry(self.display_frame)
        name_entry.pack(expand=True, fill="both")

        def on_sell_click():
            self.clear_display_frame()
            name_label = tk.Label(self.display_frame, text="Name:", padx=16, pady=16, fg="white", bg="grey")
            name_label.pack(expand=True, fill="both")
            name_entry = tk.Entry(self.display_frame)
            name_entry.pack(expand=True, fill="both")
            

            submit_button = tk.Button(self.display_frame, text="Sell Product", command=lambda: self.sell_product(name_entry), borderwidth=1, font=("Helvetica", 10))
            submit_button.pack(expand=True, fill="both")

        def on_view_click():
            self.clear_display_frame()
            name_label = tk.Label(self.display_frame, text="Name:", padx=16, pady=16, fg="white", bg="grey")
            name_label.pack(expand=True, fill="both")
            name_entry = tk.Entry(self.display_frame)
            name_entry.pack(expand=True, fill="both")

            

            submit_button = tk.Button(self.display_frame, text="View Product", command=lambda: self.view_product(name_entry), borderwidth=1, font=("Helvetica", 10))
            submit_button.pack(expand=True, fill="both")

        def on_add_click():
            self.clear_display_frame()
            name_label = tk.Label(self.display_frame, text="Name:", padx=16, pady=16, fg="white", bg="grey")
            name_label.pack(expand=True, fill="both")
            name_entry = tk.Entry(self.display_frame)
            name_entry.pack(expand=True, fill="both")

            

            submit_button = tk.Button(self.display_frame, text="Add Product", command=lambda: self.add_product(name_entry), borderwidth=1, font=("Helvetica", 10))
            submit_button.pack(expand=True, fill="both")

        return name_entry, on_sell_click, on_view_click, on_add_click

    
    
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=300, bg="black")
        frame.pack(expand=True, fill="both")
        return frame	


    def create_product_display_labels(self):
        self.clear_display_frame()
        poduct_id,name, quantity, price = self.create_product()
        product_info=f"Name: {name}\nQuantity: {quantity}\nPrice: {price}"
        create_product_label=tk.Label(self.display_frame, text=product_info, anchor="center", bg="black", fg="white",padx=16,pady=16, font=("Times",20))
        create_product_label.pack(expand=True, fill="both")	
        return create_product_label
    def view_product_display_labels(self,product_id):
        self.clear_display_frame()
        product = self.db_manager.get_product(product_id)
        if product is not None:
            name, quantity, price=product
            
            
            product_info=f" Product_id: {product_id}\nName: {name}\nQuantity: {quantity}\nPrice: {price}"
        else:
            product_info="No product available"    
        view_product_label=tk.Label(self.display_frame, text=product_info, anchor="center", bg="black", fg="white",padx=16,pady=16, font=("Times",20))
        view_product_label.pack(expand=True, fill="both")	
        return view_product_label
        
    def sell_product_display_labels(self,name_entry):
        self.clear_display_frame()
        product = self.sell_product(name_entry)
        if product is not None:
            name, quantity, price=product
            
            
            product_info=f" Sold Product\nName: {name}\nQuantity: {quantity}\nPrice: {price}"
        else:
            product_info="No product sold or out of stock"
        sell_product_label=tk.Label(self.display_frame, text=product_info, anchor=tk.ALL, bg="green", fg="white",padx=16,pady=16, font=("Times",20))
        sell_product_label.pack(expand=True, fill="both")	
        return sell_product_label
        self.sell_product_display_labels()
    def add_product_display_labels(self,product_id):
        
        self.clear_display_frame()
        product=self.db_manager.get_product(product_id)
        
        if product is not None:
            name, quantity, price=product
        
            product_info=f"Name: {name}\nQuantity: {quantity}\nPrice: {price}"
        else:
            product_info="No product selected or already in inventory"
                
        add_product_label=tk.Label(self.display_frame, text=product_info, anchor="center", bg="black", fg="white",padx=16,pady=16, font=("Times",20))
        add_product_label.pack(expand=True, fill="both")	
        return add_product_label
        
    
    def show_inventory_display_labels(self):
        self.clear_display_frame()
        inventory_text=""
        products=self.get_inventory()
        
        if not products:
            inventory_text="No products in inventory"
            inventory_label = tk.Label(self.display_frame, text="No products in inventory", font=("Times", 20))
            inventory_label.pack(expand=True, fill="both")    
        else:
        
            inventory_text="Inventory:\n"
            for product in products:
                product_id,name,quantity,price=product
                inventory_text +=f" Product_id:{product_id},Name: {name}, Quantity: {quantity}, Price: {price}\n"
                
        inventory_label = tk.Label(self.display_frame, text=inventory_text, bg="black", fg="white", padx=16, pady=16, font=("Times", 20))
        inventory_label.pack(expand=True, fill="both")
        return inventory_label
    

    def clear_display_frame(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def show_inventory(self):
        inventory=self.get_inventory()
        if not inventory:
            messagebox.showinfo('Inventory', 'The inventory is empty')
        else:
            inventory_details = ""
            for product in inventory:
                product_id,name, quantity, price = product
                inventory_details += f'Product_id:{product_id},Name: {name}, Quantity: {quantity}, Price: {price}\n'
            messagebox.showinfo("Inventory details", inventory_details)
        self.show_inventory_display_labels()
        
         
        

    def on_sell_click(self):
        name_entry, on_sell_click, on_view_click, on_add_click = self.create_name_entry()
        on_sell_click()

    def on_view_click(self):
        name_entry, on_sell_click, on_view_click, on_add_click = self.create_name_entry()
        on_view_click()

    def on_add_click(self):
        name_entry, on_sell_click, on_view_click, on_add_click = self.create_name_entry()
        on_add_click()       

    def create_product(self):
        def on_create_click():
            
            name = name_entry.get()
            quantity = quantity_entry.get()
            price = price_entry.get()
            try:
                quantity = int(quantity)
                price = float(price)
                self.db_manager.create_product(name,quantity,price)
                self.clear_display_frame()
            except ValueError:
                messagebox.showerror('Error', 'Invalid input for quantity or price')

            messagebox.showinfo("Product Created", f"Name: {name}\nQuantity: {quantity}\nPrice: {price}")

        
        
        name_label = tk.Label(self.display_frame, text="Name:", padx=16, pady=16, fg="white", bg="grey")
        name_label.pack(expand=True, fill="both")
        name_entry = tk.Entry(self.display_frame)
        name_entry.pack(expand=True, fill="both")

        quantity_label = tk.Label(self.display_frame, text="Quantity:", padx=16, pady=16, fg="white", bg="grey")
        quantity_label.pack(expand=True, fill="both")
        quantity_entry = tk.Entry(self.display_frame)
        quantity_entry.pack(expand=True, fill="both")

        price_label = tk.Label(self.display_frame, text="Price:", padx=16, pady=16, fg="white", bg="grey")
        price_label.pack(expand=True, fill="both")
        price_entry = tk.Entry(self.display_frame)
        price_entry.pack(expand=True, fill="both")

        submit_button = tk.Button(self.display_frame, text="Create Product", command=on_create_click, borderwidth=1, font=("Helvetica", 10))
        submit_button.pack(expand=True, fill="both")
        return name_entry, quantity_entry, price_entry
        self.create_product_display_labels()

    def view_product(self,name_entry):
        
        name=name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a product name")
            return
        
        product_id=self.search_product(name)
        
        #product=self.db_manager.view_product(product_id)
        if product_id is not None:
            self.view_product_display_labels(product_id)
    

            
        else:
            messagebox.showerror("Error",'No product selected')
        self.create_name_entry()
        
        #self.clear_display_frame()
    
            
            
    def sell_product(self,name_entry):
        
        
        name=name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a product name")
            return
        
        product_id=self.search_product(name)
            
        if product_id is None:
            messagebox.showerror("Error", 'No product selected')
            return
        success = self.db_manager.sell_product(product_id)
        if success:
                messagebox.showinfo('Sale successful', f'You have sold 1 {success["name"]}')
                    
        else:
                messagebox.showwarning("Out of stock", 'product  is out of stock')
        
        self.create_name_entry()

    def add_product(self,name_entry):
        
        name=name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a product name")
            return
        existing_product_id=self.search_product(name)
        
        if existing_product_id is None:
            messagebox.showerror("Error", f"Product '{name}' not found")
            return
        else:
            product=self.db_manager.add_product(existing_product_id)
        
       
        
        product_added=self.view_product_display_labels(existing_product_id)
        if product_added:
            messagebox.showinfo('Product added')
        else:
            messagebox.showerror('Product not added, product not added to the inventory') 
        self.create_name_entry()
               
        

    def create_operations(self):
        create_product = tk.Button(self.buttons_frame, text='Create Product', bg="red", font=("verdana", 20),
                                   borderwidth=1, command=self.create_product)
        create_product.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        view_product = tk.Button(self.buttons_frame, text="View Product", borderwidth=1, bg="green",
                                 font=("verdana",20), command=self.on_view_click)
        view_product.grid(row=0, column=4, columnspan=3, sticky=tk.NSEW)
        sell = tk.Button(self.buttons_frame, text='Sell', bg="blue", font=("verdana", 20), borderwidth=1,
                         command=self.on_sell_click)
        sell.grid(row=0, column=8, columnspan=2, sticky=tk.NSEW)
        add_product = tk.Button(self.buttons_frame, text='Add Product', bg="grey", font=("verdana", 20),
                                borderwidth=1, command=self.on_add_click)
        add_product.grid(row=0, column=10, columnspan=2, sticky=tk.NSEW)
        show_inventory = tk.Button(self.buttons_frame, text='Show Inventory', fg="white", bg="black", font=("verdana", 20),
                                   borderwidth=1, command=self.show_inventory)
        show_inventory.grid(row=0, column=12, sticky=tk.NSEW)
        return create_product, view_product, sell, add_product, show_inventory
    def create_image_background(self):
        image_frame=tk.Frame(self.window)
        image_frame.pack(fill="both",expand=True)
        image_path="images\pexels-toni-cuenca-585752.jpg"
        pil_image=Image.open(image_path)
        
    
        img=ImageTk.PhotoImage(pil_image)
        
        image_label=tk.Label(image_frame,image=img)
        image_label.place(relwidth=1, relheight=1,relx=0.5,rely=0.5,anchor="center")
        
        
        return image_frame
    def create_footer(self):
        footer_frame=tk.Frame(self.window,bg="black")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        company_name='Gerald Inco'
       
        company_label=tk.Label(footer_frame,text=company_name,font=("Helvetica",20,"italic bold"),bg="black",fg="white",padx=10,pady=5)
        company_label.pack()
        return footer_frame
    
        
    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    sys = System()
    sys.run()
