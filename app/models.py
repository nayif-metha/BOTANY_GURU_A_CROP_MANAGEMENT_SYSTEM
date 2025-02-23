from django.db import models

# Create your models here.
class registration_db(models.Model):
    idno = models.IntegerField()
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    profile = models.FileField()
    status = models.IntegerField()
    action=models.IntegerField()
    def __str__(self):
        return self.userid
    

class login_db(models.Model):
    password = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    status = models.IntegerField()
    action=models.IntegerField()
    def __str__(self):
        return self.userid
    

class product_db(models.Model):
    idno = models.IntegerField()
    product_id = models.IntegerField()
    name = models.CharField(max_length=255)  
    description = models.TextField() 
    price = models.IntegerField() 
    category = models.CharField(max_length=50) 
    image = models.ImageField(upload_to='products/') 
    stock = models.IntegerField()

    def __str__(self):
        return self.name
    
class order_db(models.Model):
    orderid = models.IntegerField()
    customername = models.CharField(max_length=255)  
    customermail = models.CharField(max_length=255)  
    productname = models.CharField(max_length=255) 
    productcategory = models.CharField(max_length=255)
    quantity = models.IntegerField()
    totalprice = models.IntegerField() 
    paymentstatus=models.IntegerField()
    deliverstatus=models.IntegerField()
    proid=models.IntegerField()


    def __str__(self):
        return self.customername
    
class PasswordReset(models.Model):
    user=models.ForeignKey(login_db,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)


import torch 
import torch.nn as nn
import torch.nn.functional as F


def ConvBlock(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
             nn.BatchNorm2d(out_channels),
             nn.ReLU(inplace=True)]
    if pool:
        layers.append(nn.MaxPool2d(4))
    return nn.Sequential(*layers)



# Model Architecture
class ResNet9(nn.Module):
    def __init__(self, in_channels, num_diseases):
        super().__init__()
        
        self.conv1 = ConvBlock(in_channels, 64)
        self.conv2 = ConvBlock(64, 128, pool=True) # out_dim : 128 x 64 x 64 
        self.res1 = nn.Sequential(ConvBlock(128, 128), ConvBlock(128, 128))
        
        self.conv3 = ConvBlock(128, 256, pool=True) # out_dim : 256 x 16 x 16
        self.conv4 = ConvBlock(256, 512, pool=True) # out_dim : 512 x 4 x 44
        self.res2 = nn.Sequential(ConvBlock(512, 512), ConvBlock(512, 512))
        
        self.classifier = nn.Sequential(nn.MaxPool2d(4),
                                       nn.Flatten(),
                                       nn.Linear(512, num_diseases))
        
    def forward(self, xb): # xb is the loaded batch
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.res2(out) + out
        out = self.classifier(out)
        return out  # Return the output tensor
