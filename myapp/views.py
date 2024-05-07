from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from geopy.distance import geodesic

from myapp.models import *


def login(request):
    return render(request,"loginindex.html")

def login_post(request):
    email=request.POST['textfield']
    password=request.POST['textfield2']
    log=Login.objects.filter(username=email,password=password)
    if log.exists():
        log1=Login.objects.get(username=email,password=password)
        if log1.username != email or log1.password != password:
            return HttpResponse('''<Script>alert("Invalid user and password!");window.location="/myapp/login/"</Script>''')
        request.session['lid']=log1.id
        if log1.logintype=='admin':
            return HttpResponse('''<script>alert("Login Successful");window.location='/myapp/adminhome/'</script>''')
        elif log1.logintype=='Plant Shop':
            return HttpResponse('''<script>alert("Login Successful");window.location='/myapp/shophome/'</script>''')
        elif log1.logintype=='Pet Shop':
            return HttpResponse('''<script>alert("Login Successful");window.location='/myapp/petshophome/'</script>''')

        else:
            return HttpResponse('''<script>alert("INVALID");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert("INVALID");window.location='/myapp/login/'</script>''')



def plant_changepass(request):
    return render(request,"Plant shop/plant_changepassword.html")

def plant_changepass_post(request):
     cpassword= request.POST['current_password']
     newpassword = request.POST['new_password']
     confirmpassword = request.POST['confirm_password']
     lg=Login.objects.filter(id=request.session['lid'],password=cpassword)
     if newpassword==confirmpassword:
         lg2=Login.objects.filter(id=request.session['lid']).update(password=confirmpassword)
         return HttpResponse('''<script>alert("Succefully changed password");window.location='/myapp/login/'</script>''')
     else:
         return HttpResponse('''<script>alert("Password mismatch");window.location='/myapp/plant_changepass/'</script>''')






def pet_changepass(request):
    return render(request, "pet shop/pet_changepassword.html")


def pet_changepass_post(request):
    cpassword = request.POST['current_password']
    newpassword = request.POST['new_password']
    confirmpassword = request.POST['confirm_password']
    lg = Login.objects.filter(id=request.session['lid'], password=cpassword)
    if newpassword == confirmpassword:
        lg2 = Login.objects.filter(id=request.session['lid']).update(password=confirmpassword)
        return HttpResponse('''<script>alert("Succefully changed password");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert("Password mismatch");window.location='/myapp/plant_changepass/'</script>''')


def app_changepass(request):
    cpassword = request.POST['old']
    newpassword = request.POST['new']
    confirmpassword = request.POST['confirm']
    lid= request.POST['lid']
    lg = Login.objects.filter(id=lid, password=cpassword)
    if lg.exists():
        var=Login.objects.get(id=lid, password=cpassword)
        if var is not None:
            if newpassword == confirmpassword:
                var = Login.objects.filter(id=lid,password=cpassword).update(password=confirmpassword)

                return JsonResponse({'status': "ok"})
            else:
                return JsonResponse({'status': "no"})
        else:
            return JsonResponse({'status': "no"})




    else:
        return JsonResponse({'status': "no"})






def adminhome(request):
    return render(request, "admin/adminindex.html")

def signup(request):
    return render(request,"signupindex.html")
# def shop_editprof(request):
#     obj=Shop.objects.get(LOGIN_id=request.session['lid'])
#     return render(request, "Plant shop/shop_editprof.html",{'data':obj})

def signup_post(request):
    shop_name=request.POST['textfield']
    owner_name=request.POST['textfield1']
    photo=request.FILES['fileField']
    ph_no=request.POST['textfield2']
    email=request.POST['textfield3']
    place=request.POST['textfield4']
    post=request.POST['textfield5']
    pin=request.POST['textfield6']
    district=request.POST['textfield7']
    license=request.FILES['fileField2']
    shop_type=request.POST['select']
    password=request.POST['textfield8']
    confirm_password=request.POST['textfield9']

    from datetime import datetime
    date=datetime.now().strftime('%y%m%d-%H%M%S')+'.jpg'
    fs=FileSystemStorage()
    fs.save(date,photo)
    path=fs.url(date)

    from datetime import datetime
    date1 = "lic"+datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
    fs1 = FileSystemStorage()
    fs1.save(date1,license)
    path1 = fs1.url(date1)

    lobj=Login()
    lobj.username=email
    lobj.password=password
    lobj.logintype='pending'
    lobj.save()

    if password==confirm_password:
        obj=Shop()
        obj.shop_name=shop_name
        obj.owner_name=owner_name
        obj.photo=path
        obj.ph_no=ph_no
        obj.email=email
        obj.place=place
        obj.post=post
        obj.pin=pin
        obj.district=district
        obj.licence=path1
        obj.shop_type=shop_type
        obj.status='pending'
        obj.LOGIN=lobj
        obj.save()
        return HttpResponse('''<script>alert("SignUp Successful");window.location='/myapp/login/'</script>''')


def verifyshop(request):
    res=Shop.objects.filter(status='pending')
    return render(request, "admin/verification(view shops).html",{'data':res})

def verifyshop_post(request):
    search = request.POST['textfield']
    shop = request.POST['select']
    print(search)
    print(shop)
    if search == '':
        res = Shop.objects.filter(status='pending', shop_type__icontains=shop)
        return render(request, "admin/verification(view shops).html", {'data': res})
    elif shop == 'None':
        res = Shop.objects.filter(status='pending', shop_name__icontains=search)
        return render(request, "admin/verification(view shops).html", {'data': res})
    else:
        res = Shop.objects.filter(status='pending', shop_type__icontains=shop, shop_name__icontains=search)

        return render(request, "admin/verification(view shops).html", {'data': res})









def approve(request,id):
    var = Shop.objects.filter(LOGIN=id).update(status='Approved')
    v = Shop.objects.filter(LOGIN=id)[0]
    var1 = Login.objects.filter(id=id).update(logintype=v.shop_type)
    return HttpResponse('''<script>alert("Approved");window.location='/myapp/verifyshop/'</script>''')

def reject(request,id):
    var = Shop.objects.filter(LOGIN=id).update(status='Rejected')
    var1 = Login.objects.filter(id=id).update(logintype='Rejected')
    return HttpResponse('''<script>alert("Rejected");window.location='/myapp/verifyshop/'</script>''')

def approvedshop(request):
    res = Shop.objects.filter(status='Approved')
    return render(request, "admin/approved(view shops).html", {'data': res})

def approvedshop_post(request):
    search=request.POST['textfield']
    shop=request.POST['select']
    print(search)
    print(shop)
    if search == '':
        res = Shop.objects.filter(status='Approved', shop_type__icontains=shop)
        return render(request, "admin/approved(view shops).html", {'data': res})
    elif shop == 'None':
        res = Shop.objects.filter(status='Approved', shop_name__icontains=search)
        return render(request, "admin/approved(view shops).html", {'data': res})
    else:
        res = Shop.objects.filter(status='Approved', shop_type__icontains=shop, shop_name__icontains=search)
        return render(request, "admin/approved(view shops).html", {'data': res})



def rejectedshop(request):
    res = Shop.objects.filter(status='Rejected')
    return render(request, "admin/rejected(view shops).html", {'data': res})

def rejectedshop_post(request):
    search=request.POST['textfield']
    shop = request.POST['select']
    print(search)
    print(shop)
    if search == '':
        res = Shop.objects.filter(status='Rejected', shop_type__icontains=shop)
        return render(request, "admin/rejected(view shops).html", {'data': res})
    elif shop == 'None':
        res = Shop.objects.filter(status='Rejected', shop_name__icontains=search)
        return render(request, "admin/rejected(view shops).html", {'data': res})
    else:
        res = Shop.objects.filter(status='Rejected', shop_type__icontains=shop, shop_name__icontains=search)
        return render(request, "admin/rejected(view shops).html", {'data': res})



def verifydel(request):
    var=DeliveryBoy.objects.filter(status='pending')
    return render(request, "admin/verification(Del boy).html",{'data':var})

def verifydel_post(request):
    search=request.POST['textfield']

    print(search)
    #
    # if search == '':
    #     res = DeliveryBoy.objects.filter(status='pending', id__icontains=search)
    #     return render(request, "admin/verification(Del boy).html", {'data': res})
    # else:
    res = DeliveryBoy.objects.filter(status='pending', name__icontains=search)
    return render(request, "admin/verification(Del boy).html", {'data': res})

def approvedel(request, id):
    var = DeliveryBoy.objects.filter(LOGIN=id).update(status='Approved')
    var1 = Login.objects.filter(id=id).update(logintype='delivery_boy')
    return HttpResponse('''<script>alert("Approved");window.location='/myapp/verifydel/'</script>''')

def approveddel(request):
    res = DeliveryBoy.objects.filter(status='Approved')
    return render(request, "admin/approved(Del boy).html", {'data': res})

def approveddel_post(request):
    search=request.POST['textfield']
    res = DeliveryBoy.objects.filter(status='Approved', name__icontains=search)
    return render(request, "admin/approved(Del boy).html", {'data': res})


def rejectdel(request, id):
    var = DeliveryBoy.objects.filter(LOGIN=id).update(status='Rejected')
    var1 = Login.objects.filter(id=id).update(logintype='Rejected')
    return HttpResponse('''<script>alert("Rejected");window.location='/myapp/verifydel/'</script>''')




def rejecteddel(request):
    res = DeliveryBoy.objects.filter(status='Rejected')
    return render(request, "admin/rejected(Del boy).html", {'data': res})

def rejecteddel_post(request):
    search=request.POST['textfield']
    # if search == '':
    res = DeliveryBoy.objects.filter(status='Rejected',name__icontains=search)
    return render(request, "admin/rejected(Del boy).html", {'data': res})
    # else:
    #     res = DeliveryBoy.objects.filter(status='Rejected', name__icontains=search)
    #     return render(request, "admin/rejected(Del boy).html", {'data': res})

def admin_viewreviews(request):
    var=Plantreview.objects.all()
    return render(request,"admin/admin_view review.html",{'data':var})





# --------------------------------------------------shop----------------------------


def shophome(request):
    return render(request,'Plant Shop/plantindex.html')


def shop_prof(request):
    var=Shop.objects.get(LOGIN=request.session['lid'])
    return render(request, "Plant shop/shopprof.html",{'data':var})

def shop_editprof(request):
    obj=Shop.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "Plant shop/shop_editprof.html",{'data':obj})

