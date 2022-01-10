# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.utils import timezone

from .models import Lokal_Energy, Real_estate
from .forms import Lokal_EnergyForm, Real_estateForm



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
                    real_estate.electricity_consumption_year = get_electricity_consumption_year(real_estate.property_type, real_estate.water_heating, real_estate.number_persons)
                    real_estate.person = request.user.username
                    real_estate.pub_date = timezone.now()
                    real_estate.image_path = get_image_path(real_estate.property_type, real_estate.charging_points_to_install)
                    real_estate.save()
                    #Save Results as Session Variable
                    #Otherwise they would need to stand in the url
                    ##Lastprofil und Stromverbrauch
                    request.session['property_type'] = real_estate.property_type
                    request.session['water_heating'] = real_estate.water_heating
                    request.session['number_persons'] = real_estate.number_persons
                    request.session['electricity_consumption_year'] = real_estate.electricity_consumption_year
                    #Laden
                    request.session['charging_points_to_install'] = real_estate.charging_points_to_install
                    request.session['charging_points_expandable'] = real_estate.charging_points_expandable
                    request.session['house_connection_power'] = real_estate.house_connection_power
                    request.session['image_path'] = real_estate.image_path
                    request.session['driving_profile'] = real_estate.driving_profile
                    request.session['arrival_time'] = real_estate.arrival_time
                    request.session['departure_time'] = real_estate.departure_time
                    #Kabel
                    request.session['cable_length'] = real_estate.cable_length
                    request.session['usage_years'] = real_estate.usage_years

                    # Calculate optimal Verlustleistung
                    verlustleistung_results = get_optimal_verlustleistung(real_estate.cable_length, real_estate.driving_profile, real_estate.usage_years)
                    request.session['opt_querschnitt'] = verlustleistung_results[0]
                    request.session['opt_cable_costs'] = verlustleistung_results[1]
                    request.session['opt_verlustleistungscosts'] = verlustleistung_results[2]
                    request.session['opt_min_costs'] = verlustleistung_results[3]
                    request.session['cable_costs_1_5mm'] = verlustleistung_results[4]
                    request.session['verlustleistung_costs_1_5mm'] = verlustleistung_results[5]
                    request.session['costs_1_5mm'] = verlustleistung_results[6]
                    
                    #Calculate Steuerbare Verbrauchseinrichtung
                    sve_results = get_sve_results(real_estate.driving_profile)
           
                    request.session['jahres_stromverbrauch'] = sve_results[0]
                    request.session['sve_einsparung_monat'] = sve_results[1]
                    request.session['sve_einsparung_jahr'] = sve_results[2]

                    #Calculate dynamische Stromtarife
                    dyn_Stromtarife_results = get_dyn_stromtarife_results(real_estate.driving_profile)
           
                    request.session['dyn_stromtarife_haushaltsstrom_kosten'] = dyn_Stromtarife_results[0]
                    request.session['dyn_stromtarife_ladestrom_kosten'] = dyn_Stromtarife_results[1]
                    request.session['dyn_stromtarife_kosten'] = dyn_Stromtarife_results[2]
                    request.session['dyn_stromtarife_opt_tarif'] = dyn_Stromtarife_results[3]

                    return redirect('db_load_management.html')
            else: 
                form = Real_estateForm()
            return render(request, 'input_form.html', {'form': form})                      
            
        context['segment'] = load_template

        if load_template == 'input_form_PV.html':
            if request.method == "POST":  
                form = Lokal_EnergyForm(request.POST)  
                if form.is_valid():
                    lokal_energy = form.save(commit=False)   
                    lokal_energy.person = request.user.username
                    lokal_energy.pub_date = timezone.now()

                    lokal_energy.pv_kw_peak = get_kW_peak(lokal_energy.roof_size)
                    lokal_energy.electricity_generation_year = get_electricity_generation_year(lokal_energy.pv_kw_peak, lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation)
                    
                    lokal_energy.pv_1KWpeak_investment_cost = get_investment_cost(1)
                    lokal_energy.pv_1KWpeak_saved_costs_own_electricity = get_saved_costs(1,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_1KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(1,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])

                    lokal_energy.pv_2KWpeak_investment_cost = get_investment_cost(2)
                    lokal_energy.pv_2KWpeak_saved_costs_own_electricity = get_saved_costs(2,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_2KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(2,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])

                    lokal_energy.pv_3KWpeak_investment_cost = get_investment_cost(3)
                    lokal_energy.pv_3KWpeak_saved_costs_own_electricity = get_saved_costs(3,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_3KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(3,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_4KWpeak_investment_cost = get_investment_cost(4)
                    lokal_energy.pv_4KWpeak_saved_costs_own_electricity = get_saved_costs(4,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_4KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(4,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_5KWpeak_investment_cost = get_investment_cost(5)
                    lokal_energy.pv_5KWpeak_saved_costs_own_electricity = get_saved_costs(5,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_5KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(5,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_6KWpeak_investment_cost = get_investment_cost(6)
                    lokal_energy.pv_6KWpeak_saved_costs_own_electricity = get_saved_costs(6,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_6KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(6,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_7KWpeak_investment_cost = get_investment_cost(7)
                    lokal_energy.pv_7KWpeak_saved_costs_own_electricity = get_saved_costs(7,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_7KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(7,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_8KWpeak_investment_cost = get_investment_cost(8)
                    lokal_energy.pv_8KWpeak_saved_costs_own_electricity = get_saved_costs(8,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_8KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(8,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_9KWpeak_investment_cost = get_investment_cost(9)
                    lokal_energy.pv_9KWpeak_saved_costs_own_electricity = get_saved_costs(9,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_9KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(9,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                    lokal_energy.pv_10KWpeak_investment_cost = get_investment_cost(10)
                    lokal_energy.pv_10KWpeak_saved_costs_own_electricity = get_saved_costs(10 ,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    lokal_energy.pv_10KWpeak_earnings_sold_electricity = get_earnings_sold_electricity(10 ,lokal_energy.solar_radiation, lokal_energy.roof_tilt, lokal_energy.roof_orientation, request.session['electricity_consumption_year'])
                    
                                    
                    lokal_energy.save()
                    #Save Results as Session Variable
                    #Otherwise they would need to stand in the url
                    request.session['roof_size'] = lokal_energy.roof_size
                    request.session['roof_tilt'] = lokal_energy.roof_tilt
                    request.session['roof_orientation'] = lokal_energy.roof_orientation
                    request.session['solar_radiation'] = lokal_energy.solar_radiation
                    request.session['pv_kw_peak'] = lokal_energy.pv_kw_peak
                    request.session['electricity_generation_year'] = lokal_energy.electricity_generation_year
                    
                    request.session['pv_1KWpeak_investment_cost'] =  lokal_energy.pv_1KWpeak_investment_cost
                    request.session['pv_1KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_1KWpeak_saved_costs_own_electricity
                    request.session['pv_1KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_1KWpeak_earnings_sold_electricity
                    
                    request.session['pv_2KWpeak_investment_cost'] =  lokal_energy.pv_2KWpeak_investment_cost
                    request.session['pv_2KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_2KWpeak_saved_costs_own_electricity
                    request.session['pv_2KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_2KWpeak_earnings_sold_electricity
                    
                    request.session['pv_3KWpeak_investment_cost'] =  lokal_energy.pv_3KWpeak_investment_cost
                    request.session['pv_3KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_3KWpeak_saved_costs_own_electricity
                    request.session['pv_3KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_3KWpeak_earnings_sold_electricity
                    
                    request.session['pv_4KWpeak_investment_cost'] =  lokal_energy.pv_4KWpeak_investment_cost
                    request.session['pv_4KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_4KWpeak_saved_costs_own_electricity
                    request.session['pv_4KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_4KWpeak_earnings_sold_electricity
                    
                    request.session['pv_5KWpeak_investment_cost'] =  lokal_energy.pv_5KWpeak_investment_cost
                    request.session['pv_5KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_5KWpeak_saved_costs_own_electricity
                    request.session['pv_5KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_5KWpeak_earnings_sold_electricity
                    
                    request.session['pv_6KWpeak_investment_cost'] =  lokal_energy.pv_6KWpeak_investment_cost
                    request.session['pv_6KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_6KWpeak_saved_costs_own_electricity
                    request.session['pv_6KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_6KWpeak_earnings_sold_electricity
                    
                    request.session['pv_7KWpeak_investment_cost'] =  lokal_energy.pv_7KWpeak_investment_cost
                    request.session['pv_7KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_7KWpeak_saved_costs_own_electricity
                    request.session['pv_7KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_7KWpeak_earnings_sold_electricity
                    
                    request.session['pv_8KWpeak_investment_cost'] =  lokal_energy.pv_8KWpeak_investment_cost
                    request.session['pv_8KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_8KWpeak_saved_costs_own_electricity
                    request.session['pv_8KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_8KWpeak_earnings_sold_electricity
                    
                    request.session['pv_9KWpeak_investment_cost'] =  lokal_energy.pv_9KWpeak_investment_cost
                    request.session['pv_9KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_9KWpeak_saved_costs_own_electricity
                    request.session['pv_9KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_9KWpeak_earnings_sold_electricity
                    
                    request.session['pv_10KWpeak_investment_cost'] =  lokal_energy.pv_10KWpeak_investment_cost
                    request.session['pv_10KWpeak_saved_costs_own_electricity'] =  lokal_energy.pv_10KWpeak_saved_costs_own_electricity
                    request.session['pv_10KWpeak_earnings_sold_electricity'] =  lokal_energy.pv_10KWpeak_earnings_sold_electricity
                                        
                    return redirect('db_renewables.html')
            else: 
                form = Lokal_EnergyForm()
            return render(request, 'input_form_PV.html', {'form': form})  

        #Check if Session is new
        #If Session is new, set standard variables in session variables
        real_estate = get_object_or_404(Real_estate, pk=1)
        if 'property_type' not in request.session:
            request.session['property_type'] = real_estate.property_type
            request.session['water_heating'] = real_estate.water_heating
            request.session['number_persons'] = real_estate.number_persons
            request.session['electricity_consumption_year'] = real_estate.electricity_consumption_year
            request.session['charging_points_to_install'] = real_estate.charging_points_to_install
            request.session['charging_points_expandable'] = real_estate.charging_points_expandable
            request.session['house_connection_power'] = real_estate.house_connection_power
            request.session['image_path'] = real_estate.image_path
            request.session['driving_profile'] = real_estate.driving_profile
            request.session['arrival_time'] = real_estate.arrival_time
            request.session['departure_time'] = real_estate.departure_time
            request.session['cable_length'] = real_estate.cable_length
            request.session['usage_years'] = real_estate.usage_years
        if 'opt_querschnitt' not in request.session:
            # Calculate optimal Verlustleistung
            verlustleistung_results = get_optimal_verlustleistung(10, 40, 20)
            request.session['opt_querschnitt'] = verlustleistung_results[0]
            request.session['opt_cable_costs'] = verlustleistung_results[1]
            request.session['opt_verlustleistungscosts'] = verlustleistung_results[2]
            request.session['opt_min_costs'] = verlustleistung_results[3]
            request.session['cable_costs_1_5mm'] = verlustleistung_results[4]
            request.session['verlustleistung_costs_1_5mm'] = verlustleistung_results[5]
            request.session['costs_1_5mm'] = verlustleistung_results[6]
                    
            #Calculate Steuerbare Verbrauchseinrichtung
            sve_results = get_sve_results(40)
    
            request.session['jahres_stromverbrauch'] = sve_results[0]
            request.session['sve_einsparung_monat'] = sve_results[1]
            request.session['sve_einsparung_jahr'] = sve_results[2]

            #Calculate dynamische Stromtarife
            dyn_Stromtarife_results = get_dyn_stromtarife_results(40)
    
            request.session['dyn_stromtarife_haushaltsstrom_kosten'] = dyn_Stromtarife_results[0]
            request.session['dyn_stromtarife_ladestrom_kosten'] = dyn_Stromtarife_results[1]
            request.session['dyn_stromtarife_kosten'] = dyn_Stromtarife_results[2]
            request.session['dyn_stromtarife_opt_tarif'] = dyn_Stromtarife_results[3]

        lokal_energy = get_object_or_404(Lokal_Energy, pk=1)
        if 'roof_size' not in request.session:
            request.session['roof_size'] = lokal_energy.roof_size
            request.session['roof_tilt'] = lokal_energy.roof_tilt
            request.session['roof_orientation'] = lokal_energy.roof_orientation
            request.session['solar_radiation'] = lokal_energy.solar_radiation
            request.session['pv_kw_peak'] = lokal_energy.pv_kw_peak
            request.session['electricity_generation_year'] = lokal_energy.electricity_generation_year
                
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

######
######Getter Methoden
######

def get_optimal_verlustleistung(cable_length, driving_profile, usage_years):
    verlustleistung_costs_1_5mm = round(((((768*int(cable_length))/(56*1.5)) * ((int(driving_profile)*73)/(11000)) * (0.25*int(usage_years)))), 1)
    verlustleistung_costs_2_5mm = round(((((768*int(cable_length))/(56*2.5)) * ((int(driving_profile)*73)/(11000)) * (0.25*int(usage_years)))), 1)
    verlustleistung_costs_4mm = round(((((768*int(cable_length))/(56*4)) * ((int(driving_profile)*73)/(11000)) * (0.25*int(usage_years)))), 1)
    verlustleistung_costs_6mm = round(((((768*int(cable_length))/(56*6)) * ((int(driving_profile)*73)/(11000)) * (0.25*int(usage_years)))), 1)
    verlustleistung_costs_10mm = round(((((768*int(cable_length))/(56*10)) * ((int(driving_profile)*73)/(11000)) * (0.25*int(usage_years)))), 1)
    verlustleistung_costs_16mm = round(((((768*int(cable_length))/(56*16)) * ((int(driving_profile)*73)/(11000)) * (0.25*int(usage_years)))), 1)
    
    verlustleistungscosts = [verlustleistung_costs_1_5mm, verlustleistung_costs_2_5mm, verlustleistung_costs_4mm, verlustleistung_costs_6mm, verlustleistung_costs_10mm, verlustleistung_costs_16mm]

    cable_costs_1_5mm = round( (1*int(cable_length)), 1)
    cable_costs_2_5mm = round((1.6*int(cable_length)), 1)
    cable_costs_4mm = round((3.5*int(cable_length)), 1)
    cable_costs_6mm = round((4.7*int(cable_length)), 1)
    cable_costs_10mm = round((7.4*int(cable_length)), 1)
    cable_costs_16mm = round((12*int(cable_length)), 1)
    cable_costs = [cable_costs_1_5mm, cable_costs_2_5mm, cable_costs_4mm, cable_costs_6mm, cable_costs_10mm, cable_costs_16mm]
    
    complete_costs = [(verlustleistung_costs_1_5mm+cable_costs_1_5mm), (verlustleistung_costs_2_5mm+cable_costs_2_5mm), (verlustleistung_costs_4mm+cable_costs_4mm), (verlustleistung_costs_6mm+cable_costs_6mm), (verlustleistung_costs_10mm+cable_costs_10mm), (verlustleistung_costs_16mm+cable_costs_16mm)]
    
    min_costs = complete_costs[0]
    opt_index = 0
    for i in range(len(complete_costs)):
        if min_costs >= complete_costs[i]:
            min_costs = complete_costs[i]
            opt_index = i


    costs_1_5mm = complete_costs[0]

    if(opt_index == 0):
        opt_a = 1,5
    elif(opt_index == 1):
        opt_a = 2.5
    elif(opt_index == 2):
        opt_a = 4.0
    elif(opt_index == 3):
        opt_a = 6.0
    elif(opt_index == 4):
        opt_a = 10
    elif(opt_index == 5):
        opt_a = 16


    return [opt_a, cable_costs[opt_index], verlustleistungscosts[opt_index], min_costs, cable_costs_1_5mm, verlustleistung_costs_1_5mm, costs_1_5mm]
    
def get_sve_results(driving_profile):
    jahres_stromverbrauch = round((int(driving_profile)*0.2*365),1)
    sve_einsparung_monat = round(((int(driving_profile)*0.2*0.03*30)-1.66), 2)
    sve_einsparung_jahr = round(((int(driving_profile)*0.2*0.03*365)-1.66), 2)
    result = [jahres_stromverbrauch, sve_einsparung_monat, sve_einsparung_jahr]
    return result

def get_dyn_stromtarife_results(driving_profile):
    
    dyn_stromtarife_haushaltsstrom_kosten = round((int(driving_profile)*30*0.2*0.3216),2)
    dyn_stromtarife_ladestrom_kosten = round(((int(driving_profile)*30*0.2*0.2987)+10.6),2)
    dyn_stromtarife_kosten = 0
    if (int(driving_profile) == 20):
        dyn_stromtarife_kosten == round( (( (int(driving_profile)*30*0.2*(0.1812+0.06464+0.00025))+4.58)),2)
    elif (int(driving_profile) == 40):
        dyn_stromtarife_kosten = round(( (int(driving_profile)*30*0.2*(0.1812 + 0.06464 + 0.00025))+ 4.58 ),2)
    elif (int(driving_profile) == 60):
        dyn_stromtarife_kosten = round(((int(driving_profile)*30*0.2*(0.1812+((0.06464+0.06564)/2)+0.00025)+4.58)),2)
    elif (int(driving_profile) == 100):
        dyn_stromtarife_kosten = round(((int(driving_profile)*30*0.2*(0.1812+((0.06464+0.06564)/2)+0.00025)+4.58)),2)

    dyn_Stromtarife_results = [dyn_stromtarife_haushaltsstrom_kosten, dyn_stromtarife_ladestrom_kosten, dyn_stromtarife_kosten]
    
    opt_tarif_index = 0
    opt_tarif = dyn_Stromtarife_results[0]
    for i in range(len(dyn_Stromtarife_results)):
        if opt_tarif > dyn_Stromtarife_results[i]:
            opt_tarif_index = i

    if opt_tarif_index == 0:
        opt_tarif = "Haushaltsstrom"
    elif opt_tarif_index ==1:
        opt_tarif = "Ladestrom"
    elif opt_tarif_index ==2:
        opt_tarif = "Dynamischer Stromtarif"

    dyn_Stromtarife_results.append(opt_tarif)
    return dyn_Stromtarife_results
           

def get_kW_peak(roof_size):
    result = round((int(roof_size)/6), 1)
    return result

def get_investment_cost(kw_peak):
    # Kosten_PV_Anlage + Kosten_Installation_PV + Operation_Maintenance_PV + Batterie_kosten + Operation_Maintenance_Battery
    result = 1430*kw_peak + (1430*kw_peak)*0.08 + (1430*kw_peak)*0.015*25 + 1813 + 1813*0.08 + 22*kw_peak*25
    
    return round(result,2)

def get_saved_costs(kw_peak, solar_radiation, roof_tilt, roof_orientation, electricity_consumption_year):
    electricity_generation_year = get_electricity_generation_year(kw_peak, solar_radiation, roof_tilt, roof_orientation)
    electricity_generation_day= (electricity_generation_year/365)
    electricity_consumption_day = electricity_consumption_year/365
    
    #Wenn Erzeugung <= Verbrauch, dann mit 0,28 € multiplizieren

    list_electricity_generation_day = [0, 0, 0, 0, 0, 0, 0, round((0.01*electricity_generation_day),3), round((0.02*electricity_generation_day),3), round((0.05*electricity_generation_day),3), round((0.08*electricity_generation_day), 3), round((0.11*electricity_generation_day), 3), round((0.12*electricity_generation_day), 3), round((0.13*electricity_generation_day), 3), round((0.13*electricity_generation_day), 3), round((0.12*electricity_generation_day), 3), round((0.10*electricity_generation_day), 3), round((0.08*electricity_generation_day), 3), round((0.04*electricity_generation_day), 3), round((0.01*electricity_generation_day), 3), 0, 0, 0, 0]
    list_electricity_consumption_day = [round((0.0197*electricity_consumption_day), 3), round((0.0168*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0219*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0518*electricity_consumption_day), 3), round((0.0539*electricity_consumption_day), 3), round((0.0481*electricity_consumption_day), 3), round((0.0466*electricity_consumption_day), 3), round((0.0466*electricity_consumption_day), 3), round((0.0510*electricity_consumption_day), 3), round((0.0474*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0401*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0547*electricity_consumption_day), 3), round((0.062*electricity_consumption_day), 3), round((0.0729*electricity_consumption_day), 3), round((0.062*electricity_consumption_day), 3), round((0.051*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0306*electricity_consumption_day), 3)]
    saved_costs = 0.0
    for index in range(len(list_electricity_generation_day)):
        if list_electricity_generation_day[index] <= list_electricity_consumption_day[index]:
            saved_costs = saved_costs + (list_electricity_generation_day[index]*0.28)
        else:
            saved_costs = saved_costs + list_electricity_consumption_day[index]*0.28
    
    saved_costs = round((saved_costs*365*25), 2)
   
    return saved_costs

def get_earnings_sold_electricity(kw_peak, solar_radiation, roof_tilt, roof_orientation, electricity_consumption_year):
    electricity_generation_year = get_electricity_generation_year(kw_peak, solar_radiation, roof_tilt, roof_orientation)
    electricity_generation_day = (electricity_generation_year/365)
    electricity_consumption_day = electricity_consumption_year/365

    #Wenn Erzeugung <= Verbrauch, dann mit 0,28 € multiplizieren

    list_electricity_generation_day = [0, 0, 0, 0, 0, 0, 0, round((0.01*electricity_generation_day),3), round((0.02*electricity_generation_day),3), round((0.05*electricity_generation_day),3), round((0.08*electricity_generation_day), 3), round((0.11*electricity_generation_day), 3), round((0.12*electricity_generation_day), 3), round((0.13*electricity_generation_day), 3), round((0.13*electricity_generation_day), 3), round((0.12*electricity_generation_day), 3), round((0.10*electricity_generation_day), 3), round((0.08*electricity_generation_day), 3), round((0.04*electricity_generation_day), 3), round((0.01*electricity_generation_day), 3), 0, 0, 0, 0]
    list_electricity_consumption_day = [round((0.0197*electricity_consumption_day), 3), round((0.0168*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0219*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0518*electricity_consumption_day), 3), round((0.0539*electricity_consumption_day), 3), round((0.0481*electricity_consumption_day), 3), round((0.0466*electricity_consumption_day), 3), round((0.0466*electricity_consumption_day), 3), round((0.0510*electricity_consumption_day), 3), round((0.0474*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0401*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0547*electricity_consumption_day), 3), round((0.062*electricity_consumption_day), 3), round((0.0729*electricity_consumption_day), 3), round((0.062*electricity_consumption_day), 3), round((0.051*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0306*electricity_consumption_day), 3)]
    
    earnings = 0.0
    for index in range(len(list_electricity_generation_day)):
        if list_electricity_generation_day[index] > list_electricity_consumption_day[index]:
            earnings = earnings + (list_electricity_generation_day[index] - list_electricity_consumption_day[index])*0.06

    earnings = round((earnings*365*25), 2)

    return earnings
    
def get_electricity_consumption_year(property_type, water_heating, number_persons):
    if(property_type == "Haus"):
        if(water_heating == "ohne Strom"):
            if(number_persons == "1 Person"):
                result = 2500
            elif(number_persons == "2 Personen"):
                result = 3000
            elif(number_persons == "3 Personen"):
                result = 3700
            elif(number_persons == "4 Personen"):
                result = 4000
            elif(number_persons == "> 4 Personen"):
                result = 5000
        else: 
            if(number_persons == "1 Person"):
                result = 2900
            elif(number_persons == "2 Personen"):
                result = 3800
            elif(number_persons == "3 Personen"):
                result = 4800
            elif(number_persons == "4 Personen"):
                result = 5500
            elif(number_persons == "> 4 Personen"):
                result = 6800
    else:
        if(water_heating == "ohne Strom"):
            if(number_persons == "1 Person"):
                result = 1500
            elif(number_persons == "2 Personen"):
                result = 2100
            elif(number_persons == "3 Personen"):
                result = 2600
            elif(number_persons == "4 Personen"):
                result = 2900
            elif(number_persons == "> 4 Personen"):
                result = 3500
        else: 
            if(number_persons == "1 Person"):
                result = 2000
            elif(number_persons == "2 Personen"):
                result = 3000
            elif(number_persons == "3 Personen"):
                result = 4000
            elif(number_persons == "4 Personen"):
                result = 4500
            elif(number_persons == "> 4 Personen"):
                result = 5200
    return result

def get_electricity_generation_year(kw_peak, solar_radiation, roof_tilt, roof_orientation):
    if(roof_tilt == "0"):
        factor_tilt_orientation = 1
    elif(roof_tilt == "15"):
        if(roof_orientation =="Süd"):
            factor_tilt_orientation = 1.1
        if(roof_orientation =="Süd-West/ Süd-Ost"):
            factor_tilt_orientation = 1.05
        if(roof_orientation =="West/ Ost"):
            factor_tilt_orientation = 1
        if(roof_orientation =="Nord-West/ Nord-Ost"):
            factor_tilt_orientation = 0.95
        if(roof_orientation =="Nord"):
            factor_tilt_orientation = 0.9
    elif(roof_tilt == "30"):
        if(roof_orientation =="Süd"):
            factor_tilt_orientation = 1.1
        if(roof_orientation =="Süd-West/ Süd-Ost"):
            factor_tilt_orientation = 1.05
        if(roof_orientation =="West/ Ost"):
            factor_tilt_orientation = 0.95
        if(roof_orientation =="Nord-West/ Nord-Ost"):
            factor_tilt_orientation = 0.85
        if(roof_orientation =="Nord"):
            factor_tilt_orientation = 0.78
    elif(roof_tilt == "45"):
        if(roof_orientation =="Süd"):
            factor_tilt_orientation = 1.1
        if(roof_orientation =="Süd-West/ Süd-Ost"):
            factor_tilt_orientation = 1.05
        if(roof_orientation =="West/ Ost"):
            factor_tilt_orientation = 0.9
        if(roof_orientation =="Nord-West/ Nord-Ost"):
            factor_tilt_orientation = 0.89
        if(roof_orientation =="Nord"):
            factor_tilt_orientation = 0.65
    else: 
        factor_tilt_orientation = 0        
   
    result = round((int(kw_peak)*int(solar_radiation)*factor_tilt_orientation*0.8335), 1)
    return result


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
    return result