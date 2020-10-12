from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import datetime
import json


def index(request):
    products = Product.objects.all()
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = ceil(n / 4)
        allProds.append([prod, range(1, nslides), nslides])
    print(allProds)
    params = {'allprods':allProds}
    
    return render(request, 'shop/index.html',  params)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = ceil(n / 4)
        if len(prod) != 0:
            allProds.append([prod, range(1, nslides), nslides])
    params = {'allprods':allProds,'msg':""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg':"Please make sure to enter relevent search query"}
    return render(request, 'shop/search.html',  params)


def about(request):
    return render(request, 'shop/about.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', ' ')
        email = request.POST.get('email', ' ')
        phone = request.POST.get('phone', ' ')
        desc = request.POST.get('desc', ' ')
        response = True
        msg=''
        if name !='' and email!='' and phone != '' and desc !='':
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            msg = 'Thank you for contacting us ,we will get back to you soon'
        else:
            msg = 'All fields are required'
        return render(request, 'shop/contact.html', {'response':response,'msg':msg})
    return render(request, 'shop/contact.html')



def tracker(request):
    if request.method == "POST":
        OrderId = request.POST.get('OrderId','')
        email = request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=OrderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=OrderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp.strftime("%d %B %Y")})
                    response = json.dumps({"status":"success","updates":updates,"itemsjson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
        
    return render(request, 'shop/tracker.html')







def prodview(request,myid):
    #Fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product': product[0]})



def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsjson',' ')
        name = request.POST.get('name', ' ')
        amount = request.POST.get('amount', ' ')          
        email = request.POST.get('email', ' ')
        address = request.POST.get('address1', ' ') + " " + request.POST.get('address2',' ')
        city = request.POST.get('city', ' ')
        state = request.POST.get('state', ' ')
        zip_code = request.POST.get('zip_code', ' ')
        phone = request.POST.get('phone', ' ')
        order = Orders(items_json=items_json, name=name, amount=amount,email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id = order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True

        id = order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank,'id':id})

    return render(request, 'shop/checkout.html')

