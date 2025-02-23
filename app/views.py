from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

from django.db import transaction,models
from django.db.models import Max

# Create your views here.
cities = ["Select a District", 
    "Adimaly", "Adoor", "Agathy", "Alappuzha", "Alathur", "Alleppey", "Alwaye", "Amini", 
    "Androth", "Attingal", "Badagara", "Bitra", "Calicut", "Cannanore", "Chetlet", "Ernakulam", 
    "Idukki", "Irinjalakuda", "Kadamath", "Kalpeni", "Kalpetta", "Kanhangad", "Kanjirapally", 
    "Kannur", "Karungapally", "Kasargode", "Kavarathy", "Kiltan", "Kochi", "Koduvayur", "Kollam", 
    "Kottayam", "Kovalam", "Kozhikode", "Kunnamkulam", "Malappuram", "Mananthodi", "Manjeri", 
    "Mannarghat", "Mavelikkara", "Minicoy", "Munnar", "Muvattupuzha", "Nedumandad", "Nedumgandam", 
    "Nilambur", "Palai", "Palakkad", "Palghat", "Pathaanamthitta", "Pathanamthitta", "Payyanur", 
    "Peermedu", "Perinthalmanna", "Perumbavoor", "Punalur", "Quilon", "Ranni", "Shertallai", "Shoranur", 
    "Taliparamba", "Tellicherry", "Thiruvananthapuram", "Thodupuzha", "Thrissur", "Tirur", "Tiruvalla", 
    "Trichur", "Trivandrum", "Uppala", "Vadakkanchery", "Vikom", "Wayanad"
]

#MAIN FOLDER

def home_main(request):
    return render(request,'MAIN/home.html')
def login(request):
    return render(request,'MAIN/login.html')
def signup(request):
    return render(request,'MAIN/signup.html', {'cities': cities} )
def service(request):
    return render(request,'MAIN/service.html')
def feature(request):
    return render(request,'MAIN/feature.html')
def about(request):
    return render(request,'MAIN/about.html')
def soon(request):
    return render(request,'MAIN/soon.html')

def profile(request):
    if 'fid' in request.session:
        a=request.session['fid']
        data=order_db.objects.filter(paymentstatus=1,customermail=a)
        data1 = registration_db.objects.get(email=a)
        return render(request,'FARMER/profile.html',{'pro':data1,'r':data})
    elif 'sid' in request.session:
        a=request.session['sid']
        data1 = registration_db.objects.get(email=a)
        return render(request,'SHOP/profile.html',{'pro':data1})
    else:
        a=request.session['aid']
        data1 = registration_db.objects.get(email=a)
        return render(request,'ADMIN/profile.html',{'pro':data1})


def addprofiledata(request):
    if request.method == 'POST':
        a = request.POST['idno']
        b = request.POST['name']
        c = request.POST['address']
        d = request.POST['city']
        e = request.POST['userid']
        f = request.POST['password0']
        g = request.POST['password1']
        p = request.FILES['pic']
        q = request.POST.get('dropdown')
        r = request.POST.get('email')
        try:
            data = login_db.objects.get(email=r)
            msg = 'THE EMAIL IS ALREADY EXIST'
            return render(request,'MAIN/signup.html',{'msg':msg,'cities': cities})
        except Exception:
            try:
                data = login_db.objects.get(userid=e)
                msg = 'THE USER NAME IS ALREADY EXIST'
                return render(request,'MAIN/signup.html',{'msg':msg,'cities': cities})
            except Exception:
                try:
                    data = registration_db.objects.get(idno=a)
                    msg = 'THE ID NUMBER IS ALREADY EXIST'
                    return render(request,'MAIN/signup.html',{'msg':msg,'cities': cities})
                except Exception:
                    if f!=g:
                        msg = 'THE PASSWORD MUST BE MATCH'
                        return render(request,'MAIN/signup.html',{'msg':msg,'cities': cities})
                    else:
                        data0 = registration_db.objects.create(idno=a,name=b,address=c,city=d,userid=e,profile=p,email=r,status=q,action=q)
                        data1 = login_db.objects.create(password=f,userid=e,status=q,email=r,action=q)
                        data0.save()
                        data1.save()
                        msg = 'THE REGISTRATION IS COMPLETE'
                        return render(request,'MAIN/signup.html',{'msg':msg})
          

def logindata(request):
    if request.method == 'POST':
        a = request.POST['email']
        b = request.POST['pass']
        try:
            data = login_db.objects.get(email=a)
            if data.action==1:
                if data.password==b:
                    if data.status==1:
                        request.session['fid']=a
                        return redirect(profiledata)
                    elif data.status==2:
                        request.session['sid']=a
                        return redirect(profiledata)
                    else:
                        request.session['aid']=a
                        return redirect(profiledata)
                else:
                    msg = 'THE EMAIL/PASSWORD IS INCORRECT'
                    return render(request,'MAIN/login.html',{'msg':msg})
            else:
                msg = 'THE ADMIN NOT ACCEPTED YOUR REGISTRATION'
                return render(request,'MAIN/login.html',{'msg':msg})
        except Exception:
                msg = 'THE EMAIL/PASSWORD IS INCORRECT'
                return render(request,'MAIN/login.html',{'msg':msg})