def shop_editprof_post(request):
    shop_name=request.POST['textfield']
    owner_name=request.POST['textfield2']
    email=request.POST['textfield4']
    place=request.POST['textfield5']
    post=request.POST['textfield6']
    pin=request.POST['textfield7']
    # licence=request.FILES['fileField2']
    # shop_type=request.POST['select']
    district=request.POST['textfield8']
    ph_no=request.POST['textfield3']

    obj=Shop.objects.get(LOGIN_id=request.session['lid'])
    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']
        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        obj.photo = path
        obj.save()
    if 'fileField2' in request.FILES:
        licence= request.FILES['fileField2']
        from datetime import datetime
        date1 = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs1 = FileSystemStorage()
        fs1.save(date1, licence)
        path1 = fs1.url(date1)
        obj.licence = path1
        obj.save()

    obj.shop_name=shop_name
    obj.owner_name=owner_name
    obj.email=email
    obj.place=place
    obj.post=post
    obj.pin=pin
    # obj.shop_type=shop_type
    obj.district=district
    obj.ph_no=ph_no
    obj.save()
    if obj.shop_type=='Pet Shop':
        obj=Login.objects.filter(username=email).update(logintype='Pet Shop')
        return HttpResponse('''<script>alert('Ok');window.location='/myapp/login/'</script>''')
    else:
     return HttpResponse('''<script>alert('Ok');window.location='/myapp/shop_prof/'</script>''')

def addplant(request):
    return render(request, "Plant shop/addplant.html")

def addplant_post(request):
    plant_name=request.POST['textfield']
    scientific_name=request.POST['textfield2']
    photo=request.FILES['fileField']
    size=request.POST['textfield3']
    plant_type=request.POST['select']
    price=request.POST['textfield4']
    details=request.POST['textfield5']

    from datetime import datetime
    date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)

    obj=Plant()
    obj.SHOP_ID=Shop.objects.get(LOGIN_id=request.session['lid'])
    obj.plant_name=plant_name
    obj.scientific_name=scientific_name
    obj.photo=path
    obj.size=size
    obj.plant_type=plant_type
    obj.price=price
    obj.details=details
    obj.save()

    return HttpResponse('''<script>alert('Ok');window.location='/myapp/addplant/'</script>''')

def back_phome(request):
    return render(request,'Plant Shop/plantindex.html')

def viewplant(request):
    obj=Plant.objects.filter(SHOP_ID__LOGIN_id=request.session['lid'])
    return render(request, "plant shop/view plant.html",{'data':obj})
def viewplant_post(request):

    search = request.POST['textfield']
    plant_type = request.POST['select']
    res = Plant.objects.filter(SHOP_ID__LOGIN_id=request.session['lid'], plant_type__icontains=plant_type,plant_name__icontains=search)
    return render(request, "plant shop/view plant.html", {'data': res})
    #
    # search=request.POST['textfield']
    # plant_type=request.POST['select']
    # if search == '':
    #     res = Plant.objects.filter(plant_type__icontains=plant_type)
    #     return render(request, "plant shop/view plant.html", {'data': res})
    # elif plant_type == 'None':
    #     res = Plant.objects.filter(plant_name__icontains=search)
    #     return render(request, "plant shop/view plant.html", {'data': res})
    # else:
    #     res = Plant.objects.filter(plant_type__icontains=plant_type,plant_name__icontains=search)
    #     return render(request, "plant shop/view plant.html", {'data': res})


def details(request,id):
    obj = Plant.objects.get(SHOP_ID__LOGIN_id=request.session['lid'],id=id)
    return render(request, "plant shop/details.html", {'data': obj})



def details_post(request):
    search=request.POST['textfield']
    # if search == '':
    res = Plant.objects.filter(plant_name__icontains=search)
    return render(request, "plant shop/details.html", {'data': res})
    # else:
    #     res = DeliveryBoy.objects.filter(status='Rejected', name__icontains=search)
    #     return render(request, "admin/rejected(Del boy).html", {'data': res})











def delplant(request,id):
    var = Plant.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("delete");window.location='/myapp/viewplant/'</script>''')

def editplant(request,id):
    obj=Plant.objects.get(id=id)
    return render(request, "Plant shop/editplant.html",{'data':obj})

def editplant_post(request):
    plant_name=request.POST['textfield']
    scientific_name=request.POST['textfield2']
    size=request.POST['textfield3']
    price=request.POST['textfield4']
    plant_type=request.POST['select']
    details=request.POST['textfield5']
    id=request.POST['id']


    obj=Plant.objects.get(id=id)
    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']
        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        obj.photo = path
        obj.save()

    obj.plant_name=plant_name
    obj.scientific_name=scientific_name
    obj.size=size
    obj.price=price
    obj.plant_type=plant_type
    obj.details=details
    obj.save()
    return HttpResponse('''<script>alert('Ok');window.location='/myapp/viewplant/'</script>''')

def plantstock(request):
    res=Plant.objects.filter(SHOP_ID__LOGIN__id=request.session['lid'])
    return render(request, "Plant shop/plantstock.html",{"data":res})


def plantstock_post(request):
    plant_stock=request.POST['textfield3']
    PLANT=request.POST['select']
    res=Plant_stock.objects.filter(PLANT__id=PLANT)
    if res.exists():
        print("hlooooo")
        re=Plant_stock.objects.get(PLANT__id=PLANT)
        k=int(re.stock)
        h=k+int(plant_stock)
        re.stock=h
        re.save()
    else:
        re = Plant_stock()
        re.stock = plant_stock
        re.PLANT_id= PLANT
        re.save()
    return HttpResponse('''<script>alert('Ok');window.location='/myapp/plantstock/'</script>''')


def viewplantstock(request):
    obj=Plant_stock.objects.filter(PLANT__SHOP_ID__LOGIN_id=request.session['lid'])
    return render(request, "plant shop/viewstock.html",{'data':obj})
def viewplantstock_post(request):

    search = request.POST['textfield']
    plant_type = request.POST['select']
    res = Plant_stock.objects.filter(SHOP_ID__LOGIN_id=request.session['lid'], plant_type__icontains=plant_type,plant_name__icontains=search)
    return render(request, "plant shop/viewstock.html", {'data': res})



    # search=request.POST['textfield']
    # plant_type=request.POST['select']
    # if search == '':
    #     res = Plant.objects.filter(plant_type__icontains=plant_type)
    #     return render(request, "plant shop/viewstock.html", {'data': res})
    # elif plant_type == 'None':
    #     res = Plant.objects.filter(plant_name__icontains=search)
    #     return render(request, "plant shop/view plant.html", {'data': res})
    # else:
    #     res = Plant.objects.filter(plant_type__icontains=plant_type,plant_name__icontains=search)
    #     return render(request, "plant shop/viewstock.html", {'data': res})




def logout(request):
    request.session['lid']=''
    return redirect('/myapp/login/')

def shop_viewreviews(request):
    var=Plantreview.objects.filter(SHOP__LOGIN_id=request.session['lid'])
    return render(request,"Plant Shop/plan_view review.html",{'data':var})


def shop_viewassigneddel(request,id):
    var=Assigned_order.objects.filter(ORDERMAIN_id=id)

    return render(request,"Plant Shop/assignedDeliveryBoy.html",{'data':var})



# --------------------------------------------------Pet shop----------------------------

def petshophome(request):
    return render(request,'pet Shop/pethomeindex.html')



def petshop_prof(request):
    var=Shop.objects.get(LOGIN=request.session['lid'])
    return render(request, "pet shop/petshopprof.html",{'data':var})

def petshop_editprof(request):
    obj=Shop.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "Pet shop/petshop_editprof.html",{'data':obj})


def petshop_editprof_post(request):
    shop_name=request.POST['textfield']
    owner_name=request.POST['textfield2']
    email=request.POST['textfield4']
    place=request.POST['textfield5']
    post=request.POST['textfield6']
    pin=request.POST['textfield7']
    # licence=request.FILES['fileField2']
    # shop_type=request.POST['select']
    district=request.POST['textfield8']
    ph_no=request.POST['textfield3']

    obj=Shop.objects.get(LOGIN_id=request.session['lid'])
    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']
        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        obj.photo = path
        obj.save()
    if 'fileField2' in request.FILES:
        licence= request.FILES['fileField2']
        from datetime import datetime
        date1 = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs1 = FileSystemStorage()
        fs1.save(date1, licence)
        path1 = fs1.url(date1)
        obj.licence = path1
        obj.save()

    obj.shop_name=shop_name
    obj.owner_name=owner_name
    obj.email=email
    obj.place=place
    obj.post=post
    obj.pin=pin
    # obj.shop_type=shop_type
    obj.district=district
    obj.ph_no=ph_no
    obj.save()

    if obj.shop_type == 'Plant Shop':
        obj = Login.objects.filter(username=email).update(logintype='Plant Shop')
        return HttpResponse('''<script>alert('Ok');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert('Ok');window.location='/myapp/petshop_prof/'</script>''')



def addpet(request):
    return render(request, "pet shop/addpet.html")

def addpet_post(request):
    pet_name=request.POST['textfield']
    breed_name=request.POST['textfield2']
    photo=request.FILES['fileField']
    age=request.POST['textfield3']
    # pet_type=request.POST['select']
    price=request.POST['textfield4']
    details=request.POST['textfield5']

    from datetime import datetime
    date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)

    obj=Pet()
    obj.SHOP_ID=Shop.objects.get(LOGIN_id=request.session['lid'])
    obj.pet_name=pet_name
    obj.breed_name=breed_name
    obj.photo=path
    obj.age=age

    obj.price=price
    obj.details=details
    obj.save()

    return HttpResponse('''<script>alert('Ok');window.location='/myapp/viewpet/'</script>''')



def viewpet(request):
    obj=Pet.objects.filter(SHOP_ID__LOGIN_id=request.session['lid'])
    return render(request, "pet shop/view pet.html",{'data':obj})

def viewpet_post(request):
    search=request.POST['textfield']
    res=Pet.objects.filter(Q(pet_name__icontains=search)|Q(breed_name__icontains=search))
    return render(request, "pet shop/view pet.html", {'data': res})

def delpet(request,id):
    var = Pet.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("deleted");window.location='/myapp/viewpet/'</script>''')

def editpet(request,id):
    obj=Pet.objects.get(id=id)
    return render(request, "pet shop/editpet.html",{'data':obj})

def editpet_post(request):
    pet_name=request.POST['textfield']
    breed_name=request.POST['textfield2']
    age=request.POST['textfield3']
    price=request.POST['textfield4']
    details=request.POST['textfield5']
    id=request.POST['id']


    obj=Pet.objects.get(id=id)
    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']
        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        obj.photo = path
        obj.save()

    obj.pet_name=pet_name
    obj.breed_name=breed_name
    obj.age=age
    obj.price=price
    obj.details=details
    obj.save()
    return HttpResponse('''<script>alert('Ok');window.location='/myapp/viewpet/'</script>''')

def petstock(request):
    res=Pet.objects.filter(SHOP_ID__LOGIN__id=request.session['lid'])
    return render(request, "pet shop/petstock.html",{"data":res})


def petstock_post(request):
    pet_stock=request.POST['textfield3']
    PET=request.POST['select']
    res=Pet_stock.objects.filter(PET__id=PET)
    if res.exists():
        print("hlooooo")
        re = Pet_stock.objects.get(PET__id=PET)
        k = int(re.stock)
        h = k + int(pet_stock)
        re.stock = h
        re.save()
    else:
        re = Pet_stock()
        re.stock = pet_stock
        re.PET_id= PET
        re.save()
    return HttpResponse('''<script>alert('Ok');window.location='/myapp/petstock/'</script>''')





