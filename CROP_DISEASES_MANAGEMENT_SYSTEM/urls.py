"""
URL configuration for login project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from app.views import productdetails,shopdetails,productdetailsupdate

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.profiledata),
    path('login', views.login),
    path('signup', views.signup),
    path('home_main', views.home_main),
    path('service', views.service),
    path('feature', views.feature),
    path('about', views.about),
    path('soon', views.soon),

    path('profile', views.profile),

    
    path('addprofiledata', views.addprofiledata),
    path('profiledata', views.profiledata),
    path('logindata', views.logindata),
    path('logoutdata', views.logoutdata),
    path('forgot',views.forgot,name="forgot"),
    path('reset/<token>',views.reset,name='reset_password'),


    path('home_admin', views.home_admin),
    path('home_shop', views.home_shop),
    path('home_farmer', views.home_farmer),



#ADMIN
    path('req', views.req),
    path('allshop', views.allshop),
    path('requpdate', views.requpdate),
    path('reqdelete', views.reqdelete),
    path('pur', views.pur),


#SHOP
    path('addproduct', views.addproduct),
    path('addproductdata', views.addproductdata),
    path('viewproducts', views.viewproducts),
    path('product/<int:product_id>', productdetails, name='productdetails'),
    path('productup/<int:product_id>', productdetailsupdate, name='productdetailsupdate'),

    path('custreq', views.custreq),
    path('makedeliver', views.makedeliver),

#FARMER
    path('disease', views.disease),
    path('shop', views.shop),
    path('shopproduct/<int:product_id>', shopdetails, name='shopdetails'),
    path('pay', views.pay),
    path('success', views.success),

]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)