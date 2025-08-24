# from .models import Fruit
# from .db_utils import get_stock_for_fruit
#
#
# class Cart:
#     def __init__(self, request):
#         """Initialize the cart using the session"""
#         self.session = request.session
#         cart = self.session.get("cart")
#         if not cart:
#             cart = self.session["cart"] = {}  # Create an empty cart
#         self.cart = cart
#
#     def add(self, fruit, quantity=1):
#         """Add fruit to cart (or update quantity)"""
#         fruit_id = str(fruit.id)
#
#         if fruit_id in self.cart:
#             self.cart[fruit_id]["quantity"] += quantity
#         else:
#             self.cart[fruit_id] = {
#                 "name": fruit.name,
#                 "price": str(fruit.price),  # Convert to string for session storage
#                 "quantity": quantity,
#                 "image": fruit.image,
#             }
#
#         self.save()
#
#     def remove(self, fruit):
#         """Remove fruit from cart"""
#         fruit_id = str(fruit.id)
#         if fruit_id in self.cart:
#             del self.cart[fruit_id]
#             self.save()
#
#     def save(self):
#         """Save cart data in session"""
#         self.session.modified = True
#
#     def get_items(self):
#         """Get all cart items"""
#         return self.cart.values()
#
#     # def update(self, fruit, quantity):
#     #     """ Update item quantity in the cart """
#     #     fruit_id = str(fruit.id)
#     #     if fruit_id in self.cart:
#     #         if quantity > 0:
#     #             self.cart[fruit_id]["quantity"] = quantity
#     #         else:
#     #             del self.cart[fruit_id]  #  Remove item if quantity is 0
#     #         self.session["cart"] = self.cart
#     #         self.session.modified = True
#     #     else:
#     #         print("Error: Fruit not found in cart")  # ✅ Debugging message
#
#     def update(self, fruit, quantity):
#         """Update item quantity in the cart"""
#         fruit_id = str(fruit.id)
#
#         #  get stock from online DB
#         available_stock = get_stock_for_fruit(fruit.name)
#
#         if fruit_id in self.cart:
#             if quantity > available_stock:
#                 print(f"Only {available_stock} {fruit.name} left in stock!")
#                 return
#             elif quantity > 0:
#                 self.cart[fruit_id]["quantity"] = quantity
#             else:
#                 del self.cart[fruit_id]  # remove item if quantity is 0
#
#             self.session["cart"] = self.cart
#             self.session.modified = True
#         else:
#             print("Error: Fruit not found in cart")
#
#     @property
#     def items(self):
#         """Returns a list of cart items."""
#         cart_items = []
#         for fruit_id, item in self.cart.items():
#             fruit = Fruit.objects.get(id=fruit_id)  # Ensure this is optimized if needed
#             cart_items.append({
#                 "id": fruit_id,
#                 "name": item["name"],
#                 "price": item["price"],
#                 "quantity": item["quantity"]
#             })
#         return cart_items
#
#     @property
#     def total(self):
#         total_price = 0
#         for item in self.cart.values():
#             total_price += float(item["price"]) * int(item["quantity"])
#         return total_price
#
#     def clear(self):
#         """Empty the cart"""
#         self.session["cart"] = {}
#         self.save()
#
#     def __len__(self):
#         """Return total quantity of items in the cart"""
#         return sum(item["quantity"] for item in self.cart.values())  # Fix len(cart)
#

# -----------------------------------------------------2---------------------------------------------------------------