def viewpetstock(request):
    obj=Pet_stock.objects.filter(PET__SHOP_ID__LOGIN_id=request.session['lid'])
    return render(request, "pet shop/viewpetstock.html",{'data':obj})
def viewpetstock_post(request):
    search=request.POST['textfield']
    res=Pet.objects.filter(pet_name__icontains=search)
    return render(request, "pet shop/viewpetstock.html", {'data': res})


def loginapp(request):
   email = request.POST['email']
   password=request.POST['password']
   log = Login.objects.filter(username=email, password=password)
   if log.exists():
       log1 = Login.objects.get(username=email, password=password)
       lid = log1.id
       if log1.logintype == 'user':
           return JsonResponse({'status':"ok",'lid':str(lid),'type':log1.logintype})
       elif log1.logintype == 'delivery_boy':
           return JsonResponse({'status':"ok",'lid':str(lid),'type':log1.logintype})

       else:
           return JsonResponse({'status':"Invalid"})
   else:
       return JsonResponse({'status':"Invalid"})
   # return JsonResponse({'status':"ok"})




#user home

def signup_user(request):
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    email = request.POST['email']
    dob=request.POST['dob']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    gender = request.POST['gender']
    password=request.POST['password']
    c_password=request.POST['c_password']



    lobj = Login()
    lobj.username = email
    lobj.password = password
    lobj.logintype = 'user'
    lobj.save()

    if password == c_password:
        obj = User()
        obj.name = name
        obj.ph_no =ph_no
        obj.email=email
        obj.place= place
        obj.post =post
        obj.pin = pin
        obj.dob=dob
        obj.district = district
        obj.gender=gender
        obj.LOGIN = lobj
        obj.save()

    return JsonResponse({'status':"ok"})

def viewprof_user(request):
    lid=request.POST['lid']
    var=User.objects.get(LOGIN_id=lid)
    landmark=''
    city=''
    if DeliveryAddress.objects.filter(LOGIN_id=lid).exists():
        landmark=DeliveryAddress.objects.filter(LOGIN_id=lid).last().landmark
        city=DeliveryAddress.objects.filter(LOGIN_id=lid).last().city


    return JsonResponse({'status':'ok','name':var.name,'ph_no':var.ph_no,
                         'email':var.email,'gender':var.gender,
                         'place':var.place,
                         'post':var.post,
                         'pin':var.pin,
                         'city':city,
                         'landmark':landmark,
                         'district':var.district})
def viewprof_user_address(request):
    lid=request.POST['lid']
    var=User.objects.get(LOGIN_id=lid)


    return JsonResponse({'status':'ok','name':var.name,'ph_no':var.ph_no,

                         'place':var.place,
                         'post':var.post,
                         'pin':var.pin,

                         'district':var.district})

def viewaddress_user(request):
    # lid=request.POST['lid']
    # var=User.objects.get(LOGIN_id=lid)
    # landmark=''
    # city=''
    # if DeliveryAddress.objects.filter(LOGIN_id=lid).exists():
    #     landmark=DeliveryAddress.objects.filter(LOGIN_id=lid).last().landmark
    #     city=DeliveryAddress.objects.filter(LOGIN_id=lid).last().city

    lid=request.POST['lid']
    psid=request.POST['psid']
    var=DeliveryAddress.objects.get(id=psid)
    return JsonResponse({'status':'ok','name':var.name,'ph_no':var.ph_no,
                         'place':var.place,
                         'post':var.post,
                         'pin':var.pin,
                         'city':var.city,
                         'landmark':var.landmark,
                         'district':var.district})




def ediprof_user(request):
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    email = request.POST['email']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    gender = request.POST['gender']
    lid = request.POST['lid']

    obj = User.objects.get(LOGIN_id=lid)
    obj.name = name
    obj.ph_no = ph_no
    obj.email = email
    obj.place = place
    obj.post = post
    obj.pin = pin
    obj.district = district
    obj.gender = gender
    obj.save()


    lobj = Login.objects.get(id=lid)
    lobj.username = email
    lobj.save()



    return JsonResponse({'status':"ok"})


#view plantshop and their product

def user_viewplantshops(request):
    res=Shop.objects.filter(shop_type='Plant Shop')
    l = []
    for i in res:
        l.append({'id': i.id,
                  'shop_name':i.shop_name,
                  'owner_name':i.owner_name,
                  'email':i.email,
                  'place':i.place,
                  'post':i.post,
                  'pin':i.pin,
                  'district':i.district,
                  'photo':i.photo,
                  'licence':i.licence,
                  'ph_no':i.ph_no,})



    return JsonResponse({'status': "ok","data":l})

def user_viewshopplant(request):
    sid=request.POST['sid']
    var=Plant.objects.filter(SHOP_ID__id=sid)
    l=[]
    for i in var:
        l.append({'id':i.id,
                  'plant_name':i.plant_name,
                   'scientific_name':i.scientific_name,
                  # 'size':i.size,
                  # 'plant_type':i.plant_type,
                  'photo':i.photo,
                  'price':i.price,
                  # 'details':i.details
                  })
        print(l,"hhhhhhhhhhhhhhhh")

    return JsonResponse({'status': "ok","data":l})


def plantshop_search(request):
    search = request.POST['textfield']
    res = Plant.objects.filter(Q(plant_name__icontains=search)|Q(scientific_name__icontains=search))
    l=[]
    for i in res:
        l.append({'id':i.id,
                  'plant_name':i.plant_name,
                  'scientific_name':i.scientific_name,
                  'shop_name': i.SHOP_ID.shop_name,

                  # 'size':i.size,
                  # 'plant_type':i.plant_type,
                  'photo':i.photo,
                  'price':i.price,
                  # 'details':i.details
                  })
    # res = Plant.objects.filter(Q(plant_name__icontains=search)|Q(scientific_name__icontains=search))
    return JsonResponse({'status': "ok","data":l})



def petshop_search(request):
    search = request.POST['textfield']
    res = Pet.objects.filter(Q(pet_name__icontains=search)|Q(breed_name__icontains=search))
    l=[]
    for i in res:
        l.append({'id':i.id,
                  'pet_name':i.pet_name,
                   'breed_name':i.breed_name,
                  'shop_name': i.SHOP_ID.shop_name,

                  # 'size':i.size,
                  # 'plant_type':i.plant_type,
                  'photo':i.photo,
                  'price':i.price,
                  # 'details':i.details
                  })
    # res = Plant.objects.filter(Q(plant_name__icontains=search)|Q(scientific_name__icontains=search))
    return JsonResponse({'status': "ok","data":l})

def user_viewsingleplant(request):
    pid=request.POST['pid']
    i=''
    if Plant_stock.objects.filter(PLANT_id=pid).exists():
        v=Plant_stock.objects.get(PLANT_id=pid)
        var=Plant.objects.get(id=pid)


        if v.stock >0:

            return JsonResponse({'status': "ok",
                                 "id":var.id,
                                 "plant_name":var.plant_name,
                                 "scientific_name":var.scientific_name,
                                 "size":var.size,
                                 "plant_type":var.plant_type,
                                 "photo":var.photo,
                                 "price":var.price,
                                 "details":var.details,
                                 "stock":v.stock,
                                 })
        else:
            return JsonResponse({'status': "ok",
                                 "id": var.id,
                                 "plant_name": var.plant_name,
                                 "scientific_name": var.scientific_name,
                                 "size": var.size,
                                 "plant_type": var.plant_type,
                                 "photo": var.photo,
                                 "price": var.price,
                                 "details": var.details,
                                 "stock": 'out',
                                 })

    else:
        var = Plant.objects.get(id=pid)
        return JsonResponse({'status': "ok",
                             "id": var.id,
                             "plant_name": var.plant_name,
                             "scientific_name": var.scientific_name,
                             "size": var.size,
                             "plant_type": var.plant_type,
                             "photo": var.photo,
                             "price": var.price,
                             "details": var.details,
                             "stock":"out",
                             })


def user_viewoneplant(request):
    pid=request.POST['pid']
    i = ''
    if Plant_stock.objects.filter(PLANT_id=pid).exists():
        v=Plant_stock.objects.get(PLANT_id=pid)
        var=Plant.objects.get(id=pid)
        if v.stock >0:

            return JsonResponse({'status': "ok","id":var.id,
                                 "plant_name":var.plant_name,
                                 "scientific_name":var.scientific_name,
                                 "size":var.size,
                                 "plant_type":var.plant_type,
                                 "photo":var.photo,
                                 "price":var.price,
                                 "details":var.details,
                                 "stock": v.stock,

                                 })
        else:
                return JsonResponse({'status': "ok",
                                     "id": var.id,
                                     "plant_name": var.plant_name,
                                     "scientific_name": var.scientific_name,
                                     "size": var.size,
                                     "plant_type": var.plant_type,
                                     "photo": var.photo,
                                     "price": var.price,
                                     "details": var.details,
                                     "stock": 'out',
                                     })

    else:
        var = Plant.objects.get(id=pid)
        return JsonResponse({'status': "ok",
                             "id": var.id,
                             "plant_name": var.plant_name,
                             "scientific_name": var.scientific_name,
                             "size": var.size,
                             "plant_type": var.plant_type,
                             "photo": var.photo,
                             "price": var.price,
                             "details": var.details,
                             "stock": "out",
                             })


#view petshop and their product



def user_viewpetshops(request):
    res=Shop.objects.filter(shop_type='Pet Shop')
    l = []
    for i in res:
        l.append({'id': i.id,
                  'shop_name':i.shop_name,
                  'owner_name':i.owner_name,
                  'email':i.email,
                  'place':i.place,
                  'post':i.post,
                  'pin':i.pin,
                  'district':i.district,
                  'photo':i.photo,
                  'licence':i.licence,
                  'ph_no':i.ph_no,})



    return JsonResponse({'status': "ok","data":l})


def user_viewshoppet(request):
    sid=request.POST['sid']
    var=Pet.objects.filter(SHOP_ID__id=sid)
    l=[]
    for i in var:
        l.append({'id':i.id,
                  'pet_name':i.pet_name,
                   'breed_name':i.breed_name,
                  # 'size':i.size,
                  # 'plant_type':i.plant_type,
                  'photo':i.photo,
                  'price':i.price,
                  # 'details':i.details
                  })
        print(l,"hhhhhhhhhhhhhhhh")

    return JsonResponse({'status': "ok","data":l})


