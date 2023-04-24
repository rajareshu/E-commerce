# from unicodedata import category
# from re import A
from django.http import JsonResponse
from django.shortcuts import render,redirect
from . models import Customer,Product,Cart,OrderPlaced
from django.views import View
from . form import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        mobiles=Product.objects.filter(category='M')
        bottomwears=Product.objects.filter(category='BW')
        laptops=Product.objects.filter(category='L')
        return render(request,'app/home.html',{'topwears':topwears,'mobiles':mobiles,'bottomwears':bottomwears,'laptops':laptops})



# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product})
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount+shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')
@login_required
def Plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)



@login_required
def Minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            totalamount=amount+shipping_amount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


@login_required
def Remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            
        data={

            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()

            messages.success(request,'Congratulation !! Profile Updated Successfully !!')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})



@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data == 'Sumsung' or data == 'iphone':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=20000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

    
def laptop(request,data=None):
    if data == None:
        laptops=Product.objects.filter(category='L')
    elif data == 'Asus' or data == 'Hp':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptops=Product.objects.filter(category='L').filter(discounted_price__lt=40000)
    elif data=='above':
        laptops=Product.objects.filter(category='L').filter(discounted_price__gt=40000)
    return render(request, 'app/laptop.html',{'laptops':laptops})




def top(request,data=None):
    if data == None:
        tops=Product.objects.filter(category='TW')
    elif data == 'zara' or data == 'Adidas':
        tops=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        tops=Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data=='above':
        tops=Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/top.html',{'tops':tops})




def bottom(request,data=None):
    if data == None:
        bottom=Product.objects.filter(category='BW')
    elif data == 'Lee' or data == 'Calvin':
        bottom=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottom=Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data=='above':
        bottom=Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottom.html',{'bottom':bottom})





# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! Registration Successfull')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})
        
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_item=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_item})


@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        
    return redirect('orders')
    
