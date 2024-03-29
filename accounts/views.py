from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


def register(request):
  # Register User
  if request.method == 'POST':
    # Get Form Values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # check password

    if password == password2:
        # check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That Username Is Taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.success(request, 'That Email Is Being Used')
          return redirect("register")
        else:
          # New Entry Added
          user = User.objects.create_user(username=username,password=password,
                                          email=email,first_name=first_name,last_name=last_name)

          # save the data into database
          user.save()
          messages.error(request, 'you are now registered and login')
          return redirect('login')

    else:
      messages.error(request,'Passwords Are Not Match')
      return redirect('register')
  else:
    return render(request,'accounts/register.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    if user is not None:
      auth.login(request, user)
      messages.success(request, "You are now loged in")
      return redirect('dashboard')
    else:
      messages.error(request, "Invalid credentials")
      return redirect('login')
  return render(request,'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, "You are now logout")
  return redirect('index')

def dashboard(request):
  user_contacts= Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts': user_contacts
  }
  return render(request,'accounts/dashboard.html', context)