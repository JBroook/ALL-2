from django.http import HttpResponse
from django.template import loader

# Create your views here.
def cashierPOSView(request):
    template = loader.get_template('pos/sales_page.html')
    context = {}
    return HttpResponse(template.render(context,request))

def cashierHistoryView(request):
    template = loader.get_template('pos/view_history.html')
    context = {}
    return HttpResponse(template.render(context,request))