from django.shortcuts import render,redirect
from .forms import MyAddress
from .models import BillingsAddress
from App_Cart.models import Order,Cart
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import requests
import socket
from django.contrib.auth.decorators import login_required
from django.urls  import reverse
from django.views.decorators.csrf import csrf_exempt


from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.


def userAddress(request):
	saved_address = BillingsAddress.objects.get_or_create(user=request.user)
	saved_address = saved_address[0]
	form = MyAddress(instance=saved_address)
	if  request.method == 'POST':
		form = MyAddress(request.POST,instance=saved_address)
		if form.is_valid():
			form.save()
			form = MyAddress(instance=saved_address)
			messages.success(request,"Billing Address saved sucessfully")


	order_qs = Order.objects.filter(user=request.user,ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total =order_qs[0].get_totals()

	return render(request,'App_Payment/Checkout.html',context={'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})


@login_required
def payment(request):
	saved_address = saved_address = BillingsAddress.objects.get_or_create(user=request.user)
	saved_address = saved_address[0]
	if not saved_address.is_fully_filled():
		messages.error(request,"Please fill the Billing address Properly")
		return redirect('App_Cart:view_cart')

	if not request.user.profile.is_fully_filled():
		messages.info(request,"Please complete your Profile details")
		return redirect('App_login:edit_profile')


	mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='kdtec5f9ec95a661f1', sslc_store_pass='kdtec5f9ec95a661f1@ssl')
	
	status_url = request.build_absolute_uri(reverse('App_payment:complete'))

	mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
	
	order_queries = Order.objects.filter(user=request.user,ordered=False)
	order_item = order_queries[0].orderitems.all()
	order_item_count = order_queries[0].orderitems.count()
	order_total = order_queries[0].get_totals()


	mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', 
	product_category='Mied',product_name=order_item, num_of_item=order_item_count, shipping_method='COD', product_profile='None')
	
	current_user = request.user

	mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, 
	address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode,
	country=current_user.profile.country, phone=current_user.profile.phone)

	mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address,
	city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

	response_data = mypayment.init_payment()
	return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request):
	if request.method == 'POST' or request.method=='post':
		payment_data = request.POST
		status = payment_data['status']
		

		if status == 'VALID':
			val_id = payment_data['val_id']
			bank_tran_id = payment_data['bank_tran_id']
			tran_id = payment_data['tran_id']
			messages.success(request,"your payment completed succesfull")
			return HttpResponseRedirect(reverse('App_payment:purchase',kwargs={'val_id':val_id,'tran_id':tran_id}))
		elif status == 'FAILED':
			messages.error(request,"your payment Failed please try again")
			
	return render(request,"App_Payment/complete.html")


@login_required
def purchase(request,val_id,tran_id):
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	order= order_qs[0]
	orderId = tran_id
	order.ordered= True
	order.orderId =orderId
	order.paymentId = val_id
	order.save()
	cart_items = Cart.objects.filter(user=request.user,purchased=False)
	for item in cart_items:
		item.purchased = True
		item.save()
	return HttpResponseRedirect(reverse('App_Shop:home'))

@login_required
def order_view(request):
	try:
		orders = Order.objects.filter(user=request.user,ordered=True)
		context = {'orders':orders}
	except:
		messages.warning(request,"you do not have active order")
		return redirect('App_Shop:home')
	return render(request,"App_Payment/order.html",context)		
