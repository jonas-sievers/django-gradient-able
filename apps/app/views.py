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

from .models import Charging, Real_estate
from .forms import Real_estateForm, ChargingForm



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('welcome.html')
    return HttpResponse(html_template.render(context, request))
      

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
            if request.method == "POST":  
                print("POST") 
                form = Real_estateForm(request.POST)  
                if form.is_valid():
                    print("VALID")  
                    real_estate = form.save(commit=False)   
                    real_estate.person = request.user.username
                    real_estate.pub_date = timezone.now()
                    print("hier------------------")
                    print(real_estate.property_type)
                    print(real_estate.charging_points_to_install)
                    print(type(real_estate.charging_points_to_install))
                    real_estate.image_path = get_image_path(real_estate.property_type, real_estate.charging_points_to_install)
                    real_estate.save()  
                    print("Yes------------------")
                    print(real_estate.image_path)
                    return render(request, 'db_general.html', {'real_estate': real_estate})
            else: 
                print("else") 
                form = Real_estateForm()
            return render(request, 'personal_facts.html', {'form': form})
            
        if load_template == 'db_general.html':
            real_estate = get_object_or_404(Real_estate, pk=1)
            html_template = loader.get_template(load_template)
            return render(request, 'db_general.html', {'real_estate': real_estate})
        
        if load_template == 'db_costs.html':
            if request.method == "POST":  
                print("POST") 
                form = ChargingForm(request.POST)  
                if form.is_valid():
                    print("VALID")  
                    charging = form.save(commit=False)   
                    charging.person = request.user.username
                    charging.pub_date = timezone.now()
                    charging.save()  
                    return render(request, 'db_costs.html', {'form': form, 'charging': charging})
            else: 
                form = ChargingForm()
                charging = get_object_or_404(Charging, pk=1)
            return render(request, 'db_costs.html', {'form': form, 'charging': charging})
                      
            
        context['segment'] = load_template
       
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


def get_image_path(property_type, charging_points_to_install):
    
    if(property_type == "Einfamilienhaus"):
        print("Einfamlienhaus mit einer Wallbox")
        if(charging_points_to_install == 1):
            result = "/static/assets/images/slider/E1W.png"
        elif(charging_points_to_install == 2):
            result = "/static/assets/images/slider/E2W.png"
        elif(charging_points_to_install == 3):
            result = "/static/assets/images/slider/E3W.png"
        elif(charging_points_to_install == 4):
            result = "/static/assets/images/slider/E4W.png"
        elif(charging_points_to_install == 5):
            result = "/static/assets/images/slider/E5W.png"
        else:
            result = "/static/assets/images/slider/EVW.png"
    else: 
        print("Mehrfamilienhaus")
        if(charging_points_to_install == 1):
            result = "/static/assets/images/slider/M1W.png"
        elif(charging_points_to_install == 2):
            result = "/static/assets/images/slider/M2W.png"
        elif(charging_points_to_install == 3):
            result = "/static/assets/images/slider/M3W.png"
        elif(charging_points_to_install == 4):
            result = "/static/assets/images/slider/M4W.png"
        elif(charging_points_to_install == 5):
            result = "/static/assets/images/slider/M5W.png"
        else:
            result = "/static/assets/images/slider/MVW.png"
    
    print("ergebnis" + result)
    return result