# def user_viewsinglepet(request):
#     pid=request.POST['pid']
#       i = ''
#       if Pet_stock.objects.filter(PET_id=pid).exists():
#         v = Pet_stock.objects.get(PET_id=pid)
#         var = Pet.objects.get(id=pid)
#
#         if v.stock >0:
#
#     var=Pet.objects.get(id=pid)
#     return JsonResponse({'status': "ok","id":var.id,
#                          "pet_name":var.pet_name,
#                          "breed_name":var.breed_name,
#                          "age":var.age,
#                          "photo":var.photo,
#                          "price":var.price,
#                          "details":var.details
#                          })




def user_viewsinglepet(request):
  pid=request.POST['pid']
  i=''
  if Pet_stock.objects.filter(PET_id=pid).exists():
     v=Pet_stock.objects.get(PET_id=pid)
     var=Pet.objects.get(id=pid)


     if int(v.stock) >0:

        return JsonResponse({'status': "ok",
                                 "id":var.id,
                                 "pet_name":var.pet_name,
                                 "breed_name":var.breed_name,
                                 "age":var.age,
                                 "photo":var.photo,
                                 "price":var.price,
                                 "details":var.details,
                                 "stock":v.stock,
                                 })
     else:
        return JsonResponse({'status': "ok",
                                 "id": var.id,
                                 "pet_name": var.pet_name,
                                 "breed_name": var.breed_name,
                                 "age": var.age,
                                 "photo": var.photo,
                                 "price": var.price,
                                 "details": var.details,
                                 "stock": 'out',
                                 })

  else:
        var = Pet.objects.get(id=pid)
        return JsonResponse({'status': "ok",
                             "id": var.id,
                             "pet_name": var.pet_name,
                             "breed_name": var.breed_name,
                             "age": var.age,
                             "photo": var.photo,
                             "price": var.price,
                             "details": var.details,
                             "stock":"out",
                             })





def user_viewplant(request):
    var=Plant.objects.all()
    var1=Shop.objects.all()
    l=[]
    for i in var:
        l.append({'id':i.id,
                  'plant_name':i.plant_name,
                  'shop_name':i.SHOP_ID.shop_name,
                  'scientific_name':i.scientific_name,
                  'size':i.size,
                  'plant_type':i.plant_type,
                  'photo':i.photo,
                  'price':i.price,
                  'details':i.details })


    return JsonResponse({'status': "ok","data":l})

def user_viewpet(request):
    var=Pet.objects.all()
    l=[]
    for i in var:
        l.append({'id':i.id,
                  'pet_name':i.pet_name,
                  'breed_name':i.breed_name,
                  'shop_name': i.SHOP_ID.shop_name,
                  'age':i.age,
                  # 'plant_type':i.plant_type,
                  'photo':i.photo,
                  'price':i.price,
                  'details':i.details })

    return JsonResponse({'status': "ok","data":l})

def user_viewonepet(request):
    pid=request.POST['pid']
    var=Pet.objects.get(id=pid)
    return JsonResponse({'status': "ok","id":var.id,
                         "pet_name":var.pet_name,
                         "breed_name":var.breed_name,
                         "age":var.age,
                         "photo":var.photo,
                         "price":var.price,
                         "details":var.details
                         })




def user_viewonepet(request):
    pid=request.POST['pid']
    i = ''
    if Pet_stock.objects.filter(PET_id=pid).exists():
        v=Pet_stock.objects.get(PET_id=pid)
        var=Pet.objects.get(id=pid)
        if int(v.stock) >0:

            return JsonResponse({'status': "ok",
                                 "id":var.id,
                                 "pet_name":var.pet_name,
                                 "breed_name":var.breed_name,
                                 "age":var.age,
                                 "photo":var.photo,
                                 "price":var.price,
                                 "details":var.details,
                                 "stock": v.stock,

                                 })
        else:
                return JsonResponse({'status': "ok",
                                 "id":var.id,
                                 "pet_name":var.pet_name,
                                 "breed_name":var.breed_name,
                                 "age":var.age,
                                 "photo":var.photo,
                                 "price":var.price,
                                 "details":var.details,
                                 "stock": 'out',
                                     })

    else:
        var = Pet.objects.get(id=pid)
        return JsonResponse({'status': "ok",
                                 "id":var.id,
                                 "pet_name":var.pet_name,
                                 "breed_name":var.breed_name,
                                 "age":var.age,
                                 "photo":var.photo,
                                 "price":var.price,
                                 "details":var.details,
                                 "stock": 'out',
                                     })





def user_addplantcart(request):
    lid= request.POST['lid']
    pid= request.POST['pid']

    print(pid,"hiiiiiiiiiiiiiiiiiii")

    # quantity= request.POST['quantity']
    res=Plant_cart.objects.filter(PLANT_id=pid,USER__LOGIN_id=lid)
    if res.exists():
        return JsonResponse({'status': "no"})
    c=Plant_cart()
    c.PLANT=Plant.objects.get(id=pid)
    c.USER=User.objects.get(LOGIN_id=lid)
    c.quantity=1
    c.save()
    return JsonResponse({'status': "ok"})


def userhome_addplantcart(request):
    lid= request.POST['lid']
    pid= request.POST['pid']

    print(pid,"hiiiiiiiiiiiiiiiiiii")

    # quantity= request.POST['quantity']
    res=Plant_cart.objects.filter(PLANT_id=pid,USER__LOGIN_id=lid)
    if res.exists():
        return JsonResponse({'status': "no"})
    c=Plant_cart()
    c.PLANT=Plant.objects.get(id=pid)
    c.USER=User.objects.get(LOGIN_id=lid)
    c.quantity=1
    c.save()
    return JsonResponse({'status': "ok"})

def userhome_addpetcart(request):
    lid= request.POST['lid']
    pid= request.POST['pid']

    print(pid,"hiiiiiiiiiiiiiiiiiii")

    # quantity= request.POST['quantity']
    res=Pet_cart.objects.filter(PET_id=pid,USER__LOGIN_id=lid)
    if res.exists():
        return JsonResponse({'status': "no"})
    c=Pet_cart()
    c.PET=Pet.objects.get(id=pid)
    c.USER=User.objects.get(LOGIN_id=lid)
    c.quantity=1
    c.save()
    return JsonResponse({'status': "ok"})


#plant cart

def viewplantcart(request):
    lid=request.POST['lid']
    var =Plant_cart.objects.filter(USER__LOGIN_id=lid)
    n=''
    q=''
    m='yes'
    if DeliveryAddress.objects.filter(LOGIN_id=lid).exists():
        n="yes"
    l = []
    for i in var:
        s=Plant_stock.objects.filter(PLANT_id=i.PLANT.id)

        curstock=0

        if s.exists():
            curstock=s[0].stock

        # print(s.stock)
        # q="no"
        if curstock==0:
            q='yes'
            m="no"
        l.append({'id': i.id,
                  'plant_name': i.PLANT.plant_name,
                  # 'scientific_name':i.scientific_name,
                  'quantity':str(i.quantity),
                  # 'plant_type':i.plant_type,
                  'photo': i.PLANT.photo,
                   'price':str(float(i.PLANT.price)*float(i.quantity)),
                  'n':n,
                  's': curstock,
                  'q':q
                  })
        print(q,'qqqq')
        print(n,'nn')
        print(l)


    print(n,"=======",m)

    return JsonResponse({'status': "ok", "data": l,"n":n,"q":m})

def addplant_quantitycart(request):
    qn=request.POST['qty']
    pid=request.POST['pid']
    lid = request.POST['lid']
    l=''
    if Plant_stock.objects.filter(stock__gte=qn).exists():
        l='yes'
        print(l)
        print(qn)
    if Plant_cart.objects.filter(id=pid, USER__LOGIN_id=lid).exists():
        Plant_cart.objects.filter(id=pid, USER__LOGIN_id=lid).update(quantity=qn)
    else:
        Pla = Plant_cart()
        Pla.USER = User.objects.get(LOGIN_id=lid)
        Pla.PLANT_id = Plant_cart.objects.filter(id=pid, USER__LOGIN_id=lid)[0].PLANT_id
        Pla.quantity = qn
        Pla.save()
    return JsonResponse({'status': "ok","l":l})






def delcart(request):
    aa=request.POST['pid']
    var = Plant_cart.objects.filter(id=aa).delete()
    return JsonResponse({'status': "ok"})




def delpetcart(request):
    aa=request.POST['pid']
    var = Pet_cart.objects.filter(id=aa).delete()
    return JsonResponse({'status': "ok"})#pet cart


#
# def user_addplantcart(request):
#     lid= request.POST['lid']
#     pid= request.POST['pid']
#     # quantity= request.POST['quantity']
#     res=Plant_cart.objects.filter(PLANT_id=pid,USER__LOGIN_id=lid)
#     if res.exists():
#         return JsonResponse({'status': "no"})
#     c=Plant_cart()
#     c.PLANT=Plant.objects.get(id=pid)
#     c.USER=User.objects.get(LOGIN_id=lid)
#     c.quantity=1
#     c.save()
#
#     return JsonResponse({'status': "ok"})
#
# #plant cart
#
# def viewplantcart(request):
#     lid=request.POST['lid']
#     var = Plant_cart.objects.filter(USER__LOGIN_id=lid)
#     n=''
#     q=''
#     if DeliveryAddress.objects.filter(LOGIN_id=lid).exists():
#         n="yes"
#     l = []
#     for i in var:
#         s=Plant_stock.objects.get(PLANT_id=i.PLANT.id)
#         print(s.stock)
#         if int(Plant_stock.objects.get(PLANT_id=i.PLANT.id).stock)==0:
#             q='yes'
#         l.append({'id': i.id,
#                   'plant_name': i.PLANT.plant_name,
#                   # 'scientific_name':i.scientific_name,
#                   'quantity':str(i.quantity),
#                   # 'plant_type':i.plant_type,
#                   'photo': i.PLANT.photo,
#                    'price':str(float(i.PLANT.price)*float(i.quantity)),
#                   'n':n,
#                   's':s.stock,
#                   'q':q
#                   })
#     return JsonResponse({'status': "ok", "data": l,"n":n,"q":q})
#
# def addplant_quantitycart(request):
#     qn=request.POST['qty']
#     pid=request.POST['pid']
#     lid = request.POST['lid']
#     l=''
#     if Plant_stock.objects.filter(stock__gte=qn).exists():
#         l='yes'
#         print(l)
#         print(qn)
#     if Plant_cart.objects.filter(id=pid, USER__LOGIN_id=lid).exists():
#         Plant_cart.objects.filter(id=pid, USER__LOGIN_id=lid).update(quantity=qn)
#     else:
#         Pla = Plant_cart()
#         Pla.USER = User.objects.get(LOGIN_id=lid)
#         Pla.PLANT_id = Plant_cart.objects.filter(id=pid, USER__LOGIN_id=lid)[0].PLANT_id
#         Pla.quantity = qn
#         Pla.save()
#     return JsonResponse({'status': "ok","l":l})








