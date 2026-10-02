import mysql.connector as db

con = db.connect(
    host="localhost",
    user="root",
    password="your_pass",
    database="Your_db"
)
cur = con.cursor()

def inventory_sql():
  cur.execute("select * from inventory")
  data = cur.fetchall()

  inv = {}
  for name ,qty,cp,sp in data:
    inv[name]={
        "qty":qty,
        "cp":cp,
        "sp":sp}
  return inv

inventory = inventory_sql()

owner_password = "raju123"



def users_sql():
    cur.execute("SELECT username FROM users")
    data = cur.fetchall()

    users = []
    for (username,) in data:
        users.append(username)

    return users


#Owner

def add_fruits(inv):
  name = input('enter fruit name to add : ').lower()
  if name in inv:
    print("Fruit already exits")
    return
  qty = input("Enter quantiy to add: ")
  if qty.isdigit() and int(qty)>0:
    qty = int(qty)
  else:
    print("enter valid number: ")
    return
  price = input("Enter cost price of Fruit to add: ")
  if price.isdigit() and int(price)>0:
    price = int(price)
  else:
    print("Enter valid number")
    return
  sell_price = input("Enter selling price: ")
  if sell_price.isdigit() and int(sell_price)>0:
    sell_price = int(sell_price)
  else:
    print("Enter valid price: ")
    return

  cur.execute(
    "INSERT INTO inventory (fruit, quantity, cost_price, selling_price) VALUES (%s,%s,%s,%s)",
    (name, qty, price, sell_price)
      )
  con.commit()


  inv[name]={"qty":qty,"cp":price,"sp":sell_price}
  print("Fruit added successful")



def view_inventory(inv):
  print("Your inventory:")
  print("Fruits\t\tQuantity\tcostprice\tsellingprice")
  for fruits,details in inv.items():
    print(f"{fruits}\t\t{details['qty']}\t\t{details['cp']}\t\t{details['sp']}")
def view(inv):
  print("fruits\t\t\tQuantity\t\tprice")
  for fruits,details in inv.items():
    print(f"{fruits}\t\t\t{details['qty']}\t\t{details['cp']}")
    



def remove_item(inv):
  view_inventory(inv)
  name = input("Enter Which item do you want to remove: ").lower()
  if name in inv:
    cur.execute(
    "delete from inventory where fruit=%s",
    (name,)
        )
    con.commit()
    inv.pop(name)
    print("Item removed successful")
    return
  else:
    print("Item not in Inventory")
    return




def update_inventory(inv):
  view_inventory(inv)

  fruit = input("Enter fruit name to update: ").lower()
  if fruit in inv:
    ch = input("Enter What do you want to update (Quantity/Cost price/selling price): ").lower()
    if ch=="quantity":
      user=input("enter new quantity: ")
      if user.isdigit():
        user = int(user)
        inv[fruit]["qty"]=user
        cur.execute(
        "UPDATE inventory SET quantity=%s WHERE fruit=%s",
        (user, fruit)
                  )
        con.commit()


        print("quantity updated")
      else:
        print("enter valid quantity")
        return
    elif ch=="cost price":
      user = input("enter new cost price: ")
      if user.isdigit() and int(user)>0:
        user = int(user)
        inv[fruit]["cp"]=user
        cur.execute(
            "update inventory set cost_price=%s where fruit=%s",
            (user,fruit)
        )
        con.commit()
        print("update successful")
        return
      else:
        print("Enter valid price")
        return
    elif ch=="selling price":
      user = input("enter new selling price: ")
      if user.isdigit() and int(user)>0:
        user = int(user)
        inv[fruit]["sp"]=user
        cur.execute(
            "update inventory set selling_price=%s where fruit=%s",
            (user,fruit)
        )
        con.commit()
        print("selling price update successful")
        return
      else:
        print("print enter valid price")
        return
    else:
      print("invalid option")
      return

def cart(inv,cart):
  cart_item = input("Enter fruit to add in cart: ").lower()
  if cart_item not in inv:
    print("Item not FOund")
    return
  qty = input("enter Quantity: ")
  if not qty.isdigit() or int(qty)<=0:
    print("enter valid quantity")
    return
  qty = int(qty)
  if qty > inv[cart_item]["qty"]:
    print("out of Stock")
    return
  inv[cart_item]["qty"]-=qty
  cur.execute(
    "UPDATE inventory SET quantity=%s WHERE fruit=%s",
    (inv[cart_item]["qty"], cart_item)
    )
  con.commit()

  if cart_item in cart:
    cart[cart_item]["qty"]+=qty
  else:
    cart[cart_item]={"qty":qty,
    "price":inv[cart_item]["sp"]}

  print(cart_item,"---",qty,"----",inv[cart_item]["sp"])
  print("added to Cart successfull")



