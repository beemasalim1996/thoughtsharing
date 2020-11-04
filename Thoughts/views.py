
from . import models

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout


# Create your views here.


def dashboard(request):
    return render(request, 'dashboard.html', {})



def dashboard_view(request):
    u = models.CustUser.objects.get(id=request.user.id)
    print(u,"user")
    return render(request, 'dashboard_view.html', {'u':u})

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


def thoughts_view(request):
    u = models.CustUser.objects.get(id=request.user.id)
    print(u, "user")
    thoughts = models.Thoughts.objects.order_by('-id')
    print(thoughts,"ttttttttttttttt")
    if request.method == 'POST' and 'like_id' in request.POST:
        like_id = request.POST['like_id']
        print(like_id,"like_id")
        user_details = models.Thoughts.objects.get(id=like_id)
        if user_details.ThoughtImportant:
            user_details.ThoughtImportant = False
            user_details.save()
        else:
            user_details.ThoughtImportant = True
            user_details.save()

    return render(request, 'thoughts_view.html', {'thoughts':thoughts,'u':u})

def thoughts_add(request):
    error_message=None
    u = models.CustUser.objects.get(id=request.user.id)
    print(u, "user")
    if request.method == 'POST' and "submit" in request.POST :

        Thought=request.POST.get("Thought")
        l=len(Thought)

        print(l,"lenght")
        if len(Thought) > 255:
            error_message = "Thought entered have more than 255 characters which is not allowed"

        else:
            error_message = None
        if error_message is None:
            try:
                u=models.CustUser.objects.get(id=request.user.id)
                obj = models.Thoughts()
                Thought = request.POST.get("Thought")
                obj.Thought=Thought
                obj.userId = u
                print(obj.userId,"userid")

                obj.save()
            except Exception as e:
                print(e)
        else:
            return render(request, 'thought_add.html', {'error_message': error_message})
        return redirect("thoughts_view")
    return render(request,"thought_add.html",{'u':u})


