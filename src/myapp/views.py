from django.http import Http404
from django.shortcuts import get_list_or_404, redirect, render
from .models import *
from django.contrib.auth.models import User, auth
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import MyOrder  # Update with your actual model
# views.py

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from decimal import Decimal
import razorpay

def initiate_payment(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))  # Total order amount
        client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_KEY_SECRET"))
        payment_data = {
            'amount': int(amount * 100),  # Convert amount to paise (or cents) and cast to int
            'currency': 'INR',  # Change as per your currency
            'payment_capture': '1'
        }
        try:
            razorpay_order = client.order.create(data=payment_data)
            return JsonResponse(razorpay_order)  # Return Razorpay order data to the client
        except razorpay.errors.BadRequestError as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})

# Other views remain the same



def home_view(request, *args, ** kwargs):
    arts = Art.objects.all()
    tags = Tag.objects.values('tag').distinct()
    context = {
        'arts': arts,
        'tags': tags
    }
    return render(request, "index.html", context)

def cat(request, id, *args, **kwargs):
    arts=Tag.objects.filter(tag=id)
    return render(request, 'category.html', {'arts':arts})

def description_view(request, id, *args, **kwargs):
    art = Art.objects.get(id=id)
    context = {
        'art': art
    }
    return render(request, 'description.html', context)


def add(request, id, *args, **kwargs):
    # print(request.path())
    if (not request.user.is_authenticated):
        return redirect('../../../login/login')
    user_obj = User.objects.filter(username=request.user)
    art_obj = Art.objects.filter(id=id)
    check = MyCart.objects.filter(user=request.user,art_id=id)
    if len(check) != 0:
        print("Art Exits!!")
    else:
        obj = MyCart.objects.create(
            user=user_obj[0], art_id=art_obj[0], added_date=datetime.now())
        obj.save()
    return redirect('../../../')


def remove(request, id,*args, **kwargs):
    cart_obj = MyCart.objects.get(art_id= id)
    cart_obj.delete()

    return redirect('cart')

def cancel_order(request, id,*args, **kwargs):
    order = MyOrder.objects.get(art_id=id)
    order.delete()
    return redirect('order')

def cancel_order(request, id, *args, **kwargs):
    orders = MyOrder.objects.filter(art_id=id)

    for order in orders:
        order.delete()

    return redirect('order')
#    order = get_object_or_404(MyOrder, art_id=art_id)

    # You can implement any logic here, e.g., updating the order status or deleting the order
    # For simplicity, let's assume you have a boolean field 'canceled' in your MyOrder model
    #order.delete()  # Change this line to delete the order directly

   # return JsonResponse({'message': 'Order canceled successfully'})


def about_us_view(request, *args, **kwargs):
    # about us
    return render(request, "aboutus.html", {})


def cart_view(request, *args, **kwargs):
    user_obj = User.objects.get(username=request.user)
    cart_obj = MyCart.objects.filter(user=user_obj)
    img = list()
    for item in cart_obj:
        artObj = Art.objects.get(id=item.art_id.id)
        img.append(artObj)

    con = zip(cart_obj, img)
    context = {
        'con': con
    }

    return render(request, "cart.html", context)


def order(request,id, *args, **kwargs):
    user_obj = User.objects.get(username=request.user)
    print(id)
    art_obj = Art.objects.get(id = id)
    obj = MyOrder.objects.create(user = user_obj, art_id = art_obj)
    obj.save()
    cart_obj = MyCart.objects.filter(art_id = art_obj)
    cart_obj.delete()
    art_obj.instock = False
    art_obj.save()
    return redirect('cart')


from django.db.models import Sum

def order_view(request, *args, **kwargs):
    user_obj = User.objects.get(username=request.user)

    # Fetch orders and associated arts for the user
    order_obj = MyOrder.objects.filter(user=user_obj)
    img = list()
    total_price = 0  # Initialize total price

    for item in order_obj:
        artObj = Art.objects.get(id=item.art_id.id)
        img.append(artObj)

        # Add the price of each artwork to the total price
        total_price += artObj.price

    con = zip(order_obj, img)
    context = {
        'con': con,
        'total_price': total_price,  # Pass the total price to the template
    }

    return render(request, "order.html", context)