def profiledata(request):
    if 'fid' in request.session:
        a=request.session['fid']
        data1 = login_db.objects.get(email=a)
        return render(request,'FARMER/home.html',{'pro':data1})
    elif 'sid' in request.session:
        a=request.session['sid']
        data1 = registration_db.objects.get(email=a)
        return render(request,'SHOP/home.html',{'pro':data1})
    elif 'aid' in request.session:
        a=request.session['aid']
        data1 = login_db.objects.get(email=a)
        return render(request,'ADMIN/home.html',{'pro':data1})
    else:
        return render(request,'MAIN/home.html')
                

def logoutdata(request):
    if 'fid' in request.session:
        request.session.flush()
        return render(request,'MAIN/home.html')
    elif 'sid' in request.session:
        request.session.flush()
        return render(request,'MAIN/home.html')
    else:
        request.session.flush()
        return render(request,'MAIN/home.html')
    

from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .models import login_db, PasswordReset  # Adjust the import based on your app structure

def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            u = login_db.objects.get(email=email)
        except login_db.DoesNotExist:
            messages.error(request, "This email is not registered.")
            return redirect('forgot')  # Use the name of the URL pattern for better practice

        # Generate and save a unique token
        token = get_random_string(length=4)  # Use a longer token for security
        PasswordReset.objects.create(user=u, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            messages.success(request, "Password reset email sent.")
        except Exception as e:
            messages.error(request, "Failed to send email. Please try again later.")
            return redirect('forgot')

    return render(request, 'MAIN/forgot.html')

def reset(request, token):
    try:
        # Verify token and reset the password
        password_reset = PasswordReset.objects.get(token=token)
        login = password_reset.user  # Get the user object directly

        if request.method == 'POST':
            new_password = request.POST.get('newpassword')
            repeat_password = request.POST.get('cpassword')
            if new_password == repeat_password:
                login_db.objects.filter(email=login.email).update(password=new_password)                
                PasswordReset.objects.filter(user=login).delete()  # Clean up the token
                messages.success(request, "Your password has been reset successfully.")
                return redirect('forgot')  # Redirect to login page after successful reset
            else:
                messages.error(request, "Passwords do not match.")
        
        return render(request, 'MAIN/reset.html', {'token': token})
    except PasswordReset.DoesNotExist:
        messages.error(request, "Invalid or expired token.")
        return redirect('forgot')



#ADMIN FOLDER

def home_admin(request):
    return render(request,'ADMIN/home.html')
def req(request):
    data1 = registration_db.objects.filter(status=2,action=2)
    return render(request,'ADMIN/request.html',{'r':data1})
def allshop(request):
    data1 = registration_db.objects.filter(status=2,action=1)
    return render(request,'ADMIN/shop.html',{'r':data1})
def requpdate(request):
    if request.method == 'POST':
        email = request.POST['r1']  

     
        login_data = login_db.objects.get(email=email)
        login_data.action = 1
        login_data.save()  

        registration_data = registration_db.objects.get(email=email)
        registration_data.action = 1
        registration_data.save()  


        msg = registration_db.objects.filter(status=2, action=2)
        return render(request, 'ADMIN/request.html', {'r': msg})
def reqdelete(request):
    if request.method == 'POST':
        email = request.POST['r2']  


        login_data = login_db.objects.get(email=email)
        login_data.action = 2
        login_data.save()  


        registration_data = registration_db.objects.get(email=email)
        registration_data.action = 2
        registration_data.save() 


        msg = registration_db.objects.filter(status=2, action=1)
        return render(request, 'ADMIN/shop.html', {'r': msg})
def pur(request):
    data1 = order_db.objects.all()
    return render(request,'ADMIN/purchase.html',{'r':data1})


#SHOP FOLDER

def home_shop(request):
    a=request.session['sid']
    data1 = registration_db.objects.get(email=a)
    return render(request,'SHOP/home.html',{'pro':data1})
def addproduct(request):
    return render(request,'SHOP/addproduct.html')


def productdetails(request, product_id):
    product = product_db.objects.get(id=product_id)  # Get the product by ID
    return render(request, 'SHOP/details.html', {'product': product})

def productdetailsupdate(request, product_id):
    product = product_db.objects.get(id=product_id)  # Get the product by ID
    if request.method == 'POST':
        a = request.POST['price']
        b = request.POST['stock']
        product.price = a
        product.stock = b
        product.save()
        return render(request, 'SHOP/details.html', {'product': product})


def viewproducts(request):
    a = request.session['sid']
    data = registration_db.objects.get(email=a)
    productdata=product_db.objects.filter(idno=data.idno)
    return render(request,'SHOP/products.html',{'products':productdata})

def addproductdata(request):
    if request.method == 'POST':
        a = request.POST['product_id']
        b = request.POST['product_name']
        c = request.POST['product_description']
        d = request.POST['product_price']
        e = request.POST.get('product_category')
        f =request.FILES['product_image']
        s = request.POST['product_stock']

        r = request.session['sid']
        data = registration_db.objects.get(email=r)
        g=data.idno
        id=int(str(g)+str(a))
        try:
            data1 = product_db.objects.get(product_id=id)
            msg = 'THE PRODUCT ID IS ALREADY EXIST'
            return render(request,'SHOP/addproduct.html',{'msg':msg})
        except Exception:        
            data0 = product_db.objects.create(idno=g,product_id=id,name=b,description=c,price=d,category=e,image=f,stock=s)
           
            data0.save()

            msg = 'THE REGISTRATION IS COMPLETE'
            return render(request,'SHOP/addproduct.html',{'msg':msg})
def custreq(request):
    data1 = order_db.objects.all() #the upfate this to get the data from the database for particular shop
    return render(request,'SHOP/request.html',{'r':data1})

def makedeliver(request):
    if request.method == 'POST':
        orderid = request.POST['r1']  # Directly access POST data

        # Update the first database
        data = order_db.objects.get(orderid=orderid)
        data.deliverstatus = 1
        data.save()  # Save to the default database

        # Query for messages after successful updates
        # msg = registration_db.objects.filter(status=2, action=2)
        return render(request, 'SHOP/request.html')


#FARMER FOLDER

def home_farmer(request):
    return render(request,'FARMER/home.html')
def shop(request):
    productdata=product_db.objects.all
    return render(request,'FARMER/shop.html',{'products':productdata})
def shopdetails(request, product_id):
    product = product_db.objects.get(id=product_id) 
    a = request.session['fid']
    customer = registration_db.objects.get(email=a)
    return render(request, 'FARMER/details.html', {'product': product,'customer': customer})
def pay(request):
    if request.method == 'POST':

        a = request.session['fid']
        xyz = order_db.objects.filter(paymentstatus=0,customermail=a).delete()
        customer = registration_db.objects.get(email=a)
        name=customer.name
        email=customer.email
        product_name = request.POST.get('product_name')
        product_category = request.POST.get('product_category')
        product_description = request.POST.get('product_description')
        quantity = request.POST.get('quantity')
        total_price = request.POST.get('total_price')
        productid = request.POST.get('productid')
        value = order_db.objects.order_by('-orderid').first()
        if value is not None:
            orderid = value.orderid
            neworderid = orderid + 1
        else:
            neworderid = 1
        
#   you want to add product id or shop id here so that you can 
#   track the purchace for particular shop from where the order


        data = order_db.objects.create(orderid=neworderid,customername=name,customermail=email,productname=product_name,productcategory=product_category,quantity=quantity,totalprice=total_price,paymentstatus=0,deliverstatus=0,proid=productid)
        data.save()
        payprice=int(total_price)*100
        return render(request, 'FARMER/pay.html', {
            'product_name': product_name,
            'total_price': total_price,
            'payprice':payprice,
            'quantity': quantity,
            'orderid': neworderid,
            'product_category': product_category,
            'product_description': product_description,
            'name': name,
            'email': email
            
        })
def success(request):
    value = order_db.objects.order_by('-orderid').first()
    pro = product_db.objects.get(product_id=value.proid)
    
    bill = order_db.objects.get(orderid=value.orderid)
    pro.stock=pro.stock-bill.quantity
    pro.save()
    bill.paymentstatus=1
    bill.save()
    a = request.session['fid']
    xyz = order_db.objects.filter(paymentstatus=0,customermail=a).delete()
    productdata=product_db.objects.all
    return render(request,'FARMER/shop.html',{'products':productdata})









































#flask intgration

from django.shortcuts import render, redirect
import numpy as np
import pandas as pd
import requests
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
from .utils import disease_dic, fertilizer_dic  # Import utility dictionaries
from .models import ResNet9  # Import the ResNet9 model class

# Load the disease classification model
disease_classes = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

disease_model_path = 'app/models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()



def predict_image(img, model=disease_model):
    """
    Transforms an image to a tensor and predicts the disease label.
    :param img: Image data
    :param model: Model to use for prediction
    :return: Predicted disease label
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from the model
    yb = model(img_u)
    _, preds = torch.max(yb, dim=1)  # Get index with highest probability
    prediction = disease_classes[preds[0].item()]  # Retrieve the class label
    return prediction


def disease(request):
    """Handle disease prediction based on uploaded image."""
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return redirect(request.path)
        file = request.FILES.get('file')
        if not file:
            return render(request, 'FARMER/prediction.html', {'title': 'BOTANY GURU - Disease Detection'})
        try:
            img = file.read()
            prediction = predict_image(img)  # Predict disease from image
            prediction = str(disease_dic[prediction])  # Get disease description

            # Convert image to base64 for embedding in HTML
            import base64
            img_base64 = base64.b64encode(img).decode('utf-8')
            img_data = f"data:image/jpeg;base64,{img_base64}"  # Adjust the MIME type if necessary
            

            return render(request, 'FARMER/prediction_result.html', {'prediction': prediction,'img_data':img_data ,'title': 'BOTANY GURU - Disease Detection'})
        except Exception as e:
            print(e)  # Log the error for debugging
    return render(request, 'FARMER/prediction.html', {'title': 'BOTANY GURU - Disease Detection'})
