# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .models import Real_estate
from .forms import Real_estateForm



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

        if load_template == 'input_form.html':
            if request.method == "POST":  
                form = Real_estateForm(request.POST)  
                if form.is_valid():
                    real_estate = form.save(commit=False)   
                    real_estate.person = request.user.username
                    real_estate.pub_date = timezone.now()
                    real_estate.image_path = get_image_path(real_estate.property_type, real_estate.charging_points_to_install)
                    real_estate.save()
                    #Save Results as Session Variable
                    #Otherwise they would need to stand in the url
                    request.session['property_type'] = real_estate.property_type
                    request.session['charging_points_to_install'] = real_estate.charging_points_to_install
                    request.session['charging_points_expandable'] = real_estate.charging_points_expandable
                    request.session['house_connection_power'] = real_estate.house_connection_power
                    request.session['image_path'] = real_estate.image_path
                    request.session['driving_profile'] = real_estate.driving_profile
                    request.session['arrival_time'] = real_estate.arrival_time
                    request.session['departure_time'] = real_estate.departure_time
                    request.session['cable_length'] = real_estate.cable_length
                    request.session['usage_years'] = real_estate.usage_years
                    return redirect('db_load_management.html')
            else: 
                form = Real_estateForm()
            return render(request, 'input_form.html', {'form': form})                      
            
        context['segment'] = load_template

        #Check if Session is new
        #If Session is new, set standard variables in session variables
        real_estate = get_object_or_404(Real_estate, pk=1)
        if 'property_type' not in request.session:
            request.session['property_type'] = real_estate.property_type
            request.session['charging_points_to_install'] = real_estate.charging_points_to_install
            request.session['charging_points_expandable'] = real_estate.charging_points_expandable
            request.session['house_connection_power'] = real_estate.house_connection_power
            request.session['image_path'] = real_estate.image_path
            request.session['driving_profile'] = real_estate.driving_profile
            request.session['arrival_time'] = real_estate.arrival_time
            request.session['departure_time'] = real_estate.departure_time
            request.session['cable_length'] = real_estate.cable_length
            request.session['usage_years'] = real_estate.usage_years
              
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