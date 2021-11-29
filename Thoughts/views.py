
from . import models

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
import datetime

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard.html', {})



def dashboard_view(request):
    u = models.CustUser.objects.get(id=request.user.id)
    print(u,"user")
    app_title=''
    title=''
    is_dashboard=True

    return render(request, 'dashboard_view.html', {'u':u,'app_title':app_title,'title':title,'is_dashboard':is_dashboard})

def profile(request):
    u = models.CustUser.objects.get(id=request.user.id)
    print(u,"user")
    return render(request, 'profile.html', {'u':u})




def login_view(request):
    error_msg = ""


    if request.method == "POST":
        username = request.POST['username']

        password = request.POST['password']
        print(username,password,"uuuuuuu")
        try:
            username = models.CustUser.objects.get(username__iexact=username)
            print(username,"iiiii")
        except Exception as e:
            print(e)

        user = authenticate(username=username, password=password)
        print(user, "user")
        if user is None:
            try:
                username = models.CustUser.objects.get(email__iexact=username)
                user = authenticate(username=username, password=password)
            except Exception as e:
                print(e)

        if user is not None:

            print("successfully logged in")
            login(request, user)

            try:

                ins = models.CustUser.objects.get(username=user)
                request.session['user_id'] = ins.id
                print(request.session['user_id'], "session")


                if user.is_staff:
                    return redirect("dashboard_view")
            except Exception as e:
                print(e)


            return redirect("dashboard_view")

        else:
            error_msg = "Incorrect Username or Password"



    return render(request, 'login.html', {'error_msg': error_msg})


def logout_view(request):
    logout(request)
    return redirect("login")



def signup(request):

    error_message = None


    if request.method == "POST" and "create_admin" in request.POST:

        if request.POST['username'] == "" and error_message is None:
            error_message = " Please enter a valid username"
        else:
            if models.CustUser.objects.filter(
                            username__iexact=request.POST.get('username')).exists() and error_message is None:
                error_message = "Username already exists, please try another"
            else:
                user_name = request.POST['username']
                print(user_name,"username")
        if request.POST['email'] == "" and error_message is None:
            error_message = " Please enter a valid email"
        else:
            if models.CustUser.objects.filter(
                            email__iexact=request.POST.get('email')).exists() and error_message is None:
                error_message = "Email already exists, please try another"
            else:
                email = request.POST.get('email')
                print(email, "email")
        if error_message is None and request.POST['password'] == "":
            error_message = " Please enter a valid password"
        else:
            password = request.POST.get('password')
            print(password, "password")
        # if request.FILES.get('image') is None and error_message is None:
        #     error_message = " Please provide a valid file"
        # else:

        image = request.FILES['logo']

        print(image, "image")

        # image = request.FILES['image']

        if error_message is None:
            user = models.CustUser.objects.create_superuser(username=user_name, password=password, email=email,
                                                                    logo=image)


            main = "User Successfully Registered"
            para = "Please Wait! We will be taking you back to Login Page "
            redirect_page = 'http://' + request.get_host() + ''

            return render(request, "msgsuccess.html",
                                {'main': main, 'para': para, 'redirect_page': redirect_page})


    return render(request, "signup.html", {'error_msg': error_message})


def events_view(request):
    event_page=''
    count=''
    events=''
    try:
        data = models.Thoughts.objects.all().order_by('id')
        print(data,"data")
        paginator = Paginator(data, 10)
        page = request.GET.get('page')
        event_page = paginator.get_page(page)
        count = len(data)
        u = models.CustUser.objects.get(id=request.user.id)
        print(u, "user")
        events = models.Thoughts.objects.order_by('endDate')
        print(events, "ttttttttttttttt")

        if request.method == 'POST' and 'published_id' in request.POST:
            published_id = request.POST.get('published_id')
            print(published_id,"published_id")
            user_details = models.Thoughts.objects.get(id=published_id)
            if user_details.published:
                user_details.published = False
                user_details.save()
            else:
                user_details.published = True
                user_details.save()

        if request.method == 'POST' and 'paid_id' in request.POST:
            paid_id = request.POST['paid_id']
            print(paid_id,"paid_id")
            user_details = models.Thoughts.objects.get(id=paid_id)
            if user_details.paid:
                user_details.paid = False
                user_details.save()
            else:
                user_details.paid = True
                user_details.save()


        if request.method == 'POST' and 'like_id' in request.POST:
            like_id = request.POST['like_id']
            print(like_id,"like_id")
            user_details = models.Thoughts.objects.get(id=like_id)
            if user_details.like:
                user_details.like = False
                user_details.save()
            else:
                user_details.like = True
                user_details.save()
    except Exception as e:
        print(e)


    return render(request, 'event_view.html',{'key': event_page,'count':count,'events':events})

def events_add(request):
    error_message=None
    u = models.CustUser.objects.get(id=request.user.id)
    print(u, "user")
    if request.method == 'POST' and 'submit' in request.POST:
        title=request.POST.get("event_title")
        print(title,"hhhhhhhhhhhhhh")
        startdate = request.POST.get('event_start_date')
        print(startdate,"startdate")
        endDate = request.POST.get('event_end_date')
        location = request.POST.get("event_location")

        category = request.POST.get("category")
        description = request.POST.get("event_description")
        # published = request.POST.get("event_published")
        # paid = request.POST.get("event_paid")
        image = request.FILES["image"]
        print(title,startdate,endDate,location,image, "title")
        obj = models.Thoughts()

        obj.title = title

        obj.startdate = startdate

        obj.endDate = endDate
        obj.location = location
        obj.description = description
        obj.category = category
        # obj.published = published
        # obj.paid = paid
        obj.image = image
        obj.userId = models.CustUser.objects.get(id=request.user.id)
        print(obj.userId,obj.image,"uuuuuuuuuu")
        obj.save()
        print("save")
        # if error_message is None:
        #     try:
        #         u=models.CustUser.objects.get(id=request.user.id)
        #         obj = models.Thoughts()
        #         Thought = request.POST.get("event_title")
        #         obj.title=Thought
        #         obj.userId = u
        #         print(obj.userId,"userid")
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #         obj.save()
        #     except Exception as e:
        #         print(e)
        # else:
        #     return render(request, 'event_add.html', {'error_message': error_message})
        return redirect("events_view")
    return render(request,"event_add.html",{'u':u})


