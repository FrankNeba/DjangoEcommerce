from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, User, Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import  UserForm, UserUpdate
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
from verify_email.email_handler import send_verification_email

# Create your views here.

def mail(message, subject, recipient):
    send_mail(
        subject=subject,
        message= message,
        recipient_list=[recipient],
        from_email= None,
        fail_silently=False
    )


#home view
def home(request):
    q = request.GET.get('q')
    p = request.GET.get('p')
    products = categories = []
    
    if q is None and p is not None and p is not '':
        categories = Category.objects.filter(name__contains=p)
        products = Product.objects.filter(category__name__contains = p)
    else:
        if q is None:
            q=''
        products = Product.objects.filter(name__contains = q)
        [categories.append(product.category) for product in products if product.category not in categories]

    categoryoptions = Category.objects.all()
    context = {'products': products, 'categories':categories, 'categoryoptions': categoryoptions}
    return render(request, 'shop/home.html', context)

#sign up view
def Signup(request):
    form = UserForm()
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.POST.get('username'))
        except:
            user = None
        if user is not None and user.is_active:
            messages.error(request, 'Username exists')
        else:
            try:
                user = User.objects.get(email = request.POST.get('email'))
            except:
                user = None
            if user is not None and user.is_active:    
                messages.error(request, 'Email exists') 
            elif request.POST.get('password1') != request.POST.get('password2'):
                messages.error(request,"Passwords don't match")
            else:
                if user is not None and user.is_active == False:
                    user.delete()
                form = UserForm(request.POST)
                form.email = request.POST.get('email')
                form.username = request.POST.get('username')
                form.password1 = request.POST.get('password1')
                form.password2 = request.POST.get('password2')
                
                if form.is_valid():
                    user = form.save(commit = False)
                    user.is_active = False
                    code = random.randint(1000, 9999)
                    user.code=code
                    user.save()
                    message = f'Hello {user.username}, \nYour Account activation code is {code}'
                    # try:
                    #     send_mail(
                    #     subject="Verify Ecommerce account",
                    #     message= message,
                    #     recipient_list=[user.email],
                    #     from_email= None,
                    #     fail_silently=False
                    # )
                    # except:
                    #     messages.error(request, 'Check your internet connection \nCheck if email exist')

                    return redirect('verify', pk=user.id)
                messages.error(request, "Password can easily be guessed. Use a mixture of letters and symbols for a strong password")
    return render(request, 'shop/signup.html', {'form':form})

def verifyemail(request, pk):
    user = User.objects.get(id = pk)
    email = ''
    for i in range(len(user.email)):
        if i < 4:
            email += user.email[i]
        else :
            email += '*'
    if request.method == 'POST':
        code = int(request.POST.get('code'))
        if code == user.code:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect ('home')
        messages.error(request, 'Code is invalid')
    return render(request, 'shop/verify.html', {'user':user, 'email':email})



