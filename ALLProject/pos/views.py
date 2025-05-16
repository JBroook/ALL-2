from django.shortcuts import render

# Create your views here.
def cashierPOSView(request):
    return render(request, 'pos/sales_page.html')

def cashierHistoryView(request):
    return render(request,'pos/view_history.html')