def profit():
  cur.execute("select fruit,quantity,cost_price,selling_price from inventory")
  data = cur.fetchall()
  total=0
  print("Fruits\tprofit")
  for fruit,qty,cp,sp in data:
    profit_items= sp-cp
    fruit_profit=qty*profit_items
    total = total+fruit_profit
    print(f"{fruit}\t{fruit_profit}")
  print("TOTAL PROFIT:",total)
#USER COde
def add_user(username):
    users = users_sql()
    if username in users:
        return

    cur.execute(
        "insert into users (username) values(%s)",
        (username,)
    )
    con.commit()


def view_cart(cart):
  print("items\tQuantity\tPrice")
  for i,j in cart.items():

    print(f"{i}\t{j['qty']}\t\t{j['price']}")



def remove_cart(inv,cart):
  view_cart(cart)
  fruit = input("Enter what do you want to remove: ").lower()
  if fruit in cart:
    inv[fruit]["qty"]+=cart[fruit]["qty"]
    cur.execute(
    "UPDATE inventory SET quantity=%s WHERE fruit=%s",
    (inv[fruit]["qty"], fruit)  )

    con.commit()

    cart.pop(fruit)
    print(fruit,"removed successfully")
  else:
    print("Item not Found")



def modify_cart(inv,cart):
  view_cart(cart)
  modify_fruit = input("Enter Fruit name to modify: ").lower()
  if modify_fruit in cart:
    new_qty = input("Enter quantity to modify : ")
    if not new_qty.isdigit() or int(new_qty)<=1:
      print("please Enter valid Quantity")
      return
    new_qty = int(new_qty)
    old_qty = cart[modify_fruit]["qty"]
    diff = new_qty-old_qty
    if diff > 0:

      if diff > inv[modify_fruit]["qty"]:
       print("Out of Stock")
       return
      else:
        inv[modify_fruit]["qty"]-=diff
    elif diff<0:
      inv[modify_fruit]["qty"]+=old_qty-new_qty

    cart[modify_fruit]["qty"] = new_qty
    cur.execute(
    "UPDATE inventory SET quantity=%s WHERE fruit=%s",
    (inv[modify_fruit]["qty"], modify_fruit)
      )
    con.commit()

    print("cart updated successfully")





def billing(inv,cart):
  total = 0
  print('*'*10,"bill",'*'*10)
  print("Items\tQuantity\tPrice")
  for items,details in cart.items():
    amount = details["qty"]*details["price"]
    total +=amount
    print(f"{items}\t{details['qty']}\t\t{details['price']}")
  print('-'*20)
  print("please pay",total)
  print("Thank you For Shopping")







while True:
  print("Welcome to Fruits Shop")
  user = input("Select Role OWNER/USER: ").lower()
  if user=='owner':
    password = input("Enter password: ")
    if password!= owner_password:
      print("wrong password")
      continue
    print("Access granted")
    print("1.Add Items to Inventory")
    print("2.remove Items")
    print("3.Update Items")
    print("4.View Inverntory")
    print("5.View users")
    print("6.profit")
    print("7.Exit")
    owner_in = input("Enter your option: ")
    if not owner_in.isdigit():
      print("please choose valid option")
      continue
    owner_in = int(owner_in)
    if owner_in==1:
      add_fruits(inventory)
    elif owner_in==2:
      remove_item(inventory)
    elif owner_in==3:
      update_inventory(inventory)
    elif owner_in==4:
      view_inventory(inventory)
    elif owner_in==5:
       users = users_sql()
       print("Users are:")
       for u in users:
        print(u)
    elif owner_in==6:
      profit()
    elif owner_in==7:
      print("Exiting")
      break
    else:
      print("Invalid Selection")

  elif user=="user":
    user_name = input("Enter Your name: ").lower()
    if not user_name.isdigit():
      add_user(user_name)
      user_cart = {}
    else:
      print("Number not allowed")
      continue
    while True:

      print('1.ADD cart')
      print('2.Remove Cart')
      print('3.Modify Cart')
      print('4.view Cart')
      print('5.Billing')
      print('6.Exit')
      user_in = input("choose one option: ")
      if not user_in.isdigit():
        print("please choose valid option")
        continue
      user_in = int(user_in)
      if user_in==1:
        view(inventory)

        cart(inventory,user_cart)

      elif user_in==2:
        remove_cart(inventory,user_cart)
      elif user_in==3:
        modify_cart(inventory,user_cart)

      elif user_in==4:
        view_cart(user_cart)
      elif user_in==5:
        billing(inventory,user_cart)
      elif user_in==6:
        print("Exiting")
        break
      else:
        print("Invalid Selection")


    else:
      print("Invalid seletion")

cur.close()
con.close()











