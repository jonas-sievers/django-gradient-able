# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Real_estate
from .forms import Real_estateForm



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('welcome.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def personal_facts(request):
    if request.method == "POST":   
       form = Real_estateForm(request.POST)  
       if form.is_valid():   
           real_estate = form.save(commit=False)   
           real_estate.person = "Jonas Sievers"   
           real_estate.pub_date = timezone.now()
           real_estate.save()   
           return HttpResponseRedirect(reverse('db_general', args=(real_estate.pk,)))  
    else:   
          form = Real_estateForm()
    return render(request, 'personal_facts.html', {'form': form}) 
        

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
       
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        if load_template == 'personal_facts.html':
            print("-----------------------facts----------------------------------------------")
            if request.method == "POST":   
                print("-----------------------POST----------------------------------------------")
                form = Real_estateForm(request.POST)  
                if form.is_valid():  
                    print("-----------------------VALID----------------------------------------------") 
                    real_estate = form.save(commit=False)   
                    real_estate.person = "Jonas Sievers"   
                    real_estate.pub_date = timezone.now()
                    real_estate.save()   
                    return HttpResponseRedirect('db_general.html')  
            else:
                print("-----------------------NOT POST----------------------------------------------")   
                form = Real_estateForm()
            return render(request, 'personal_facts.html', {'form': form})
            
            context['segment'] = load_template
       
            html_template = loader.get_template(load_template)
            return HttpResponse(html_template.render(context, request))
            
       
       
        context['segment'] = load_template
       
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