def user_addpetcart(request):
    lid= request.POST['lid']
    pid= request.POST['pid']

    print(pid,"hiiiiiiiiiiiiiiiiiii")

    # quantity= request.POST['quantity']
    res=Pet_cart.objects.filter(PET_id=pid,USER__LOGIN_id=lid)
    if res.exists():
        return JsonResponse({'status': "no"})
    c=Pet_cart()
    c.PET=Plant.objects.get(id=pid)
    c.USER=User.objects.get(LOGIN_id=lid)
    c.quantity=1
    c.save()
    return JsonResponse({'status': "ok"})












def viewpetcart(request):
    lid = request.POST['lid']
    var = Pet_cart.objects.filter(USER__LOGIN_id=lid)
    n = ''
    q = ''
    m = 'yes'
    if DeliveryAddress.objects.filter(LOGIN_id=lid).exists():
        n = "yes"
    l = []
    for i in var:
        s = Pet_stock.objects.filter(PET_id=i.PET.id)

        curstock = 0

        if s.exists():
            curstock = s[0].stock

        # print(s.stock)
        # q="no"
        if curstock == 0:
            q = 'yes'
            m = "no"
        l.append({'id': i.id,
                  'pet_name': i.PET.pet_name,
                  # 'scientific_name':i.scientific_name,
                  'quantity': str(i.quantity),
                  # 'plant_type':i.plant_type,
                  'photo': i.PET.photo,
                  'price': str(float(int(i.PET.price)) * float(i.quantity)),
                  'n': n,
                  's': curstock,
                  'q': q
                  })
        print(q, 'qqqq')
        print(n, 'nn')
        print(l)

    print(n, "=======", m)

    return JsonResponse({'status': "ok", "data": l, "n": n, "q": m})


def addpet_quantitycart(request):
    qn=request.POST['qty']
    pid=request.POST['pid']
    lid = request.POST['lid']
    l=''
    if Pet_stock.objects.filter(stock__gte=qn).exists():
        l='yes'
        print(l)
        print(qn)
    if Pet_cart.objects.filter(id=pid, USER__LOGIN_id=lid).exists():
        Pet_cart.objects.filter(id=pid, USER__LOGIN_id=lid).update(quantity=qn)
    else:
        Pla = Pet_cart()
        Pla.USER = User.objects.get(LOGIN_id=lid)
        Pla.PET_id = Pet_cart.objects.filter(id=pid, USER__LOGIN_id=lid)[0].PET_id
        Pla.quantity = qn
        Pla.save()
    return JsonResponse({'status': "ok","l":l})





#address


def add_address(request):
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    place = request.POST['place']
    city = request.POST['city']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    landmark = request.POST['landmark']
    lid=request.POST['lid']

    c = DeliveryAddress()
    c.LOGIN_id=lid
    c.name=name
    c.ph_no=ph_no
    c.place=place
    c.city=city
    c.post=post
    c.pin=pin
    c.district=district
    c.landmark=landmark
    c.save()


    return JsonResponse({'status':"ok"})

def user_makepayment(request):
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    place = request.POST['place']
    city = request.POST['city']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    landmark = request.POST['landmark']
    lid = request.POST['lid']

    c = DeliveryAddress()
    c.LOGIN_id = lid
    c.name = name
    c.ph_no = ph_no
    c.place = place
    c.city = city
    c.post = post
    c.pin = pin
    c.district = district
    c.landmark = landmark
    c.save()



    Amount=float(request.POST['amount'])

    res = Plant_cart.objects.filter(USER__LOGIN_id=lid).values_list('PLANT__SHOP_ID_id').distinct()
    for i in res:
        print(i)
        mytotal = 0

        res2 = Plant_cart.objects.filter(USER__LOGIN_id=lid,PLANT__SHOP_ID_id=i[0])

        boj = Plant_ordermain()
        boj.USER = User.objects.get(LOGIN_id=lid)
        # t=i.amount*i.qty
        boj.amount = 0
        boj.deldate = "with in 5 days"
        import datetime
        boj.date = datetime.datetime.now().date().today()
        boj.SHOP_id = i[0]
        boj.status='pending'
        boj.ADDRESS=c
        # boj = Stock.objects.get(PRODUCT_id=[0])
        boj.save()







        ress = Payment()
        ress.PLANT_ORDERMAIN = boj
        ress.save()
        for j in res2:
            quantity = int(j.quantity)
            stock = Plant_stock.objects.filter(PLANT_id=j.PLANT_id, stock__gte=quantity)

            if stock.exists():
                stock=0
                bs=Plant_ordersub()
                bs.PLANT_ORDERMAIN=boj
                bs.PLANT_id=j.PLANT.id
                bs.quantity=j.quantity
                bs.save()

                mytotal+=(float(j.PLANT.price)*int(j.quantity))

                f = Plant_stock.objects.get(PLANT=j.PLANT)

                Plant_stock.objects.filter(PLANT_id=j.PLANT_id).update(stock=int(f.stock) - int(j.quantity))
        Plant_cart.objects.filter(PLANT__SHOP_ID_id=i[0], USER__LOGIN_id=lid).delete()
        boj=Plant_ordermain.objects.get(id=boj.id)
        boj.amount=mytotal
        boj.save()

    return JsonResponse({'k':'0','status':"ok"})
def user_makepaymentto(request):

    lid = request.POST['lid']
    aid = request.POST['aid']





    Amount=float(request.POST['amount'])

    res = Plant_cart.objects.filter(USER__LOGIN_id=lid).values_list('PLANT__SHOP_ID_id').distinct()
    for i in res:
        print(i)
        mytotal = 0

        res2 = Plant_cart.objects.filter(USER__LOGIN_id=lid,PLANT__SHOP_ID_id=i[0])

        boj = Plant_ordermain()
        boj.deldate = "with in 5 days"
        boj.USER = User.objects.get(LOGIN_id=lid)
        # t=i.amount*i.qty
        boj.amount = 0
        import datetime
        boj.date = datetime.datetime.now().date().today()
        boj.SHOP_id = i[0]
        boj.status='pending'
        boj.ADDRESS_id=aid
        # boj = Stock.objects.get(PRODUCT_id=[0])
        boj.save()
        ress = Payment()
        ress.PLANT_ORDERMAIN = boj
        ress.save()
        for j in res2:
            quantity = int(j.quantity)
            print(quantity)
            stock = Plant_stock.objects.filter(PLANT_id=j.PLANT_id)
            print(stock)
            if stock.exists():
                stock=0
                bs=Plant_ordersub()
                bs.PLANT_ORDERMAIN=boj
                bs.PLANT_id=j.PLANT.id
                bs.quantity=j.quantity
                bs.save()

                mytotal+=(float(j.PLANT.price)*int(j.quantity))

                f = Plant_stock.objects.get(PLANT=j.PLANT)

                Plant_stock.objects.filter(PLANT_id=j.PLANT_id).update(stock=int(f.stock) - int(j.quantity))
        Plant_cart.objects.filter(PLANT__SHOP_ID_id=i[0], USER__LOGIN_id=lid).delete()
        boj=Plant_ordermain.objects.get(id=boj.id)
        boj.amount=mytotal
        boj.save()

    return JsonResponse({'k':'0','status':"ok"})

def user_makepetpayment(request):
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    place = request.POST['place']
    city = request.POST['city']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    landmark = request.POST['landmark']
    lid = request.POST['lid']

    c = DeliveryAddress()
    c.LOGIN_id = lid
    c.name = name
    c.ph_no = ph_no
    c.place = place
    c.city = city
    c.post = post
    c.pin = pin
    c.district = district
    c.landmark = landmark
    c.save()



    Amount=float(request.POST['amount'])

    res = Pet_cart.objects.filter(USER__LOGIN_id=lid).values_list('PET__SHOP_ID_id').distinct()
    for i in res:
        print(i)
        mytotal = 0

        res2 = Pet_cart.objects.filter(USER__LOGIN_id=lid,PET__SHOP_ID_id=i[0])

        boj = Pet_ordermain()
        boj.USER = User.objects.get(LOGIN_id=lid)
        # t=i.amount*i.qty
        boj.amount = 0
        boj.deldate = "with in 5 days"
        import datetime
        boj.date = datetime.datetime.now().date().today()
        boj.SHOP_id = i[0]
        boj.status='pending'
        boj.ADDRESS=c
        # boj = Stock.objects.get(PRODUCT_id=[0])
        boj.save()







        ress = Payment()
        ress.PET_ORDERMAIN = boj
        ress.save()
        for j in res2:
            quantity = int(j.quantity)
            stock = Pet_stock.objects.filter(PET_id=j.PET_id, stock__gte=quantity)

            if stock.exists():
                stock=0
                bs=Pet_ordersub()
                bs.PET_ORDERMAIN=boj
                bs.PET_id=j.PLANT.id
                bs.quantity=j.quantity
                bs.save()

                mytotal+=(float(j.PET.price)*int(j.quantity))

                f = Pet_stock.objects.get(PLANT=j.PLANT)

                Pet_stock.objects.filter(PET_id=j.PET_id).update(stock=int(f.stock) - int(j.quantity))
        Pet_cart.objects.filter(PET__SHOP_ID_id=i[0], USER__LOGIN_id=lid).delete()
        boj=Pet_ordermain.objects.get(id=boj.id)
        boj.amount=mytotal
        boj.save()

    return JsonResponse({'k':'0','status':"ok"})
def user_makepetpaymentto(request):

    lid = request.POST['lid']
    aid = request.POST['aid']





    Amount=float(request.POST['amount'])

    res = Pet_cart.objects.filter(USER__LOGIN_id=lid).values_list('PET__SHOP_ID_id').distinct()
    for i in res:
        print(i)
        mytotal = 0

        res2 = Pet_cart.objects.filter(USER__LOGIN_id=lid,PET__SHOP_ID_id=i[0])

        boj = Pet_ordermain()
        boj.deldate = "with in 5 days"
        boj.USER = User.objects.get(LOGIN_id=lid)
        # t=i.amount*i.qty
        boj.amount = 0
        import datetime
        boj.date = datetime.datetime.now().date().today()
        boj.SHOP_id = i[0]
        boj.status='pending'
        boj.ADDRESS_id=aid
        # boj = Stock.objects.get(PRODUCT_id=[0])
        boj.save()
        ress = Payment()
        ress.PET_ORDERMAIN = boj
        ress.save()
        for j in res2:
            quantity = int(j.quantity)
            print(quantity)
            stock = Pet_stock.objects.filter(PET_id=j.PET_id)
            print(stock)
            if stock.exists():
                stock=0
                bs=Pet_ordersub()
                bs.PET_ORDERMAIN=boj
                bs.PET_id=j.PET.id
                bs.quantity=j.quantity
                bs.save()

                mytotal+=(float(j.PET.price)*int(j.quantity))

                f = Pet_stock.objects.get(PET=j.PET)

                Pet_stock.objects.filter(PET_id=j.PET_id).update(stock=int(f.stock) - int(j.quantity))
        Pet_cart.objects.filter(PET__SHOP_ID_id=i[0], USER__LOGIN_id=lid).delete()
        boj=Pet_ordermain.objects.get(id=boj.id)
        boj.amount=mytotal
        boj.save()

    return JsonResponse({'k':'0','status':"ok"})





