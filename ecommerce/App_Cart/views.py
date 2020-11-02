from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.auth.decorators import login_required

from .models import Order,Cart

from App_Shop.models import Product
from django.contrib import messages

# Create your views here.

@login_required
def add_to_cart(request,pk):
	item = get_object_or_404(Product, pk=pk)
	order_item = Cart.objects.get_or_create(user=request.user,item=item,purchased=False)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order= order_qs[0]
		if order.orderitems.filter(item=item).exists():
			order_item[0].quantity += 1
			order_item[0].save()
		else:
			order.orderitems.add(order_item[0])
			messages.success(request,"Item Added Successfully")
			return redirect('App_Shop:home')

	else:
		order = Order(user=request.user)
		order.save()
		order.orderitems.add(order_item[0])
		return redirect('App_Shop:home')


@login_required
def view_Cart(request):
	cart = Cart.objects.filter(user=request.user,purchased=False)
	orders = Order.objects.filter(user=request.user,ordered=False)

	if cart.exists() and orders.exists():
		order = orders[0]
		return render(request,'App_Cart/cart.html',context={'cart':cart,'order':order})
	else:

		messages.error(request,"You Dont have Any item in the Cart")


@login_required
def remove_from_cart(request,pk):
	item = get_object_or_404(Product,pk=pk)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.orderitems.filter(item=item).exists():
			order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
			order.orderitems.remove(order_item)
			order_item.delete()
			messages.warning(request,"This item is removed from cart")
			return redirect('App_Shop:home')
		else:
			messages.info(request,"this item is not in your cart")
	else:
		messages.info(request,"you don't have active order")
		return redirect('App_Shop:home')	


@login_required
def increase_cart(request,pk):
	item = get_object_or_404(Product,pk=pk)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.orderitems.filter(item=item).exists():	
			order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
			if order_item.quantity	>=1:
				order_item.quantity	+=1
				order_item.save()
				messages.success(request,f"{item.name} quantity has been updated")
				return redirect('App_Cart:view_cart')
			else:
				messages.error(request,	f"{item.name} is not in your product list")
				return redirect('App_Shop:home')
		else:
			messages.error(request,	"You don't have active orders")
			return redirect('App_Cart:home')


@login_required
def descrease_cart(request,pk):
	item = get_object_or_404(Product,pk=pk)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.orderitems.filter(item=item).exists():	
			order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
			if order_item.quantity	>1:
				order_item.quantity	-=1
				order_item.save()
				messages.success(request,f"{item.name} quantity has been updated")
				return redirect('App_Cart:view_cart')
			else:
				order.orderitems.remove(order_item)
				order_item.delete()
				messages.error(request,	f"{item.name} is Removed From in your product list")
				return redirect('App_Shop:home')
		else:
			messages.error(request,	"You don't have active orders")
			return redirect('App_Cart:home')
			
