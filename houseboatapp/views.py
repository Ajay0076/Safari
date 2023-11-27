import email
from django.shortcuts import render, redirect
from django.db.models import Max
from houseboatapp.models import Registration,Login,Addboat
from django.core.files.storage import FileSystemStorage


# from django.http import HttpResponse

# Create your views here.




def adminhome(request):
    return render(request, 'adminhome.html')


def user_home(request):
    return render(request, './houseboatapp/user_home.html')


def registration(request):
    return render(request, './houseboatapp/registration.html')


def homepage(request):
    return render(request, './houseboatapp/index.html')


def addrooms(request):
    return render(request, './houseboatapp/addboats.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Registration.objects.filter(email=email,password=password,usertype="A"):
            a=Registration.objects.get(email=email,password=password,usertype="A")
            # for i in a:
            #     y = i.id
            #     request.session['id'] =y
            #     request.session['first_name']=first_name
            print(type(a))
            request.session["uid"] = a.reg_id

            print(request.session["uid"])

            return render(request, "./houseboatapp/adminhome.html")
        elif Registration.objects.filter(email=email, password=password, usertype="user"):
            a= Registration.objects.get(email=email, password=password, usertype="user")
            print(a.reg_id)

            request.session['uid'] =a.reg_id
            request.session['email'] = email
            # last_name = {'last_name': request.session['last_name']}
            return render(request, "./houseboatapp/user_home.html")
        else:
            return render(request, "./houseboatapp/invalid.html")

    return render(request, "./houseboatapp/login.html")





def addboat(request):
    if request.method == 'POST':
        a=request.session['uid']

        u_file = request.FILES['image']
        fs = FileSystemStorage()
        path = fs.save(u_file.name, u_file)

        p = request.POST.get('boat_type')
        d = request.POST.get('boat_name')
        pr = request.POST.get('rate')
        q = request.POST.get('discription')
        z = request.POST.get('phone')
        w = request.POST.get('location')

        pd = Addboat(id=a,image=path,boat_type=p, boat_name=d, rate=pr, discription=q, phone=z,location=w)
        pd.save()

        context = {'msg': 'houseboat added'}
        return render(request, './houseboatapp/adminhome.html', context)

    else:
        return render(request, './houseboatapp/addboats.html')


def logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return login(request)
    else:
        return login(request)


# def registration(request):
# return render(request,'./products/registration.html')


def registration(request):
    if request.method == "POST":
        a = request.POST.get('fname')
        b = request.POST.get('lname')
        c = request.POST.get('email')
        d = request.POST.get('phone')
        e = request.POST.get('password')
        f = request.POST.get('usertype')

        un = c
        pwd = e
        ul = Login(username=un, password=pwd)
        ul.save()
        user_id = Login.objects.all().aggregate(Max('id'))['id__max']


        ab = Registration(reg_id=user_id, first_name=a, last_name=b, email=c, phone=d, password=e,usertype=f)
        ab.save()

        msg = {'msg': 'User Registered'}
        return render(request, "./houseboatapp/login.html", msg)
    else:
        return render(request, "./houseboatapp/registration.html")


def profile(request):
    single = Registration.objects.filter(id=request.session['user_id'])
    context = {'details': single}
    return render(request, './houseboatapp/profile.html', context)

def viewboats(request):
    a=request.session["uid"]
    viewboats = Addboat.objects.filter(id=a)
    vp = {'details': viewboats}
    return render(request, './houseboatapp/viewboats.html' ,vp)

def updateboats(request,boat_id):
    if request.method == 'POST':
        boat_name = request.POST.get('boat_name')
        boat_type = request.POST.get('boat_type')
        rate = request.POST.get('rate')
        discription = request.POST.get('discription')
        phone = request.POST.get('phone')
        location=request.POST.get('location')
        up = Addboat.objects.get(boat_id=boat_id)
        up.boat_name = boat_name

        up.rate = rate
        up.discription = discription
        up.phone=phone
        up.location=location
        up.save()
        msg = 'houseboat updated'
        up_l = Addboat.objects.all()
        context = {'details': up_l, 'msg': msg}
        return redirect('http://127.0.0.1:8000/viewboats',context)
    else:

        up = Addboat.objects.get(boat_id=boat_id)
        context={'up':up}
        return render(request, './houseboatapp/updateboat.html',context)

def deleteboat(request,boat_id):
    a = Addboat.objects.get(boat_id=boat_id)
    a.delete()
    return redirect('http://127.0.0.1:8000/viewboats')

def about(request):
    return render(request, './houseboatapp/About.html')

def userboat(request):
    viewboat = Addboat.objects.all()
    vp = {'details': viewboat}
    return render(request, './houseboatapp/boats.html',vp)
def updateprofile(request):
    if request.method == 'POST':
        reg_id = request.session['uid']
        up = Registration.objects.get(reg_id=reg_id)

        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('contact')

        up.first_name = first_name
        up.last_name = last_name
        up.email = email
        up.phone = phone

        up.save()

        context = {'msg': 'User Details Updated', 'up': up}
        return render(request, './houseboatapp/updateprofile.html', context)

    else:
        reg_id = request.session['uid']
        up = Registration.objects.get(reg_id=reg_id)
        context = {'up': up}
        return render(request, './houseboatapp/updateprofile.html', context)