# def user_vieworders(request):
#     return
#




# Petreview.objects.all().delete()
# Plant_ordermain.objects.all().delete()
# Plant_stock.objects.all().delete()



def signup_del(request):
    name = request.POST['name']
    Ph_no = request.POST['Ph_no']
    email = request.POST['email']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    gender = request.POST['gender']
    photo=request.POST['photo']
    idproof=request.POST['idproof']
    password=request.POST['password']
    c_password=request.POST['c_password']

    from datetime import datetime
    date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
    import base64
    a=base64.b64decode(photo)
    fh=open('C:\\Users\\minha\\PycharmProjects\\petplantshop\\media\\delivery\\'+date,'wb')
    path='/media/delivery/'+date
    fh.write(a)
    fh.close()

    from datetime import datetime
    date1=datetime.now().strftime('%Y%m%d-%H%M%S')+'idp.jpg'
    import base64
    a1=base64.b64decode(idproof)
    fh1=open('C:\\Users\\minha\\PycharmProjects\\petplantshop\\media\\delivery\\id\\'+date1,'wb')
    path1='/media/delivery/id/'+date1
    fh1.write(a1)
    fh1.close()


    lobj = Login()
    lobj.username = email
    lobj.password = password
    lobj.logintype = 'pending'
    lobj.save()

    if password == c_password:
        obj = DeliveryBoy()
        obj.name = name
        obj.ph_no = Ph_no
        obj.email = email
        obj.place = place
        obj.post = post
        obj.pin = pin
        obj.district = district
        obj.gender = gender
        obj.photo= path
        obj.idproof=path1
        obj.status="pending"
        obj.LOGIN = lobj
        obj.save()

    return JsonResponse({'status': "ok"})

def viewprof_del(request):
    lid=request.POST['lid']
    var=DeliveryBoy.objects.get(LOGIN_id=lid)
    return JsonResponse({'status':'ok',
                         'name':var.name,
                         'photo':var.photo,
                         'ph_no':var.ph_no,
                         'email':var.email,
                         'gender':var.gender,
                         'place':var.place,
                         'post':var.post,
                         'pin':var.pin,
                         'district':var.district,
                         'idproof':var.idproof})

def ediprof_del(request):
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    email = request.POST['email']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    gender = request.POST['gender']
    photo = request.POST['photo']
    idproof = request.POST['idproof']
    lid = request.POST['lid']

    obj = DeliveryBoy.objects.get(LOGIN_id=lid)
    if len(photo)>0:
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
        import base64
        a = base64.b64decode(photo)
        fh = open('C:\\Users\\minha\\PycharmProjects\\petplantshop\\media\\delivery\\' + date, 'wb')
        path = '/media/delivery/' + date
        fh.write(a)
        fh.close()
        obj.photo = path

    if len(idproof)>0:
        from datetime import datetime
        date1 = datetime.now().strftime('%Y%m%d-%H%M%S') + 'idp.jpg'
        import base64
        a1 = base64.b64decode(idproof)
        fh1 = open('C:\\Users\\minha\\PycharmProjects\\petplantshop\\media\\delivery\\id\\' + date1, 'wb')
        path1 = '/media/delivery/id/' + date1
        fh1.write(a1)
        fh1.close()
        obj.idproof = path1

    obj.name = name
    obj.ph_no = ph_no
    obj.email = email
    obj.place = place
    obj.post = post
    obj.pin = pin
    obj.district = district
    obj.gender = gender
    obj.save()


    lobj = Login.objects.get(id=lid)
    lobj.username = email
    lobj.save()



    return JsonResponse({'status':"ok"})





def viewdef_address_user(request):
    lid=request.POST['lid']

    var=DeliveryAddress.objects.filter(LOGIN_id=lid)
    if var.exists():
        var=var[0]
        print(var)
        return JsonResponse({'status': 'ok', 'id':var.id,'name': var.name, 'ph_no': var.ph_no,
                                                  'place':var.place,
                                                  'post':var.post,
                                                  'pin':var.pin,
                                                  'city':var.city,
                                                  'landmark':var.landmark,
                                                  'district':var.district})

        # cartl.append({'id': i.id,
        #               'plant_name': i.PLANT.plant_name,
        #               # 'scientific_name':i.scientific_name,
        #               'quantity': str(i.quantity),
        #               # 'plant_type':i.plant_type,
        #               'photo': i.PLANT.photo,
        #               'price': str(float(i.PLANT.price) * float(i.quantity)),
        #               'n': n,
        #               's': curstock,
        #               'q': q
        #               })


    # return JsonResponse({'status': 'ok', 'name': '', 'ph_no': '',
    #                                           'place':'',
    #                                           'post':'',
    #                                           'pin':'',
    #                                           'city':'',
    #                                           'landmark':'',
    #                                           'district':''})




def editaddress_user(request):
    aid=request.POST['aid']
    name = request.POST['name']
    ph_no = request.POST['ph_no']
    place = request.POST['place']
    city = request.POST['city']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    landmark = request.POST['landmark']
    # lid = request.POST['lid']

    obj = DeliveryAddress.objects.get(id=aid)
    obj.name = name
    obj.ph_no = ph_no
    obj.place = place
    obj.city = city
    obj.post = post
    obj.pin = pin
    obj.district = district
    obj.landmark = landmark
    obj.save()


    return JsonResponse({'status':"ok"})


def viewassigned_delboy(request):
     lid = request.POST['lid']
     var = Assigned_order.objects.filter(DELIVERY__LOGIN_id=lid,status="Assigned")
     l = []
     for i in var:
         l.append({
             'id': i.id,
             'oid': i.ORDERMAIN.id,
               'name': i.ORDERMAIN.ADDRESS.name,
               # 'scientific_name':i.scientific_name,
               'ph_no':i.ORDERMAIN.ADDRESS.ph_no,
               'place': i.ORDERMAIN.ADDRESS.place,
               'post': i.ORDERMAIN.ADDRESS.post,
               'city': i.ORDERMAIN.ADDRESS.city,
               'pin': i.ORDERMAIN.ADDRESS.pin,
               'district': i.ORDERMAIN.ADDRESS.district,
               'landmark': i.ORDERMAIN.ADDRESS.landmark
                   })

     return JsonResponse({'status': "ok", "data": l})

def del_editdeldate(request):
    oid=request.POST['oid']
    date=request.POST['date']
    var=Plant_ordermain.objects.filter(id=oid).update(deldate=date)

    return JsonResponse({'status':"ok"})

def del_updatestatus(request):
    id=request.POST['id']
    oid=request.POST['oid']
    from datetime import datetime
    date=datetime.now().strftime('%Y-%m-%d')
    res=Assigned_order.objects.filter(id=id).update(status='Delivered')
    obj= Plant_ordermain.objects.filter(id=oid).update(status='Delivered',deldate=date)
    return JsonResponse({'status': "ok"})


def view_deliveredorder(request):
    lid = request.POST['lid']
    var = Assigned_order.objects.filter(DELIVERY__LOGIN_id=lid, status="Delivered")
    l = []
    for i in var:
        l.append({
            'id': i.id,
            'oid': i.ORDERMAIN.id,
            'name': i.ORDERMAIN.ADDRESS.name,
            # 'scientific_name':i.scientific_name,
            'ph_no': i.ORDERMAIN.ADDRESS.ph_no,
            'place': i.ORDERMAIN.ADDRESS.place,
            'post': i.ORDERMAIN.ADDRESS.post,
            'city': i.ORDERMAIN.ADDRESS.city,
            'pin': i.ORDERMAIN.ADDRESS.pin,
            'district': i.ORDERMAIN.ADDRESS.district,
            'landmark': i.ORDERMAIN.ADDRESS.landmark
        })

    return JsonResponse({'status': "ok", "data": l})


# landmark=''
    # city=''
    # if DeliveryAddress.objects.filter(LOGIN_id=lid).exists():
    #     landmark=DeliveryAddress.objects.filter(LOGIN_id=lid).last().landmark
    #     city=DeliveryAddress.objects.filter(LOGIN_id=lid).last().city
    # return JsonResponse({'status':'ok','name':var.name,'ph_no':var.ph_no,
    #                      'place':var.place,
    #                      'post':var.post,
    #                      'pin':var.pin,
    #                      'city':var.city,
    #                      'landmark':var.landmark,
    #                      'district':var.district})


def viewdef_alladdress_user(request):
    lid=request.POST['lid']
    var=DeliveryAddress.objects.filter(LOGIN_id=lid)
    l=[]
    for i in var:
        l.append({'id':i.id,'name':i.name,'ph_no':i.ph_no,
                         'place':i.place,
                         'post':i.post,
                         'pin':i.pin,
                         'city':i.city,
                         'landmark':i.landmark,
                         'district':i.district})
    return JsonResponse({'status': "ok", "data": l})
#
# def viewdef_alladdress_user(request):
#     sid=request.POST['sid']
#     var=DeliveryAddress.objects.filter(LOGIN_id=sid)
#     l=[]
#     for i in var:
#         l.append({'id':i.id,'name':i.name,'ph_no':i.ph_no,
#                          'place':i.place,
#                          'post':i.post,
#                          'pin':i.pin,
#                          'city':i.city,
#                          'landmark':i.landmark,
#                          'district':i.district})
#     return JsonResponse({'status': "ok", "data": l})


def plantshop_vieworders(request):
    var=Plant_ordermain.objects.filter(SHOP__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request,"Plant Shop/vieworders.html",{'data':var})
#
# def plantshop_vieworders_post(request):
#     fromdate=request.POST['fdate']
#     todate=request.POST['tdate']
#     search = request.POST['Filter']
#
#     if search == '':
#         res = Shop.objects.filter(status='pending', shop_name__icontains=search)
#     elif status == 'None':
#         res = Shop.objects.filter(status='Pending', shop_name__icontains=search)
#     else:
#         var = Plant_ordersub.objects.filter(PLANT_ORDERMAIN__SHOP__LOGIN_id=request.session['lid'],
#                                             PLANT_ORDERMAIN__date__range=[fromdate, todate],
#                                             PLANT_ORDERMAIN__status__icontains=search)
#
#     return render(request, "Plant Shop/vieworders.html", {'data': var})






from django.db.models import Q

def plantshop_vieworders_post(request):
    fromdate = request.POST['fdate']
    todate = request.POST['tdate']
    search = request.POST['search']

    if search == '':
        # If search field is empty, only filter by date range
        var = Plant_ordermain.objects.filter(
            SHOP__LOGIN_id=request.session['lid'],
            date__range=[fromdate, todate],
        )
    elif fromdate and todate:
        # If search field is not empty and dates are specified, filter by both
        var = Plant_ordermain.objects.filter(
            SHOP__LOGIN_id=request.session['lid'],
            date__range=[fromdate, todate],
            status__icontains=search,
        )
    else:
        # If only search field is specified
        var = Plant_ordermain.objects.filter(
            PLANT_ORDERMAIN__SHOP__LOGIN_id=request.session['lid'],
            PLANT_ORDERMAIN__status__icontains=search,
        )

    return render(request, "Plant Shop/vieworders.html", {'data': var})