#update user
@login_required(login_url='login')
def Update(request):
    form = UserUpdate(instance = request.user)
    if request.method == 'POST':
        form = UserUpdate(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        messages.error(request, "Inputs not valid")
    return render(request, 'shop/updateprofile.html', {'form':form})



#user profile view
@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    products = Product.objects.filter(seller = user)
    context = {"products": products}
    return render(request, 'shop/profile.html', context)


#login view
def Loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, "email or password not correct")
    return render(request, 'shop/login.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email = email)
            code = random.randint(11111, 99999)
            user.code = code
            user.save()
            message = f'Hello {user.username}, \nYour Password reset code is {code}'
            subject = 'ResetPassword'
            recipient = user.email
            try:
                mail(message,subject, recipient)
            except:
                messages.error(request, 'Message not sent. Check your internet conection')
            return redirect('passwordcode', pk=user.id)
        except:
            messages.error(request, f'Account with email {email} doesn\'t exist')
    return render(request, 'shop/forgotpassword.html')

def passwordcode(request, pk):
    user = User.objects.get(id = pk)
    email = ''
    for i in range(len(user.email)):
        if i < 4:
            email += user.email[i]
        else :
            email += '*'
    if request.method == 'POST':
        code = int(request.POST.get('code'))
        if code == user.code:
            return  redirect('resetpassword', pk=user.id)
        messages.error(request, 'Invalid code')
    return render(request, 'shop/passwordcode.html', {'user':user})

def resendpassword(request, pk):
    user = User.objects.get(id = pk)
    code = random.randint(11111, 99999)
    user.code = code
    user.save()
    message = f'Hello {user.username}, \nYour Password reset code is {code}'
    subject = 'ResetPassword'
    recipient = user.email
    try:
        mail(message,subject, recipient)
    except:
        messages.error(request, 'Message not sent. Check your internet conection')
    return redirect('passwordcode', pk=user.id)



def resetPassword(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id = pk)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(password1) < 8:
            messages.error(request, 'Password must be atleast 8 characters')
        elif password1 != password2:
            messages.error(request, 'Passwords don\'t  match')
        else:
            
            try: 
                password = int(password)
                messages.error(request, 'Password can easily be guessed')
            except:
                user.password = make_password(password1)
                user.save()
                # login(request, user)
                return redirect('login')
            
    return render(request, 'shop/resetpassword.html')

#logout view
def LogoutView(request):
    logout(request)
    return redirect('home')
    
#add product view
@login_required(login_url='login')
def addProduct(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get("name")
        seller = request.user
        price = int(request.POST.get('price'))
        description = request.POST.get('description')
        category = request.POST.get('category')
        otherCategory = request.POST.get('other')
        if category == 'other':
            newCategory = Category(name=otherCategory)
            newCategory.save()
            category = Category.objects.get(name = newCategory)
        else:
            category = Category.objects.get(id=int(category))
        
        product = Product(name = name, seller = seller, price = price, description = description, category = category, image = image)
        product.save()
        return redirect('home')
    
    context = {'categories': categories}
    return render(request, 'shop/addProduct.html', context)



#add product view
@login_required(login_url='login')
def editProduct(request,pk):
    product = Product.objects.get(id = pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get("name")
        seller = request.user
        price = int(request.POST.get('price'))
        description = request.POST.get('description')
        category = request.POST.get('category')
        category = Category.objects.get(id=int(category))
        image = request.FILES.get('image')
        product.name = name
        product.seller = seller
        product.price = price
        product.description = description
        product.image = image
        product.save()
        return redirect('home')
    
    context = {'categories': categories, 'product': product}
    return render(request, 'shop/addProduct.html', context)


def productDetails(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'shop/product.html', context)

#add category
@login_required(login_url='login')
def Categories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = Category(name = name)
        category.save()
        return redirect('home')
    return render(request, 'shop/category.html')

def image(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'shop/image.html', {'product':product}) 


#delete item
@login_required(login_url='login')
def delete(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    context = {"item": product}
    return render(request, 'shop/delete.html', context)


@login_required(login_url='login')
def addToCart(request, pk):
    product = Product.objects.get(id = pk)
    items = Cart.objects.all()
    for item in items:
        if item.product == product:
            messages.error(request,"Already added to cart")
            return redirect('product-details', pk=product.id)
    user = request.user
    item = Cart(product = product, user=user)
    item.save()
    messages.success(request, 'Added to cart succesfully')
    return redirect('product-details', pk=product.id)

@login_required(login_url='login')
def viewCart(request):
    cart = Cart.objects.filter(user = request.user)
    context = {'cart':cart}
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def removecart(request, pk):
    if request.method == 'POST':
        item = Cart.objects.get(id=pk)
        item.delete()
        return redirect('cart')

@login_required(login_url='login')
def order(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        price = amount * int(product.price)
        orderMessage = f"Hello {product.seller.username}, \nAn order has been made by {request.user.email}\nName: {request.user.username}\nProduct: {product.name}  \nQuantity: {amount}\nAddress: {request.user.address}\nPrice: {price}XAF"
        replyMessage = f"Hello {request.user.username}, \nYou have successfully made an order to  {product.seller.email}\nName: {product.seller.username}\nProduct: {product.name}  \nQuantity: {amount}\nPrice: {price}XAF"
        send_mail(
        subject="Order Made",
        message= orderMessage,
        recipient_list=[product.seller.email],
        from_email= None,
        fail_silently=False
        )
        send_mail(
        subject="Order Made",
        message= replyMessage,
        recipient_list=[request.user.email],
        from_email= None,
        fail_silently=False
        )
        return redirect("cart")
    context = {'product': product}
    return render(request, 'shop/order.html', context)


    
    





