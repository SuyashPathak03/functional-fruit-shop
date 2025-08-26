from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Fruit, OrderItem, Order
from .cart import Cart
from django.contrib.auth.decorators import login_required



# Home
def home_view(request):
    fruits = Fruit.objects.all()  # Fetch all fruits
    return render(request, 'shop/fruits.html', {'fruits': fruits})


# User Signup
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('home')  # Redirect to home page
    else:
        form = SignupForm()
    return render(request, "shop/signup.html", {"form": form})


# User Login
def login_view(request, ):
    next_url = request.GET.get("next")
    if not next_url:
        next_url = resolve_url("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})


# User Logout
def logout_view(request):
    logout(request)
    return redirect('home')


# Purchase
def buy_fruit(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)

    if fruit.stock > 0:
        fruit.stock -= 1  # Reduce stock by 1
        fruit.save()
        message = f"You bought {fruit.name}! Remaining stock: {fruit.stock}"
    else:
        message = f"Sorry, {fruit.name} is out of stock!"

    return render(request, 'shop/buy.html', {'message': message})


# Cart
def add_to_cart(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    cart = Cart(request)  # Using your Cart class
    cart.add(fruit)  # Add fruit to cart

    # Update cart count by summing quantities of all items in the cart
    cart_count = sum(item["quantity"] for item in cart.cart.values())

    # Store updated cart count in session
    request.session["cart_count"] = cart_count
    request.session.modified = True  # Ensure session is saved

    # Return JSON response for AJAX requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "message": f"{fruit.name} added to cart!",
            "cart_count": cart_count
        })

    return redirect("cart_detail")


def cart_count(request):
    cart = request.session.get("cart", {})
    total_items = sum(item["quantity"] for item in cart.values())  # ✅ Count all items
    return JsonResponse({"cart_count": total_items})


def remove_from_cart(request, fruit_id):
    cart = Cart(request)
    fruit = get_object_or_404(Fruit, id=fruit_id)
    cart.remove(fruit)
    return redirect("cart_detail")


def cart_detail(request):
    cart = request.session.get("cart", {})
    cart_count = sum(item["quantity"] for item in cart.values())  # Ensure cart count is correct

    # If cart is empty, ensure cart count is set to 0
    if not cart:
        cart_count = 0

    request.session["cart_count"] = cart_count  # Update the session cart count

    # Convert cart data into list for rendering
    cart_items = []
    total_price = 0

    for fruit_id, item in cart.items():
        try:
            price = float(item["price"])
            quantity = int(item["quantity"])
            total_price += price * quantity
            cart_items.append({
                "id": fruit_id,
                "name": item["name"],
                "price": price,
                "quantity": quantity,
                "total": price * quantity,
                "image": Fruit.image,
            })
        except (ValueError, TypeError) as e:
            print(f"Error processing cart item {fruit_id}: {e}")

    return render(request, "shop/cart_detail.html", {
        "cart": {"items": cart_items, "total": total_price, "count": cart_count}
    })



def update_cart(request, fruit_id):
    if request.method == "POST":
        cart = Cart(request)
        fruit = get_object_or_404(Fruit, id=fruit_id)
        quantity = int(request.POST.get("quantity", 1))

        print(f"Updating fruit {fruit.name} (ID: {fruit_id}) to quantity {quantity}")
        cart = Cart(request)
        fruit = Fruit.objects.get(id=fruit_id)
        cart.update(fruit, quantity, request=request)


    return redirect("cart_detail")


@login_required(login_url='login')
def checkout(request):
    return render(request, "shop/checkout.html")  # ✅ Ensure the correct path


def process_checkout(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        address = request.POST["address"]
        payment_method = request.POST["payment_method"]

        cart = Cart(request)
        if not cart.items:  # If the cart is empty, prevent checkout
            return redirect("cart_detail")

        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            address=address,
            payment_method=payment_method,
            total_price=cart.total  # Assuming 'total' is defined in Cart for total price
        )

        for item in cart.items:  # Iterates over items in the cart
            fruit = Fruit.objects.get(id=item["id"])  # Fetch the fruit from DB
            OrderItem.objects.create(
                order=order,
                fruit=fruit,
                price=item["price"],
                quantity=item["quantity"]
            )
            # Reduce stock when the order is placed
            fruit.stock -= item["quantity"]
            fruit.save()

        cart.clear()  # Empty the cart after purchase
        return redirect("order_success")

    return redirect("checkout")



def order_success(request):
    return render(request, "shop/order_success.html")