def plantshop_vieworders_more(request,id):
    var=Plant_ordersub.objects.filter(PLANT_ORDERMAIN_id=id,PLANT_ORDERMAIN__SHOP__LOGIN_id=request.session['lid'])
    return render(request,"Plant Shop/order_moredetails.html",{'data':var})




def plantshop_vieworders_more_post(request):
    var=Plant_ordersub.objects.filter(PLANT_ORDERMAIN__SHOP__LOGIN_id=request.session['lid'])
    return render(request,"Plant Shop/order_moredetails.html",{'data':var})

def plantshop_assigndel(request,id):
    dist=Plant_ordermain.objects.get(id=id).ADDRESS.district
    place=Plant_ordermain.objects.get(id=id).ADDRESS.place

    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.geocode(place+","+ dist)
    print(location.latitude, location.longitude,"hellooooooooooooooooooooooooooo")


    l1=(location.latitude, location.longitude)


    var=DeliveryBoy.objects.filter(status="Approved")

    ls=[]

    for i in var:
        geolocator = Nominatim(user_agent="myapp")

        print(i.place , i.district ,""+ i.name)
        location2 = geolocator.geocode(i.place + "," + i.district)

        l2 = (location2.latitude, location2.longitude)

        dist= geodesic(l1, l2).km


        ls.append({ 'd': i ,'dist': dist})

    print(ls)

    for i in range(0,len(ls)):


        for j in range(0,len(ls)):

            print(ls[i],"Hellooooooooooooooooooooooooooo",ls[j])

            if ls[i]['dist']< ls[j]['dist']:

                temp=  ls[i]
                ls[i]= ls[j]
                ls[j]= temp







    return render(request, "Plant Shop/assign_delivery.html", {'data': ls,'id':id})

def plantshop_assigndel_post(request):
    DeliveryBoy=request.POST['select']



    o_id=request.POST["o_id"]
    var=Assigned_order()
    var.DELIVERY_id=DeliveryBoy
    var.ORDERMAIN_id=o_id
    from datetime import datetime
    var.date=datetime.now().today()
    var.status="Assigned"
    var.save()


    a=Plant_ordermain.objects.filter(id=o_id).update(status='Assigned')


    return HttpResponse('''<script>alert('Ok');window.location='/myapp/plantshop_vieworders/'</script>''')


#public
def public_viewoneplant(request):
    pid=request.POST['pid']
    var=Plant.objects.get(id=pid)
    return JsonResponse({'status': "ok","id":var.id,
                         "plant_name":var.plant_name,
                         "scientific_name":var.scientific_name,
                         "size":var.size,
                         "plant_type":var.plant_type,
                         "photo":var.photo,
                         "price":var.price,
                         "details":var.details
                         })


def user_viewmyorder(request):
    lid=request.POST['lid']
    var = Payment.objects.filter(PLANT_ORDERMAIN__USER__LOGIN_id=lid).order_by('-id')
    l = []
    for i in var:
        l.append({'id': i.id,
                  'shop_name': i.PLANT_ORDERMAIN.SHOP.shop_name,
                  'place':i.PLANT_ORDERMAIN.SHOP.place,
                  'ph_no':i.PLANT_ORDERMAIN.SHOP.ph_no,
                  'date':i.PLANT_ORDERMAIN.date,
                  'date2':i.PLANT_ORDERMAIN.deldate,
                  'photo': i.PLANT_ORDERMAIN.SHOP.photo,
                   'total_amount':i.PLANT_ORDERMAIN.amount,
                   'status':i.PLANT_ORDERMAIN.status,

                  # 'details':i.details
                  })
    return JsonResponse({'status': "ok", "data": l})

def user_viewmyordermore(request):
    oid=request.POST['oid']
    var = Plant_ordersub.objects.filter(PLANT_ORDERMAIN_id=oid)
    l = []
    for i in var:
        l.append({'id': i.id,
                  'plant_name': i.PLANT.plant_name,
                  'quantity':i.quantity,
                  'price': str(float(i.PLANT.price) * float(i.quantity)),

                  'photo': i.PLANT.photo,

                  })
    return JsonResponse({'status': "ok", "data": l})

def user_cancelmyorder(request):
    oid=request.POST['oid']
    Plant_ordermain.objects.filter(id=oid).update(status='canceled')
    return JsonResponse({'status': "ok" })

def add_plantreview(request):
    rating = request.POST['rating']
    review = request.POST['review']

    from datetime import  datetime

    lid=request.POST['lid']
    sid=request.POST['sid']

    c = Plantreview()
    c.USER=User.objects.get(LOGIN_id=lid)
    c.SHOP_id=sid
    c.rating=rating
    c.review=review
    c.date=datetime.now()
    c.save()


    return JsonResponse({'status':"ok"})



def add_petreview(request):
    rating = request.POST['rating']
    review = request.POST['review']

    from datetime import  datetime

    lid=request.POST['lid']
    sid=request.POST['sid']

    c = Plantreview()
    c.USER=User.objects.get(LOGIN_id=lid)
    c.SHOP_id=sid
    c.rating=rating
    c.review=review
    c.date=datetime.now()
    c.save()


    return JsonResponse({'status':"ok"})



def userpet_viewmyorder(request):
    lid=request.POST['lid']
    var = Pet_ordermain.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in var:
        l.append({'id': i.id,
                  'shop_name': i.SHOP.shop_name,
                  'place':i.SHOP.place,
                  'ph_no':i.SHOP.ph_no,
                  'date':i.date,
                  'date2':i.date,
                  'photo': i.SHOP.photo,
                   'total_amount':'100'
                  # 'details':i.details
                  })
    return JsonResponse({'status': "ok", "data": l})

def userpet_viewmyordermore(request):
    oid=request.POST['oid']
    var = Pet_ordersub.objects.filter(PET_ORDERMAIN_id=oid)
    l = []
    for i in var:
        l.append({'id': i.id,
                  'pet_name': i.PET.pet_name,
                  'quantity':i.quantity,
                  'price': str(float(i.PET.price) * float(i.quantity)),

                  'photo': i.PET.photo,

                  })
    return JsonResponse({'status': "ok", "data": l})

def user_viewreviews(request):
    sid=request.POST['sid']
    var =Plantreview.objects.filter(SHOP_id=sid)
    l=[]
    for i in var:
        l.append({'id':i.id,'name':i.USER.name,'date':i.date,'review':i.review,'rating':i.rating})

    return JsonResponse({'status': "ok", "data": l})


#disease prediction


def upload_file(request):
    photo = request.POST['photo']

    import datetime
    import base64

    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh = open("C:\\Users\\minha\\PycharmProjects\\petplantshop\\media\\" + date + ".jpg", "wb")
    fh.write(a)
    fh.close()

    from myapp.classify import check
    pred = check("C:\\Users\\minha\\PycharmProjects\\petplantshop\\media\\" + date + ".jpg")
    # print(type(pred))
    # print(pred)
    return JsonResponse({"status": "ok", "name": str(pred[0])})


#
# #bill generation

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


def generate_bill_pdf(date, user_name, user_phone, products, total_amount,bill_id):
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    company_heading_style = ParagraphStyle(
        name='CompanyHeading',
        parent=styles['Heading1'],  # Inherit from an existing style if needed
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold',  # Specify font name and bold
        fontSize=18,  # Specify font size
    )
    company_heading_style1 = ParagraphStyle(
        name='CompanyHeading',
        parent=styles['Heading4'],  # Inherit from an existing style if needed
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold',  # Specify font name and bold
        fontSize=13,  # Specify font size
    )
    company_bill = ParagraphStyle(
        name='CompanyHeading',
        parent=styles['Heading4'],  # Inherit from an existing style if needed
        alignment=2,  # Center alignment
        fontName='Helvetica-Bold',  # Specify font name and bold
        fontSize=10,  # Specify font size
    )
    company_message = ParagraphStyle(
        name='CompanyHeading',
        parent=styles['Heading4'],  # Inherit from an existing style if needed
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold',  # Specify font name and bold
        fontSize=10,  # Specify font size
    )


    line1 = Paragraph("---------------------------------------------------------------------------", company_heading_style)
    company_heading = Paragraph("<b><font color='Green'> GreenPaws! </font></b>", company_heading_style)
    # company_heading.alignment = 1

    bill_subheading = Paragraph("<b>Online Pet-Plant Hub</b>", company_heading_style1)
    # bill_subheading.alignment = 1
    line2= Paragraph("---------------------------------------------------------------------------",
                      company_heading_style)

    bill_id= Paragraph(f"Bill No:{bill_id}", company_bill)
    # bill_subheading.alignment = 2

    customer_info= Paragraph(f"Name  : {user_name}", styles['Heading4'])
    # customer_info.alignment = 3

    customer_phone = Paragraph(f"Phone : {user_phone}", styles['Heading4'])
    # customer_phone.alignment = 3.5



    data = [["Sl.no", "Date", "Shop Name","Product Name", "Quantity", "Price"]]
    for i, product in enumerate(products, start=1):
        row = [i,product['date'],product['shop'], product['name'],  product['quantity'], f"Rs:{product['price']}"]
        data.append(row)

    table = Table(data, colWidths=[30, 100, 100, 100, 60], rowHeights=30)  # Adjusted colWidths to fit quantity and price
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    spacer = Spacer(1, 20)

    total_text = Paragraph("<b>Total Amount:</b> Rs:{}".format(total_amount), styles['Normal'])
    total_text.alignment = 2

    thank_you_message = Paragraph("<b>Thank you for choosing <i>GreenPaws</i> for your pet and plant needs!. Visit again....</b>",
                                  company_message)
    thank_you_message.alignment = 1
    line = Paragraph("---------------------------------------------------------------------------", company_heading_style)


    flowables = [line1,company_heading, bill_subheading,line2, spacer,bill_id ,spacer,customer_info,customer_phone, spacer, table, spacer, total_text,
                 spacer,spacer, thank_you_message,spacer,line]
    document.build(flowables)

    buffer.seek(0)
    return buffer


