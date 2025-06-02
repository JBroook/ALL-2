from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render

# Create your views here.
def ManagerReportView(request):
    template = loader.get_template('reports/partials/sales_transactions.html')
    context = {}
    return HttpResponse(template.render(context,request))