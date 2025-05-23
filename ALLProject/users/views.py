from django.shortcuts import render

# Create your views here.
def user_list_view(request):
    return render(request, 'users/user_list.html')