# from .models import Fruit
#
#
# class Cart:
#     def __init__(self, request):
#         """Initialize the cart using the session"""
#         self.session = request.session
#         cart = self.session.get("cart")
#         if not cart:
#             cart = self.session["cart"] = {}  # Create an empty cart
#         self.cart = cart
#
#     def add(self, fruit, quantity=1):
#         """Add fruit to cart (or update quantity)"""
#         fruit_id = str(fruit.id)
#         available_stock = fruit.stock  # get stock directly from ORM
#
#         if quantity > available_stock:
#             print(f"Cannot add {quantity} {fruit.name}. Only {available_stock} in stock!")
#             return
#
#         if fruit_id in self.cart:
#             new_quantity = self.cart[fruit_id]["quantity"] + quantity
#             if new_quantity > available_stock:
#                 print(f"Cannot add {quantity} {fruit.name}. Only {available_stock} in stock!")
#                 return
#             self.cart[fruit_id]["quantity"] = new_quantity
#         else:
#             self.cart[fruit_id] = {
#                 "name": fruit.name,
#                 "price": str(fruit.price),
#                 "quantity": quantity,
#                 "image": fruit.image,
#             }
#
#         self.save()
#
#     def remove(self, fruit):
#         """Remove fruit from cart"""
#         fruit_id = str(fruit.id)
#         if fruit_id in self.cart:
#             del self.cart[fruit_id]
#             self.save()
#
#     def update(self, fruit, quantity):
#         """Update item quantity in the cart"""
#         fruit_id = str(fruit.id)
#         available_stock = fruit.stock  # stock from ORM
#
#         if fruit_id in self.cart:
#             if quantity > available_stock:
#                 print(f"Only {available_stock} {fruit.name} left in stock!")
#                 return
#             elif quantity > 0:
#                 self.cart[fruit_id]["quantity"] = quantity
#             else:
#                 del self.cart[fruit_id]  # remove item if quantity is 0
#
#             self.session["cart"] = self.cart
#             self.session.modified = True
#         else:
#             print("Fruit not found in cart")
#
#     def save(self):
#         """Save cart data in session"""
#         self.session.modified = True
#
#     @property
#     def items(self):
#         """Returns a list of cart items with a single DB query."""
#         cart_items = []
#         fruit_ids = self.cart.keys()  # get all fruit IDs in the cart
#         fruits = Fruit.objects.filter(id__in=fruit_ids)  # single query for all fruits
#
#         # Create a mapping from id to fruit object for easy access
#         fruit_map = {str(fruit.id): fruit for fruit in fruits}
#
#         for fruit_id, item in self.cart.items():
#             fruit = fruit_map.get(fruit_id)
#             if not fruit:
#                 continue  # skip if fruit was deleted from DB
#             cart_items.append({
#                 "id": fruit_id,
#                 "name": item["name"],
#                 "price": item["price"],
#                 "quantity": item["quantity"]
#             })
#
#         return cart_items
#
#     @property
#     def total(self):
#         total_price = 0
#         for item in self.cart.values():
#             total_price += float(item["price"]) * int(item["quantity"])
#         return total_price
#
#     def clear(self):
#         """Empty the cart"""
#         self.session["cart"] = {}
#         self.save()
#
#     def __len__(self):
#         """Return total quantity of items in the cart"""
#         return sum(item["quantity"] for item in self.cart.values())


# ----------------------------------------------3--------------------------------------------------------------
from .models import Fruit
from django.contrib import messages


class Cart:
    def __init__(self, request):
        """Initialize the cart using the session"""
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}  # Create an empty cart
        self.cart = cart

    def add(self, fruit, quantity=1):
        """Add fruit to cart (or update quantity)"""
        fruit_id = str(fruit.id)
        available_stock = fruit.stock  # stock from ORM

        if quantity > available_stock:
            print(f"Cannot add {quantity} {fruit.name}. Only {available_stock} in stock!")
            return

        if fruit_id in self.cart:
            new_quantity = self.cart[fruit_id]["quantity"] + quantity
            if new_quantity > available_stock:
                print(f"Cannot add {quantity} {fruit.name}. Only {available_stock} in stock!")
                return
            self.cart[fruit_id]["quantity"] = new_quantity
        else:
            self.cart[fruit_id] = {
                "name": fruit.name,
                "price": str(fruit.price),
                "quantity": quantity,
                "image": fruit.image,
            }

        self.save()



    def update(self, fruit, quantity, request=None):
        """Update item quantity in the cart"""
        fruit_id = str(fruit.id)
        available_stock = fruit.stock  # stock from ORM

        if fruit_id in self.cart:
            if quantity > available_stock:
                if request:
                    messages.error(request, f"Only {available_stock} {fruit.name} left in stock!")
                return
            elif quantity > 0:
                self.cart[fruit_id]["quantity"] = quantity
            else:
                del self.cart[fruit_id]  # remove item if quantity is 0

            self.session["cart"] = self.cart
            self.session.modified = True
        else:
            if request:
                messages.error(request, "Fruit not found in cart")

    def remove(self, fruit):
        """Remove fruit from cart"""
        fruit_id = str(fruit.id)
        if fruit_id in self.cart:
            del self.cart[fruit_id]
            self.save()

    def save(self):
        """Save cart data in session"""
        self.session.modified = True

    @property
    def items(self):
        """Returns a list of cart items with a single DB query"""
        cart_items = []
        fruit_ids = self.cart.keys()
        fruits = Fruit.objects.filter(id__in=fruit_ids)
        fruit_map = {str(fruit.id): fruit for fruit in fruits}

        for fruit_id, item in self.cart.items():
            fruit = fruit_map.get(fruit_id)
            if not fruit:
                continue  # skip if fruit was deleted from DB
            cart_items.append({
                "id": fruit_id,
                "name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                'image': fruit.image
            })

        return cart_items

    @property
    def total(self):
        total_price = 0
        for item in self.cart.values():
            total_price += float(item["price"]) * int(item["quantity"])
        return total_price

    def clear(self):
        """Empty the cart"""
        self.session["cart"] = {}
        self.save()

    def __len__(self):
        """Return total quantity of items in the cart"""
        return sum(item["quantity"] for item in self.cart.values())
