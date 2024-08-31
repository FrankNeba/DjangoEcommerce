from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('add', views.addProduct, name='addproduct'),
    path('login', views.Loginview, name='login'),
    path('logout', views.LogoutView, name='logout'),
    path('signup', views.Signup, name='signup'),
    path('update', views.Update, name="updateProfile"),
    path('editproduct/<str:pk>', views.editProduct, name="editproduct"),
    path('product/<str:pk>', views.productDetails, name="product-details"),
    path('addcategory', views.Categories, name='addcategory'),
    path('image/<str:pk>', views.image, name='image'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('add_to_cart/<str:pk>', views.addToCart, name='addtocart'),
    path('cart', views.viewCart, name="cart"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('removeitem/<str:pk>', views.removecart, name='removecart'),
    path("sendmail", views.mail, name='sendmail'),
    path('order/<str:pk>', views.order, name='order')

    
]
