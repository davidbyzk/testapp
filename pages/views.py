from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from users.models import CustomUser
from django.contrib.auth.decorators import login_required

class HomePageView(TemplateView):
    template_name = 'home.html'

@login_required
def dashboard(request):
    t = loader.get_template('dashboard.html')
    c={}
    return HttpResponse(t.render(c, request), content_type='text/html')