def generate_pdf_bill_payment(request, pid):
    print(pid)
    products = []
    try:
        psub = Plant_ordersub.objects.filter(PLANT_ORDERMAIN_id=pid)
        total_amount = 0
        osub = Plant_ordermain.objects.get(id=pid)
        date = osub.date
        shop_name = osub.SHOP.shop_name
        user_name = osub.USER.name
        user_phone = osub.USER.ph_no
        bill_id = osub.id
        for payment in psub:
            product_name = payment.PLANT.plant_name
            # product_name = payment.quantity
            price = payment.PLANT.price
            # material = payment.DRESSMATERIAL.material
            amount = payment.PLANT_ORDERMAIN.amount

            quantity = payment.quantity

            products.append({'shop':shop_name,'name': product_name,'date':date, 'price': price, 'quantity': quantity})
            total_amount += float(price) * int(quantity)
            # total_amount += float(amount) * int(quantity)

        print(total_amount, 'ttttttttt')

        buffer = generate_bill_pdf(date, user_name, user_phone, products, total_amount, bill_id)

        fs = FileSystemStorage()
        filename = f"bill_{pid}.pdf"
        file_path = fs.save('bills/' + filename, buffer)

        # psub.update(billfle = fs.url('bills/' + filename))
        # payment.save()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())
        return response

    except Plant_ordersub.DoesNotExist:
        return HttpResponse("Payment does not exist")





















def user_generate_pdf_bill_payment(request):
    pid=request.POST['pid']
    print(pid)
    products = []
    try:
        psub = Plant_ordersub.objects.filter(PLANT_ORDERMAIN_id=pid)
        total_amount = 0
        osub = Plant_ordermain.objects.get(id=pid)
        date = osub.date
        shop_name = osub.SHOP.shop_name
        user_name = osub.USER.name
        user_phone = osub.USER.ph_no
        bill_id = osub.id
        for payment in psub:
            product_name = payment.PLANT.plant_name
            # product_name = payment.quantity
            price = payment.PLANT.price
            # material = payment.DRESSMATERIAL.material
            amount = payment.PLANT_ORDERMAIN.amount

            quantity = payment.quantity

            products.append({'shop':shop_name,'name': product_name,'date':date, 'price': price, 'quantity': quantity})
            total_amount += float(price) * int(quantity)
            # total_amount += float(amount) * int(quantity)

        print(total_amount, 'ttttttttt')

        buffer = generate_bill_pdf(date, user_name, user_phone, products, total_amount, bill_id)

        fs = FileSystemStorage()
        filename = f"bill_{pid}.pdf"
        file_path = fs.save('bills/' + filename, buffer)

        # psub.update(billfle = fs.url('bills/' + filename))
        # payment.save()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())
        # return response
        return JsonResponse({'status':'ok'})

    except Plant_ordersub.DoesNotExist:
        # return HttpResponse("Payment does not exist")
        return JsonResponse({'status':'no'})




#cirtificate generation

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


# def generate_bill_pdf(date, user_name, user_phone, products, total_amount,bill_id):
#     buffer = BytesIO()
#     document = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#
#     company_heading_style = ParagraphStyle(
#         name='CompanyHeading',
#         parent=styles['Heading1'],
#         alignment=1,
#         fontName='Helvetica-Bold',
#         fontSize=20,
#     )
#     company_heading_style1 = ParagraphStyle(
#         name='CompanyHeading',
#         parent=styles['Heading2'],
#         alignment=1,
#         fontName='Helvetica-Bold',
#         fontSize=15,
#     )
#     company_subheading_style = ParagraphStyle(
#         name='CompanySubHeading',
#         parent=styles['Normal'],
#         alignment=1,
#         fontName='Helvetica',
#         fontSize=12,
#         spaceAfter=10
#     )
#     content_style = ParagraphStyle(
#         name='Content',
#         parent=styles['Normal'],
#         alignment=0,
#         fontName='Helvetica',
#         fontSize=12,
#         leading=15,
#
#     )
#     sign_style = ParagraphStyle(
#         name='Content',
#         # parent=styles['Normal'],
#         # alignment=0,
#         # fontName='Helvetica',
#         fontSize=12,
#         leading=15,
#
#         parent=styles['Heading4'],  # Inherit from an existing style if needed
#         alignment=2,  # Center alignment
#         fontName='Helvetica-Bold',  # Specify font name and bold
#
#     )
#     line3= Paragraph(
#         "------------------------------------------------------------------------------------------------------------------",
#         content_style)
#     # cer_heading4 = Paragraph("<b>കേരള സർക്കാർ</b>", company_heading_style)
#     cer_heading1 = Paragraph("<b>GOVERNMENT OF KERALA</b>", company_heading_style1)
#     cer_heading2 = Paragraph("<b>DEPARTMENT OF PANCHAYAT</b>", company_heading_style1)
#
#     cer_subheading1 = Paragraph(
#         "<b>Name of Local Government issuing certificate:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Payam Grama Panchayat</b>",
#         company_subheading_style)
#
#     cer_heading3 = Paragraph("<b> DEATH CERTIFICATE </b>", company_heading_style)
#     caption = Paragraph("(Issued under Section 12 of the Registration of Births and Deaths Acts, 1969 and Rule 8 of the Kerala Registration of Births and Deaths Rules, 1999)", content_style)
#
#     # cer_subheading = Paragraph("<b>This Certificate shows that</b>", company_subheading_style)
#     # content = Paragraph("<b><u>{Name}</u></b> Sex <b><u>Female</u> </b> was born at <b><u>{hospital}</u></b> in Keralaon the <b><u>{date}</u></b> day of<b> <u>{month ,year}</u></b> and that the parents names are as follows:", content_style)
#     caption2 = Paragraph(
#         "(This is to certify that the following informatid has been taken from the original record of death which is the register for (local area/local body) Payam Grama Panchayat of Taluk Kannur of District Kannur of State Kerala.)",
#         content_style)
#     name = Paragraph("Name       <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {name}</b>", content_style)
#     sex = Paragraph("Sex       <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {Sex}</b>", content_style)
#     death_date= Paragraph("Date of Death       <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {Date of Death}</b>", content_style)
#     place_date= Paragraph("Place of Death  <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {Place of Death}</b>", content_style)
#     mother_name = Paragraph("Name of Mother       <b>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {mother name}</b>", content_style)
#     father_name= Paragraph(" Name of Father/Husband       <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {father name/husband}</b>", content_style)
#     c_address= Paragraph(" Address of the deceased <br/>at the time of death     <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {current address}</b>", content_style)
#     p_address= Paragraph(" permanent address of <br/>deceased     <b>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {permanent address}</b>", content_style)
#     Registration_no= Paragraph(" Registration Number     <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {Registration number}</b>", content_style)
#     Registration_date= Paragraph(" Date of Registration      <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {Date of Registration}</b>", content_style)
#
#
#     # line=Paragraph("------------------------------------------------------------------------------------------------------------------",content_style)
#     # date1= Paragraph("Date  of Issue :&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Address of the issuing Athority: <b> <br/>{Date}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Registrar of  Births and Deaths,<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Payam Grama Panchayat</b>", content_style)
#     # date1= Paragraph("Date  of Issue : {Date}", content_style)
#     date1 = Paragraph("<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Date  of Issue &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {Date}</b>", content_style)
#     # signature = Paragraph("Address of the issuing Athority <b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : Registrar of  Births and Deaths, <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Payam Grama Panchayat  </b>", content_style)
#     line2 = Paragraph(
#         "------------------------------------------------------------------------------------------------------------------",
#         content_style)
#     #
#     flowables = [line3,Spacer(1, 12),cer_heading1,Spacer(1, 12), cer_heading2,Spacer(1, 12),cer_subheading1,Spacer(1, 12), cer_heading3,caption,Spacer(1, 20),caption2, Spacer(1, 60),Spacer(1, 12),name,Spacer(1, 12),sex,Spacer(1, 12),death_date,Spacer(1, 12),place_date,Spacer(1, 12),mother_name,Spacer(1, 12), father_name,Spacer(1, 12),c_address,Spacer(1, 12),p_address,Spacer(1, 12),Registration_no,Spacer(1, 12),Registration_date,Spacer(1, 12),date1,Spacer(1, 12),Spacer(1, 12),line2]
#     # flowables = [cer_heading1,cer_heading2,cer_heading3, bill_subheading,bill_subheading1,bill_subheading2,bill_subheading3, spacer,bill_id,signature ,spacer,customer_info, spacer, table, spacer, total_text,
#     #              spacer,spacer, thank_you_message]
#     document.build(flowables)
#
#     buffer.seek(0)
#     return buffer


def generate_pdf_bill_payment(request, pid):
    print(pid)
    products = []
    try:
        psub = Plant_ordersub.objects.filter(PLANT_ORDERMAIN_id=pid)
        total_amount = 0
        osub = Plant_ordermain.objects.get(id=pid)
        date = osub.date
        shop_name = osub.SHOP.shop_name
        user_name = osub.USER.name
        user_phone = osub.USER.ph_no
        bill_id = osub.id
        for payment in psub:
            product_name = payment.PLANT.plant_name
            # product_name = payment.quantity
            price = payment.PLANT.price
            # material = payment.DRESSMATERIAL.material
            amount = payment.PLANT_ORDERMAIN.amount

            quantity = payment.quantity

            products.append({'shop':shop_name,'name': product_name,'date':date, 'price': price, 'quantity': quantity})
            total_amount += float(price) * int(quantity)
            # total_amount += float(amount) * int(quantity)

        print(total_amount, 'ttttttttt')

        buffer = generate_bill_pdf(date, user_name, user_phone, products, total_amount, bill_id)

        fs = FileSystemStorage()
        filename = f"bill_{pid}.pdf"
        file_path = fs.save('bills/' + filename, buffer)

        # psub.update(billfle = fs.url('bills/' + filename))
        # payment.save()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())
        return response

    except Plant_ordersub.DoesNotExist:
        return HttpResponse("Payment does not exist")





















def user_generate_pdf_bill_payment(request):
    pid=request.POST['pid']
    print(pid)
    products = []
    try:
        psub = Plant_ordersub.objects.filter(PLANT_ORDERMAIN_id=pid)
        total_amount = 0
        osub = Plant_ordermain.objects.get(id=pid)
        date = osub.date
        shop_name = osub.SHOP.shop_name
        user_name = osub.USER.name
        user_phone = osub.USER.ph_no
        bill_id = osub.id
        for payment in psub:
            product_name = payment.PLANT.plant_name
            # product_name = payment.quantity
            price = payment.PLANT.price
            # material = payment.DRESSMATERIAL.material
            amount = payment.PLANT_ORDERMAIN.amount

            quantity = payment.quantity

            products.append({'shop':shop_name,'name': product_name,'date':date, 'price': price, 'quantity': quantity})
            total_amount += float(price) * int(quantity)
            # total_amount += float(amount) * int(quantity)

        print(total_amount, 'ttttttttt')

        buffer = generate_bill_pdf(date, user_name, user_phone, products, total_amount, bill_id)

        fs = FileSystemStorage()
        filename = f"bill_{pid}.pdf"
        file_path = fs.save('bills/' + filename, buffer)

        # psub.update(billfle = fs.url('bills/' + filename))
        # payment.save()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())
        # return response
        return JsonResponse({'status':'ok'})

    except Plant_ordersub.DoesNotExist:
        # return HttpResponse("Payment does not exist")
        return JsonResponse({'status':'no'})


def purchase_details(request):
    var=Plant_cart.objects.all()
