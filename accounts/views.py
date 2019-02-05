from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from accounts.forms import CustomChurchCreationForm
# Create your views here.


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def add_new_church(request):
    
    if request.method == 'POST':
        form = CustomChurchCreationForm(request.POST)
        print("############:  form created")

        if form.is_valid():
            print("############# It's Valid PAPA")
            form.save()
            return redirect('dashboard')
    else:
        form = CustomChurchCreationForm()
        return render(request, 'new_church.html', {'form':form})
        
        
def login_view(request):
    pass




def logout_view(request):
    pass