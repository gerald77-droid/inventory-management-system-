import sqlite3

class InventoryDatabase:
    def  __init__(self, db_file="inventory.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                quantity INTEGER,
                price REAL
            )
        ''')
        self.conn.commit()
    def create_product(self, name, quantity, price):
        self.conn.execute('''INSERT INTO products (name, quantity, price)
                        VALUES (?, ?, ?)''', (name, quantity, price))
        self.conn.commit()

    
    
    
    
    def add_product(self,product_id):
        existing_product=self.get_product(product_id)
        
        if existing_product:
            _, existing_quantity, _ =existing_product 
            new_quantity=existing_quantity + 1
            self.conn.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))

        else:
            return None
        self.conn.commit()

    def get_products(self):
        cursor = self.conn.execute('''SELECT * FROM products''')
        return cursor.fetchall()
    
    def get_product_by_name(self, name):
        cursor = self.conn.execute("SELECT id FROM products WHERE name = ?", (name,))
        product = cursor.fetchone()
        if product:
            return product
        else:
            return None



    def get_product(self, product_id):
        cursor = self.conn.execute("SELECT name, quantity, price FROM products WHERE id = ?", (product_id,))
        product_data = cursor.fetchone()
        if product_data:
            return product_data
        else:
            return None 

    def sell_product(self, product_id):
        product_details = self.get_product(product_id)
        if product_details is None:
            return None
        name, quantity, price = product_details
        if quantity <= 0:
            return None
        new_quantity=quantity-1
        self.conn.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
        self.conn.commit()
        return {'product_id':product_id,'name': name, 'quantity': quantity - 1, 'price': price}
    def view_products(self):
        cursor=self.conn.execute('''SELECT * FROM products''')
        return cursor.fetchall()
    
    def view_product(self,product_id):
        product_data=self.get_product(product_id)
        if product_data:
            product_id,name,quantity,price=product_data
            return {'product_id':product_id,'name':name,'quantity':quantity,'price':price}
        else:
            return None