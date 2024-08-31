from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, User, Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import  UserForm, UserUpdate
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
#home view
def home(request):
    q = request.GET.get('q','')
    p = request.GET.get('p','')
    products = list(Product.objects.filter(Q(name__contains = q) ))
    categories = list(Category.objects.filter(Q(name__contains = p)))
    # if products.count() > 0 and categories.count() == 0:
        # categories = []
        # [categories.append(product.category) for product in products if product.category not in categories]
    for category in categories:
        countn = 0
        for product in products:
            if product.category == category:
                countn += 1
        if countn == 0:
            categories.remove(category)

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
        if user is not None:
            messages.error(request, 'Username exists')
        else:
            try:
                user = User.objects.get(email = request.POST.get('email'))
            except:
                user = None
            if user is not None:
                messages.error(request, 'Email exists') 
            elif request.POST.get('password1') != request.POST.get('password2'):
                messages.error(request,"Passwords don't match")
            else:
                form = UserForm(request.POST)
                if form.is_valid():
                    user = form.save(commit = False)
                    user.save()
                    login(request, user)
                    return redirect('home')
                messages.error(request, "Password can easily be guessed. Use a mixture of letters and symbols for a strong password")
            # email = request.POST.get('email')
            # username = request.POST.get('username')
            # password1 = request.POST.get('password1')
            # password2 = request.POST.get('password2')
            # if len(password1) > 4 and password1 == password2:
            #     user = User.objects.create_user(username = email, password= password2)
            #     login(request, user)
            #     return redirect('home')
            # else:
            #     messages.error(request, 'passwords dont match')
    return render(request, 'shop/signup.html', {'form':form})


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


#logout view
def LogoutView(request):
    logout(request)
    return redirect('home')
    
#add product view
@login_required(login_url='login')
def addProduct(request):
    categories = Category.objects.all()
    if request.method == 'POST':
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
        image = request.FILES.get('image')
        form = Product(name = name, seller = seller, price = price, description = description, category = category, image = image)
        form.save()
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

@login_required(login_url='login')
def mail(request):
    send_mail(
        subject="Hello",
        message= "Django Email testing",
        recipient_list=["frankneba92@gmail.com"],
        from_email= None,
        fail_silently=False
    )
    return redirect("cart")
    
    





