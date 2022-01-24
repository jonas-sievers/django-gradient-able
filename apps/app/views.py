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

#Standard Python Formattierung existiert nur für englisches Format (Punkt das Dezimaltrennzeichen)
#drop trailing zeros from decimal
def number_format(number):
    try: 
        number = round((float(number)), 2)
        #Wenn keine Nachkommastelle, dann Dezimalstellen abschneiden
        if number.is_integer():
            formatted_number = ("%g" % number).replace('.',',')
        #Sonst immer zwei Nachkommastellen anzeigen
        else: 
             formatted_number = '{0:.2f}'.format(number).replace('.', ',')
    except:
        formatted_number = number
    return formatted_number

#@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    #Check if Session is new
    #If Session is new, set standard variables in session variables
    real_estate = get_object_or_404(Real_estate, pk=1)
    if 'property_type' not in request.session:
        request.session['property_type'] = real_estate.property_type
        request.session['number_properties'] = real_estate.number_properties
        request.session['water_heating'] = real_estate.water_heating
        request.session['number_persons'] = real_estate.number_persons
        request.session['electricity_consumption_year'] = number_format(real_estate.electricity_consumption_year)
        request.session['electricity_consumption_year_number'] = real_estate.electricity_consumption_year
        request.session['electricity_consumption_day'] = number_format((int(real_estate.electricity_consumption_year)/ 365))
        request.session['charging_points_to_install'] = real_estate.charging_points_to_install
        request.session['house_connection_power'] = real_estate.house_connection_power
        request.session['image_path'] = real_estate.image_path
        request.session['driving_profile'] = real_estate.driving_profile
        request.session['arrival_time'] = real_estate.arrival_time
        request.session['departure_time'] = real_estate.departure_time
        request.session['cable_length'] = real_estate.cable_length
        request.session['usage_years'] = real_estate.usage_years

    #Calculate Stat. and dyn. Loadmanagement
    if 'hours_to_charge' not in request.session:        
        stat_dyn_loadmanagement_results = get_stat_dyn_loadmanagement(3800, 1, 'mit Strom', 43, 4, 40, 17, 8)
        request.session['hours_to_charge'] = number_format(stat_dyn_loadmanagement_results[0])
        request.session['needed_electricity_ev_day'] = number_format(stat_dyn_loadmanagement_results[1])
        request.session['stat_Leistungs_peak_ohne_ev_kW'] = number_format(stat_dyn_loadmanagement_results[2])
        request.session['stat_verfuegbare_ladeleistung_fuer_alle_wallboxen'] = number_format(stat_dyn_loadmanagement_results[3])
        request.session['stat_verfuegbare_ladeleistung_fuer_wallbox'] = number_format(stat_dyn_loadmanagement_results[4])
        request.session['stat_needed_time_to_charge'] = number_format(stat_dyn_loadmanagement_results[5])
        request.session['stat_loadmanagement_max_evs_to_charge'] = number_format(stat_dyn_loadmanagement_results[6])
        request.session['opt_lastmanagement'] = stat_dyn_loadmanagement_results[7]
        request.session['dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen'] = number_format(stat_dyn_loadmanagement_results[8])
        request.session['dyn_verfuegbare_ladeleistung_fuer_wallbox'] = number_format(stat_dyn_loadmanagement_results[9])
        request.session['dyn_needed_time_to_charge'] = number_format(stat_dyn_loadmanagement_results[10])
        request.session['dyn_loadmanagement_max_evs_to_charge'] = number_format(stat_dyn_loadmanagement_results[11])
                

    if 'opt_querschnitt' not in request.session:
        #Calculate dynamische Stromtarife
        dyn_Stromtarife_results = get_dyn_stromtarife_results(40, 3800, 0.75, 17, 8)
        request.session['electricity_consumption_month_house'] = number_format(dyn_Stromtarife_results[0])
        request.session['electricity_consumption_month_ev'] = number_format(dyn_Stromtarife_results[1])    
        request.session['electricity_consumption_month_ev_house'] = number_format(round((dyn_Stromtarife_results[0] + dyn_Stromtarife_results[1]),2))
        request.session['hausstrom_electricity_cost_month_house'] = number_format(dyn_Stromtarife_results[2])
        request.session['hausstrom_electricity_cost_month_ev_house'] = number_format(dyn_Stromtarife_results[3])
        request.session['ladestrom_electricity_cost_month_ev'] = number_format(dyn_Stromtarife_results[4])
        request.session['ladestrom_electricity_cost_month_ev_house'] = number_format(dyn_Stromtarife_results[5])
        request.session['dyn_strom_electricity_cost_month_ev'] = number_format(dyn_Stromtarife_results[6])
        request.session['dyn_strom_electricity_cost_month_ev_house'] = number_format(dyn_Stromtarife_results[7])
        request.session['opt_tarif'] = dyn_Stromtarife_results[8]
        request.session['opt_arbeitspreis_eur'] = number_format(dyn_Stromtarife_results[9])
        
        # Calculate optimal Verlustleistung
        verlustleistung_results = get_optimal_verlustleistung(10, 40, 20, 10.64, dyn_Stromtarife_results[9])
        request.session['opt_querschnitt'] = number_format(verlustleistung_results[0])
        request.session['opt_cable_costs'] = number_format(verlustleistung_results[1])
        request.session['opt_verlustleistungscosts'] = number_format(verlustleistung_results[2])
        request.session['opt_min_costs'] = number_format(verlustleistung_results[3])
        request.session['cable_costs_1_5mm'] = number_format(verlustleistung_results[4])
        request.session['verlustleistung_costs_1_5mm'] = number_format(verlustleistung_results[5])
        request.session['costs_1_5mm'] = number_format(verlustleistung_results[6])
                
        #Calculate Steuerbare Verbrauchseinrichtung
        sve_results = get_sve_results(40)

        request.session['jahres_stromverbrauch'] = number_format(sve_results[0])
        request.session['sve_einsparung_monat'] = number_format(sve_results[1])
        request.session['sve_einsparung_jahr'] = number_format(sve_results[2])

    lokal_energy = get_object_or_404(Lokal_Energy, pk=1)
    if 'roof_size' not in request.session:
        request.session['roof_size'] = lokal_energy.roof_size
        request.session['roof_tilt'] = lokal_energy.roof_tilt
        request.session['roof_orientation'] = lokal_energy.roof_orientation
        request.session['solar_radiation'] = lokal_energy.solar_radiation
        request.session['battery_capacity'] = lokal_energy.battery_capacity
        
        real_estate = get_object_or_404(Real_estate, pk=1)
        pv_storage_results = get_pv_storage_results(lokal_energy.battery_capacity, lokal_energy.roof_size, lokal_energy.roof_tilt, lokal_energy.roof_orientation, lokal_energy.solar_radiation, real_estate.electricity_consumption_year, real_estate.driving_profile, real_estate.arrival_time, real_estate.departure_time)
                
        request.session['pv_kW_peak'] = number_format(pv_storage_results[0])
        request.session['battery_kWh'] = number_format(pv_storage_results[1])
        request.session['pv_investment_cost_eur'] = number_format(pv_storage_results[2])
        request.session['battery_investment_cost_eur'] = number_format(pv_storage_results[3])
        request.session['capex_pv_und_battery'] = number_format(pv_storage_results[4])
        request.session['battery_status'] = pv_storage_results[5]
        request.session['electricity_pv_generation_day'] = number_format(pv_storage_results[6])
        request.session['electricity_consumption_day'] = number_format(pv_storage_results[7])
        request.session['electricity_sold_grid'] = number_format(pv_storage_results[8])
        request.session['electricity_saved'] = number_format(pv_storage_results[9])
        request.session['quote_pv_nutzung'] = number_format(pv_storage_results[10])
        request.session['quote_eigenversorgung'] = number_format(pv_storage_results[11])
        request.session['einnahmen_tag'] = number_format(pv_storage_results[12])
        request.session['einnahmen_jahr'] = number_format(pv_storage_results[13])
        request.session['gewinn_10_jahre'] = number_format(pv_storage_results[14])
        request.session['pv_speicher_sinnvoll'] = pv_storage_results[15]
        request.session['ev_connected_time'] = pv_storage_results[16]
        request.session['ev_deconnected_time'] = pv_storage_results[17]
        request.session['ev_needed_electricity_kWh'] = number_format(pv_storage_results[18])
        request.session['ev_charged_electricity'] = number_format(pv_storage_results[19])

    html_template = loader.get_template('welcome.html')
    return HttpResponse(html_template.render(context, request))
      

#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
       
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        if load_template == 'input_form_house.html':
            if request.method == "POST":  
                form = Real_estateForm(request.POST)  
                if form.is_valid():
                    real_estate = form.save(commit=False)   
                    real_estate.electricity_consumption_year = get_electricity_consumption_year(real_estate.property_type, real_estate.number_properties,  real_estate.water_heating, real_estate.number_persons)
                    real_estate.person = request.user.username
                    real_estate.pub_date = timezone.now()
                    real_estate.image_path = get_image_path(real_estate.property_type, real_estate.charging_points_to_install)
                    real_estate.save()
                    #Save Results as Session Variable
                    #Otherwise they would need to stand in the url
                    ##Lastprofil und Stromverbrauch
                    request.session['property_type'] = real_estate.property_type
                    request.session['number_properties'] = real_estate.number_properties
                    request.session['water_heating'] = real_estate.water_heating
                    request.session['number_persons'] = real_estate.number_persons                  
                    request.session['electricity_consumption_year'] = number_format(real_estate.electricity_consumption_year)
                    request.session['electricity_consumption_year_number'] = real_estate.electricity_consumption_year
                    request.session['electricity_consumption_day'] = number_format((int(real_estate.electricity_consumption_year)/ 365))
        
                    #Laden
                    request.session['charging_points_to_install'] = real_estate.charging_points_to_install
                    request.session['house_connection_power'] = real_estate.house_connection_power
                    request.session['image_path'] = real_estate.image_path
                    request.session['driving_profile'] = real_estate.driving_profile
                    request.session['arrival_time'] = real_estate.arrival_time
                    request.session['departure_time'] = real_estate.departure_time
                    #Kabel
                    request.session['cable_length'] = real_estate.cable_length
                    request.session['usage_years'] = real_estate.usage_years

                    #Calculate Stat. and dyn. Loadmanagement
                    stat_dyn_loadmanagement_results = get_stat_dyn_loadmanagement(real_estate.electricity_consumption_year, real_estate.number_properties, real_estate.water_heating, real_estate.house_connection_power, real_estate.charging_points_to_install, real_estate.driving_profile, real_estate.arrival_time, real_estate.departure_time)
                    request.session['hours_to_charge'] = number_format(stat_dyn_loadmanagement_results[0])
                    request.session['needed_electricity_ev_day'] = number_format(stat_dyn_loadmanagement_results[1])
                    request.session['stat_Leistungs_peak_ohne_ev_kW'] = number_format(stat_dyn_loadmanagement_results[2])
                    request.session['stat_verfuegbare_ladeleistung_fuer_alle_wallboxen'] = number_format(stat_dyn_loadmanagement_results[3])
                    request.session['stat_verfuegbare_ladeleistung_fuer_wallbox'] = number_format(stat_dyn_loadmanagement_results[4])
                    request.session['stat_needed_time_to_charge'] = number_format(stat_dyn_loadmanagement_results[5])
                    request.session['stat_loadmanagement_max_evs_to_charge'] = number_format(stat_dyn_loadmanagement_results[6])
                    request.session['opt_lastmanagement'] = stat_dyn_loadmanagement_results[7]
                    request.session['dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen'] = number_format(stat_dyn_loadmanagement_results[8])
                    request.session['dyn_verfuegbare_ladeleistung_fuer_wallbox'] = number_format(stat_dyn_loadmanagement_results[9])
                    request.session['dyn_needed_time_to_charge'] = number_format(stat_dyn_loadmanagement_results[10])
                    request.session['dyn_loadmanagement_max_evs_to_charge'] = number_format(stat_dyn_loadmanagement_results[11])
        

                    #Calculate dynamische Stromtarife
                    dyn_Stromtarife_results = get_dyn_stromtarife_results(real_estate.driving_profile, request.session['electricity_consumption_year_number'], stat_dyn_loadmanagement_results[10],  request.session['arrival_time'], request.session['departure_time']) 
                    request.session['electricity_consumption_month_house'] = number_format(dyn_Stromtarife_results[0])
                    request.session['electricity_consumption_month_ev'] = number_format(dyn_Stromtarife_results[1])    
                    request.session['electricity_consumption_month_ev_house'] = number_format(round((dyn_Stromtarife_results[0] + dyn_Stromtarife_results[1]),2))
                    request.session['hausstrom_electricity_cost_month_house'] = number_format(dyn_Stromtarife_results[2])
                    request.session['hausstrom_electricity_cost_month_ev_house'] = number_format(dyn_Stromtarife_results[3])
                    request.session['ladestrom_electricity_cost_month_ev'] = number_format(dyn_Stromtarife_results[4])
                    request.session['ladestrom_electricity_cost_month_ev_house'] = number_format(dyn_Stromtarife_results[5])
                    request.session['dyn_strom_electricity_cost_month_ev'] = number_format(dyn_Stromtarife_results[6])
                    request.session['dyn_strom_electricity_cost_month_ev_house'] = number_format(dyn_Stromtarife_results[7])
                    request.session['opt_tarif'] = dyn_Stromtarife_results[8]
                    request.session['opt_arbeitspreis_eur'] = number_format(dyn_Stromtarife_results[9])
                        
                    # Calculate optimal Verlustleistung
                    verlustleistung_results = get_optimal_verlustleistung(real_estate.cable_length, real_estate.driving_profile, real_estate.usage_years, stat_dyn_loadmanagement_results[9], dyn_Stromtarife_results[9])
                    request.session['opt_querschnitt'] = number_format(verlustleistung_results[0])
                    request.session['opt_cable_costs'] = number_format(verlustleistung_results[1])
                    request.session['opt_verlustleistungscosts'] = number_format(verlustleistung_results[2])
                    request.session['opt_min_costs'] = number_format(verlustleistung_results[3])
                    request.session['cable_costs_1_5mm'] = number_format(verlustleistung_results[4])
                    request.session['verlustleistung_costs_1_5mm'] = number_format(verlustleistung_results[5])
                    request.session['costs_1_5mm'] = number_format(verlustleistung_results[6])
                    
                    #Calculate Steuerbare Verbrauchseinrichtung
                    sve_results = get_sve_results(real_estate.driving_profile)
                    request.session['jahres_stromverbrauch'] = number_format(sve_results[0])
                    request.session['sve_einsparung_monat'] = number_format(sve_results[1])
                    request.session['sve_einsparung_jahr'] = number_format(sve_results[2])

                    #Update PV
                    pv_storage_results = get_pv_storage_results(request.session['battery_capacity'], request.session['roof_size'], request.session['roof_tilt'], request.session['roof_orientation'], request.session['solar_radiation'], request.session['electricity_consumption_year_number'], request.session['driving_profile'], request.session['arrival_time'], request.session['departure_time'])
                    request.session['pv_kW_peak'] = number_format(pv_storage_results[0])
                    request.session['battery_kWh'] = number_format(pv_storage_results[1])
                    request.session['pv_investment_cost_eur'] = number_format(pv_storage_results[2])
                    request.session['battery_investment_cost_eur'] = number_format(pv_storage_results[3])
                    request.session['capex_pv_und_battery'] = number_format(pv_storage_results[4])
                    request.session['battery_status'] = pv_storage_results[5]
                    request.session['electricity_pv_generation_day'] = number_format(pv_storage_results[6])
                    request.session['electricity_consumption_day'] = number_format(pv_storage_results[7])
                    request.session['electricity_sold_grid'] = number_format(pv_storage_results[8])
                    request.session['electricity_saved'] = number_format(pv_storage_results[9])
                    request.session['quote_pv_nutzung'] = number_format(pv_storage_results[10])
                    request.session['quote_eigenversorgung'] = number_format(pv_storage_results[11])
                    request.session['einnahmen_tag'] = number_format(pv_storage_results[12])
                    request.session['einnahmen_jahr'] = number_format(pv_storage_results[13])
                    request.session['gewinn_10_jahre'] = number_format(pv_storage_results[14])
                    request.session['pv_speicher_sinnvoll'] = pv_storage_results[15]
                    request.session['ev_connected_time'] = pv_storage_results[16]
                    request.session['ev_deconnected_time'] = pv_storage_results[17]
                    request.session['ev_needed_electricity_kWh'] = number_format(pv_storage_results[18])
                    request.session['ev_charged_electricity'] = number_format(pv_storage_results[19])
                                        
                    return redirect('db_load_management.html')
            else: 
                form = Real_estateForm()
            return render(request, 'input_form_house.html', {'form': form})                      
            
        context['segment'] = load_template


        if load_template == 'input_form_PV.html':
            if request.method == "POST":  
                form = Lokal_EnergyForm(request.POST)  
                if form.is_valid():
                    lokal_energy = form.save(commit=False)   
                    lokal_energy.person = request.user.username
                    lokal_energy.pub_date = timezone.now()   
                    lokal_energy.save()                                 
                    #Save Results as Session Variable
                    #Otherwise they would need to stand in the url
                   
                    request.session['roof_size'] = lokal_energy.roof_size
                    request.session['roof_tilt'] = lokal_energy.roof_tilt
                    request.session['roof_orientation'] = lokal_energy.roof_orientation
                    request.session['solar_radiation'] = lokal_energy.solar_radiation
                    request.session['battery_capacity'] = lokal_energy.battery_capacity
                    
                    #Calculated values
                    pv_storage_results = get_pv_storage_results(lokal_energy.battery_capacity, lokal_energy.roof_size, lokal_energy.roof_tilt, lokal_energy.roof_orientation, lokal_energy.solar_radiation, request.session['electricity_consumption_year_number'], request.session['driving_profile'], request.session['arrival_time'], request.session['departure_time'])

                    request.session['pv_kW_peak'] = number_format(pv_storage_results[0])
                    request.session['battery_kWh'] = number_format(pv_storage_results[1])
                    request.session['pv_investment_cost_eur'] = number_format(pv_storage_results[2])
                    request.session['battery_investment_cost_eur'] = number_format(pv_storage_results[3])
                    request.session['capex_pv_und_battery'] = number_format(pv_storage_results[4])
                    request.session['battery_status'] = pv_storage_results[5]
                    request.session['electricity_pv_generation_day'] = number_format(pv_storage_results[6])
                    request.session['electricity_consumption_day'] = number_format(pv_storage_results[7])
                    request.session['electricity_sold_grid'] = number_format(pv_storage_results[8])
                    request.session['electricity_saved'] = number_format(pv_storage_results[9])
                    request.session['quote_pv_nutzung'] = number_format(pv_storage_results[10])
                    request.session['quote_eigenversorgung'] = number_format(pv_storage_results[11])
                    request.session['einnahmen_tag'] = number_format(pv_storage_results[12])
                    request.session['einnahmen_jahr'] = number_format(pv_storage_results[13])
                    request.session['gewinn_10_jahre'] = number_format(pv_storage_results[14])
                    request.session['pv_speicher_sinnvoll'] = pv_storage_results[15]
                    request.session['ev_connected_time'] = pv_storage_results[16]
                    request.session['ev_deconnected_time'] = pv_storage_results[17]
                    request.session['ev_needed_electricity_kWh'] = number_format(pv_storage_results[18])
                    request.session['ev_charged_electricity'] = number_format(pv_storage_results[19])
                    
                    return redirect('db_renewables.html')
            else: 
                form = Lokal_EnergyForm()
            return render(request, 'input_form_PV.html', {'form': form})  
                    
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

def get_stat_dyn_loadmanagement(electricity_consumption_year, number_properties, warm_water_heating, house_connection_power, charging_points_to_install, driving_profile, arrival_time, departure_time):
    print("---get_stat_dyn_loadmanagement")
    #Declare variables
    #EV
    hours_to_charge = 0
    needed_electricity_ev_day = 0
    ###Stat. Variables for calculation
    stat_Leistungs_peak_ohne_ev_kW = 0
    stat_verfuegbare_ladeleistung_fuer_alle_wallboxen = 0
    stat_verfuegbare_ladeleistung_fuer_wallbox = 0
    ###Result stat Lastmanagement
    stat_needed_time_to_charge = 0
    stat_loadmanagement_max_evs_to_charge = 0
    
    ########################################
    ###Dyn. Lastmanagement Variables for calculation
    dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen = 0
    dyn_verfuegbare_ladeleistung_fuer_wallbox = 0
    ###Result stat Lastmanagement
    dyn_needed_time_to_charge = 0
    dyn_loadmanagement_max_evs_to_charge = 0
    ###Result Lastmanagement
    opt_lastmanagement = 'Kein Lastmanagement'

    #calculate
    ##Statisches Lastmanagement
    ###Take values from table
    if int(number_properties) == 1:
        if(warm_water_heating == 'ohne Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 14.5
        elif(warm_water_heating == 'mit Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 34
    elif int(number_properties) == 5:
        if(warm_water_heating == 'ohne Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 41
        elif(warm_water_heating == 'mit Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 81
    elif int(number_properties) == 10:
        if(warm_water_heating == 'ohne Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 55
        elif(warm_water_heating == 'mit Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 107
    elif int(number_properties) == 20:
        if(warm_water_heating == 'ohne Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 72
        elif(warm_water_heating == 'mit Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 134
    elif int(number_properties) == 30:
        if(warm_water_heating == 'ohne Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 82
        elif(warm_water_heating == 'mit Strom'):
            stat_Leistungs_peak_ohne_ev_kW = 153
   
    #Calculate available Leistung
    stat_verfuegbare_ladeleistung_fuer_alle_wallboxen = round((float(house_connection_power) - float(stat_Leistungs_peak_ohne_ev_kW)),2)
    stat_verfuegbare_ladeleistung_fuer_wallbox = round(((float(stat_verfuegbare_ladeleistung_fuer_alle_wallboxen) / float(charging_points_to_install))),2)
    if float(stat_verfuegbare_ladeleistung_fuer_alle_wallboxen) < 0:
        stat_verfuegbare_ladeleistung_fuer_alle_wallboxen = 0

    if float(stat_verfuegbare_ladeleistung_fuer_wallbox) < 0:
        stat_verfuegbare_ladeleistung_fuer_wallbox = 0
    
    #Calculate for EV 
    if arrival_time != "Home Office" and departure_time != "Home Office":
        hours_to_charge = (24-int(arrival_time)) + int(departure_time)
    else:
        hours_to_charge = 24 
      
    
    needed_electricity_ev_day = round((int(driving_profile)*0.2),2)

    #Result for stat Loadmanagement
    if int(stat_verfuegbare_ladeleistung_fuer_wallbox != 0):
        stat_needed_time_to_charge = round(((float(needed_electricity_ev_day)/float(stat_verfuegbare_ladeleistung_fuer_wallbox))),2)
        stat_loadmanagement_max_evs_to_charge = round((hours_to_charge/stat_needed_time_to_charge),2)
    
        if int(stat_needed_time_to_charge > hours_to_charge):
            stat_needed_time_to_charge = "-"
            stat_loadmanagement_max_evs_to_charge = 0
    else: 
        stat_needed_time_to_charge = "-"
        stat_loadmanagement_max_evs_to_charge = 0

    ################################################################
    #Dynamisches Lastmanagement

    #Rechnung: Summiere Differenz aus Leistungsnachfrage und Hausanschluss
    #Auflösung: Stündliche Leistungswerte aus Standardlastprofil
    electricity_consumption_day_kWh = round(((int(electricity_consumption_year)*int(number_properties))/365),3)       
    #Stromverbauch nach Standardlastprofil für gesamte Immobilie
    #array leistungsnachfrage stündlich
    ln_h = [round((0.0197*electricity_consumption_day_kWh),3), round((0.0168*electricity_consumption_day_kWh),3), round((0.0160*electricity_consumption_day_kWh),3), round((0.0160*electricity_consumption_day_kWh),3), round((0.0160*electricity_consumption_day_kWh),3), round((0.0219*electricity_consumption_day_kWh),3), round((0.0437*electricity_consumption_day_kWh),3), round((0.0518*electricity_consumption_day_kWh),3), round((0.0539*electricity_consumption_day_kWh),3), round((0.0481*electricity_consumption_day_kWh),3), round((0.0466*electricity_consumption_day_kWh),3), round((0.0466*electricity_consumption_day_kWh),3), round((0.0510*electricity_consumption_day_kWh),3), round((0.0474*electricity_consumption_day_kWh),3), round((0.0437*electricity_consumption_day_kWh),3), round((0.0401*electricity_consumption_day_kWh),3), round((0.0437*electricity_consumption_day_kWh),3), round((0.0547*electricity_consumption_day_kWh),3), round((0.062*electricity_consumption_day_kWh),3), round((0.0729*electricity_consumption_day_kWh),3), round((0.062*electricity_consumption_day_kWh),3), round((0.051*electricity_consumption_day_kWh),3), round((0.0437*electricity_consumption_day_kWh),3), round((0.0306*electricity_consumption_day_kWh),3)]
    dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen = round((((int(house_connection_power) - ln_h[0]) + (int(house_connection_power) - ln_h[1]) + (int(house_connection_power) - ln_h[2]) + (int(house_connection_power) - ln_h[3]) + (int(house_connection_power) - ln_h[4]) + (int(house_connection_power) - ln_h[5]) + (int(house_connection_power) - ln_h[6]) + (int(house_connection_power) - ln_h[7]) + (int(house_connection_power) - ln_h[8]) + (int(house_connection_power) - ln_h[9]) + (int(house_connection_power) - ln_h[10])+ (int(house_connection_power) - ln_h[11]) + (int(house_connection_power) - ln_h[12]) + (int(house_connection_power) - ln_h[13]) + (int(house_connection_power) - ln_h[14]) + (int(house_connection_power) - ln_h[15]) + (int(house_connection_power) - ln_h[16]) + (int(house_connection_power) - ln_h[17]) + (int(house_connection_power) - ln_h[18]) + (int(house_connection_power) - ln_h[19]) + (int(house_connection_power) - ln_h[20]) + (int(house_connection_power) - ln_h[21]) + (int(house_connection_power) - ln_h[22]) + (int(house_connection_power) - ln_h[23]))/24),2)
    dyn_verfuegbare_ladeleistung_fuer_wallbox = round((dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen/int(charging_points_to_install)), 2)
    
    if float(dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen) < 0:
        dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen = 0
    if float(dyn_verfuegbare_ladeleistung_fuer_wallbox) < 0:
        dyn_verfuegbare_ladeleistung_fuer_wallbox = 0

    if int(dyn_verfuegbare_ladeleistung_fuer_wallbox != 0):
        dyn_needed_time_to_charge = round(((float(needed_electricity_ev_day)/float(dyn_verfuegbare_ladeleistung_fuer_wallbox))),2)
        dyn_loadmanagement_max_evs_to_charge = round((hours_to_charge/dyn_needed_time_to_charge),2)
    
        if int(dyn_needed_time_to_charge > hours_to_charge):
            dyn_needed_time_to_charge = "-"
            dyn_loadmanagement_max_evs_to_charge = 0
    else: 
        dyn_needed_time_to_charge = "-"
        dyn_loadmanagement_max_evs_to_charge = 0
    
    #Result wich Loadmanagement
    if float(stat_verfuegbare_ladeleistung_fuer_wallbox >= 11):
        opt_lastmanagement = 'kein Lastmanagement'
    elif float(stat_verfuegbare_ladeleistung_fuer_wallbox < 11 and dyn_needed_time_to_charge != "-"):
        opt_lastmanagement = 'ein Lastmanagement'
    else:
        opt_lastmanagement = 'eine Netzanschlusserweiterung'
     
    loadmanagement_results = [hours_to_charge, needed_electricity_ev_day, stat_Leistungs_peak_ohne_ev_kW, stat_verfuegbare_ladeleistung_fuer_alle_wallboxen, stat_verfuegbare_ladeleistung_fuer_wallbox, stat_needed_time_to_charge, stat_loadmanagement_max_evs_to_charge, opt_lastmanagement, dyn_verfuegbare_ladeleistung_fuer_alle_wallboxen, dyn_verfuegbare_ladeleistung_fuer_wallbox, dyn_needed_time_to_charge, dyn_loadmanagement_max_evs_to_charge]
    return loadmanagement_results


def get_optimal_verlustleistung(cable_length, driving_profile, usage_years, dyn_verfuegbare_ladeleistung_fuer_wallbox, opt_arbeitspreis_eur):
    #Die Ladeleistung wird durch das dynamische Lastamanagement vorgegeben
    #Sollte ein Netzausbau notwendig sein, wird als Ladeleistung 11 kW angenommen
    if dyn_verfuegbare_ladeleistung_fuer_wallbox == 0:
        dyn_verfuegbare_ladeleistung_fuer_wallbox = 11
    verlustleistung_costs_1_5mm = round(((((768*int(cable_length))/(56*1.5)) * ((int(driving_profile)*73)/(float(dyn_verfuegbare_ladeleistung_fuer_wallbox)*1000)) * (opt_arbeitspreis_eur*int(usage_years)))), 2)
    verlustleistung_costs_2_5mm = round(((((768*int(cable_length))/(56*2.5)) * ((int(driving_profile)*73)/(float(dyn_verfuegbare_ladeleistung_fuer_wallbox)*1000)) * (opt_arbeitspreis_eur*int(usage_years)))), 2)
    verlustleistung_costs_4mm = round(((((768*int(cable_length))/(56*4)) * ((int(driving_profile)*73)/(float(dyn_verfuegbare_ladeleistung_fuer_wallbox)*1000)) * (opt_arbeitspreis_eur*int(usage_years)))), 2)
    verlustleistung_costs_6mm = round(((((768*int(cable_length))/(56*6)) * ((int(driving_profile)*73)/(float(dyn_verfuegbare_ladeleistung_fuer_wallbox)*1000)) * (opt_arbeitspreis_eur*int(usage_years)))), 2)
    verlustleistung_costs_10mm = round(((((768*int(cable_length))/(56*10)) * ((int(driving_profile)*73)/(float(dyn_verfuegbare_ladeleistung_fuer_wallbox)*1000)) * (opt_arbeitspreis_eur*int(usage_years)))), 2)
    verlustleistung_costs_16mm = round(((((768*int(cable_length))/(56*16)) * ((int(driving_profile)*73)/(float(dyn_verfuegbare_ladeleistung_fuer_wallbox)*1000)) * (opt_arbeitspreis_eur*int(usage_years)))), 2)
    
    verlustleistungscosts = [verlustleistung_costs_1_5mm, verlustleistung_costs_2_5mm, verlustleistung_costs_4mm, verlustleistung_costs_6mm, verlustleistung_costs_10mm, verlustleistung_costs_16mm]

    cable_costs_1_5mm = round( (1*int(cable_length)), 2)
    cable_costs_2_5mm = round((1.6*int(cable_length)), 2)
    cable_costs_4mm = round((3.5*int(cable_length)), 2)
    cable_costs_6mm = round((4.7*int(cable_length)), 2)
    cable_costs_10mm = round((7.4*int(cable_length)), 2)
    cable_costs_16mm = round((12*int(cable_length)), 2)
    cable_costs = [cable_costs_1_5mm, cable_costs_2_5mm, cable_costs_4mm, cable_costs_6mm, cable_costs_10mm, cable_costs_16mm]
    
    complete_costs = [round((verlustleistung_costs_1_5mm+cable_costs_1_5mm),2), round((verlustleistung_costs_2_5mm+cable_costs_2_5mm),2), round((verlustleistung_costs_4mm+cable_costs_4mm),2), round((verlustleistung_costs_6mm+cable_costs_6mm),2), round((verlustleistung_costs_10mm+cable_costs_10mm),2), round((verlustleistung_costs_16mm+cable_costs_16mm),2)]
    
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
    print("----------get_sve_results")
    jahres_stromverbrauch = round((int(driving_profile)*0.2*365),2)
    sve_einsparung_monat = round(((int(driving_profile)*0.2*0.03*30)-1.66), 2)
    sve_einsparung_jahr = round(((int(driving_profile)*0.2*0.03*365)-1.66), 2)
    result = [jahres_stromverbrauch, sve_einsparung_monat, sve_einsparung_jahr]
    return result

def get_dyn_stromtarife_results(driving_profile, electricity_consumption_year, dyn_needed_time_to_charge, arrival_time, departure_time):
    print("Stromtarife")
    #Declare variables
    electricity_consumption_month_ev = 0
    #Haus
    electricity_consumption_month_house = 0
    hausstrom_electricity_cost_month_house = 0
    #Haus und EV
    hausstrom_electricity_cost_month_ev_house = 0
    ladestrom_electricity_cost_month_ev = 0
    ladestrom_electricity_cost_month_ev_house = 0
    dyn_strom_electricity_cost_month_ev = 0
    dyn_strom_electricity_cost_month_ev_house = 0

    #Strom nur Haus
    electricity_consumption_month_house = round((electricity_consumption_year/12),2)
    hausstrom_electricity_cost_month_house = round(((electricity_consumption_month_house*0.4778)+10.20),2)
    #Strom Haus und EV
    electricity_consumption_month_ev = (int(driving_profile)*30.5*0.2)
    #Grundgebuhr + Arbeitspreis Stromverbrauch EV und Haus
    hausstrom_electricity_cost_month_ev_house = round((((electricity_consumption_month_ev + (electricity_consumption_year/12)) *0.4754)+10.20),2)
    #Strom Ladestrom: 
    ladestrom_electricity_cost_month_ev = round(((electricity_consumption_month_ev *0.4409)+12.89+1.66),2)
    ladestrom_electricity_cost_month_ev_house = round((ladestrom_electricity_cost_month_ev+hausstrom_electricity_cost_month_house),2)
       
    #Strom Dynamisch
    #Array mit den stümdlichen durchschnittspreisen
    array_hourly_prices = [7.376, 6.941, 6.685, 6.464, 6.564, 7.060, 8.608, 10.035, 10.538, 9.821, 9.027, 8.553, 8.041, 7.439, 7.224, 7.576, 8.239, 9.778, 10.872, 11.332, 10.527, 9.452, 8.866, 7.753]
    #Array bereinigt um die Stunden, in denen das Auto nicht angeschlossen ist
    #Bsp. 17 Uhr, 8 Uhr (-> lösche alles zwischen 8 und 17 Uhr -> Index 7 bis 16)
    #Wenn Wert gelöscht verschiebt sich index um eins, daher im For Loop immer gleichen Index löschen
    ev_connected_hourly_prices = [7.376, 6.941, 6.685, 6.464, 6.564, 7.060, 8.608, 10.035, 10.538, 9.821, 9.027, 8.553, 8.041, 7.439, 7.224, 7.576, 8.239, 9.778, 10.872, 11.332, 10.527, 9.452, 8.866, 7.753]
    if arrival_time != "Home Office" and departure_time != "Home Office":
        for x in range((int(departure_time)-1), (int(arrival_time)-1)):
            ev_connected_hourly_prices.pop((int(departure_time)-1))
    print("hier noch alles gut")
    #Anzahl der zu ladenden Stunden
    print(dyn_needed_time_to_charge) 

    if dyn_needed_time_to_charge == "-":
        dyn_needed_time_to_charge = round(((int(driving_profile)*0.2)/11), 2)
    
  

    if arrival_time != "Home Office" and departure_time != "Home Office":
        round_up_dyn_needed_time_to_charge = round((dyn_needed_time_to_charge+0.5),0)
    else: 
        round_up_dyn_needed_time_to_charge = 24
    
    #Es wird der Durchschnittspreis der zu ladenden Stunden gebildet
    dyn_electricity_price__kWh_cent = 0
    avg_dyn_electricity_price = 0
    #Aufsummieren der Preise
    for x in range(0, int(round_up_dyn_needed_time_to_charge)):
        ev_connected_hourly_prices.sort()
        avg_dyn_electricity_price = avg_dyn_electricity_price + ev_connected_hourly_prices[0]
        ev_connected_hourly_prices.pop(0)
    #Bilden des Durchschnitts
    avg_dyn_electricity_price = avg_dyn_electricity_price/int(round_up_dyn_needed_time_to_charge)
    #Baiserend auf dem var. Strompreis wird der monatliche Strompreis gebildet
    dyn_electricity_price__kWh_cent = round((avg_dyn_electricity_price+18.12+0.25),2)
    # Zuzuueglich dem extra Stromzähler
    dyn_strom_electricity_cost_month_ev = round((((dyn_electricity_price__kWh_cent*electricity_consumption_month_ev)/100)+13.99),2) 
    dyn_strom_electricity_cost_month_ev_house = round((dyn_strom_electricity_cost_month_ev+hausstrom_electricity_cost_month_house),2)

    
    stromtarife = [hausstrom_electricity_cost_month_ev_house, ladestrom_electricity_cost_month_ev_house, dyn_strom_electricity_cost_month_ev_house]
    
    opt_tarif_index = 0
    opt_tarif = stromtarife[0]
    for i in range(len(stromtarife)):
        if opt_tarif > stromtarife[i]:
            opt_tarif_index = i
    opt_arbeitspreis_eur = 0
    if opt_tarif_index == 0:
        opt_tarif = "Haushaltsstrom"
        opt_arbeitspreis_eur = 0.4754
    elif opt_tarif_index ==1:
        opt_tarif = "Ladestrom"
        opt_arbeitspreis_eur = 0.4409
    elif opt_tarif_index ==2:
        opt_tarif = "dynamischer Stromtarif"
        opt_arbeitspreis_eur = round((dyn_electricity_price__kWh_cent/100),2)


    dyn_Stromtarife_results = [electricity_consumption_month_house, electricity_consumption_month_ev, hausstrom_electricity_cost_month_house, hausstrom_electricity_cost_month_ev_house, ladestrom_electricity_cost_month_ev, ladestrom_electricity_cost_month_ev_house, dyn_strom_electricity_cost_month_ev, dyn_strom_electricity_cost_month_ev_house, opt_tarif, opt_arbeitspreis_eur]
    return dyn_Stromtarife_results
           
def get_pv_storage_results(battery_capacity, roof_size, roof_tilt, roof_orientation, solar_radiation, electricity_consumption_year, driving_profile, arrival_time, departure_time):
    #calculate results
    # PV: 1, 7, 14 kWpeak
    # Batterie: 4, 6, 9 kWh
    
    #################Szenario 1 kWpeak PV und 1 kWh Speicher
    pv_kW_peak = round((int(roof_size)/6), 0)
    #Annahme Speicher Kapazität gleich kWpeak PV
    battery_kWh = int(battery_capacity)
    #CAPEX PV und Batterie
    pv_investment_cost_eur = round(1852.88*pv_kW_peak,2)
    battery_investment_cost_eur = round(350*battery_kWh,2)
    capex_pv_und_battery = round((pv_investment_cost_eur + battery_investment_cost_eur),2)
    #OPEX PV und Batterie nach Lebenserwartung
    opex_1kW_peak_pv_und_1kWh_battery = 0 #round(((pv_investment_cost_eur/20)+(battery_investment_cost_eur/10)),2)
    #Einnahmen aus gesparten Stromkosten und eigenem Stromverkauf
    
    pv_batterie_calculations = get_pv_storage_values(pv_kW_peak, battery_kWh, solar_radiation, roof_tilt, roof_orientation, electricity_consumption_year, driving_profile, arrival_time, departure_time)
    battery_status = round(pv_batterie_calculations[0],2)
    electricity_pv_generation_day = round(pv_batterie_calculations[1],2)
    electricity_consumption_day = round(pv_batterie_calculations[2],2)
    electricity_sold_grid = round(pv_batterie_calculations[3],2)
    electricity_saved = round(pv_batterie_calculations[4],2)
    ev_connected_time = pv_batterie_calculations[5]
    ev_deconnected_time = pv_batterie_calculations[6]
    ev_needed_electricity_kWh = round(pv_batterie_calculations[7],2)
    ev_charged_electricity = round(pv_batterie_calculations[8],2)

    quote_pv_nutzung = round((1-(electricity_sold_grid/electricity_pv_generation_day))*100,0)
    quote_eigenversorgung = round(((electricity_saved/electricity_consumption_day)*100),0)
    einnahmen_tag = round((electricity_sold_grid*0.068+(electricity_saved+battery_status+ev_charged_electricity)*0.30),2)
    einnahmen_jahr = round(einnahmen_tag*365,2)
    gewinn_10_jahre = round(((10*((einnahmen_tag*365)-opex_1kW_peak_pv_und_1kWh_battery))-capex_pv_und_battery),2)
    if gewinn_10_jahre > 0:
        pv_speicher_sinnvoll = "sinnvoll"
    else:
        pv_speicher_sinnvoll = "nicht sinnvoll"
    

    results_pv_battery = [
        pv_kW_peak,
        battery_kWh,
        pv_investment_cost_eur,
        battery_investment_cost_eur, 
        capex_pv_und_battery,
        battery_status,
        electricity_pv_generation_day,
        electricity_consumption_day,
        electricity_sold_grid,
        electricity_saved,
        quote_pv_nutzung,
        quote_eigenversorgung,
        einnahmen_tag,
        einnahmen_jahr,
        gewinn_10_jahre,
        pv_speicher_sinnvoll, 
        ev_connected_time, 
        ev_deconnected_time,
        ev_needed_electricity_kWh,
        ev_charged_electricity
        ]
    return results_pv_battery
   
def get_pv_storage_values(pv_kW_peak, battery_kWh, solar_radiation, roof_tilt, roof_orientation, electricity_consumption_year, driving_profile, arrival_time, departure_time):
    #Berechnen der PV Stromerzeugung
    electricity_pv_generation_year = get_electricity_generation_year(pv_kW_peak, solar_radiation, roof_tilt, roof_orientation)
    electricity_pv_generation_day= (electricity_pv_generation_year/365)
    #Berechnung des Stromverbrauches der Immobilie
    electricity_consumption_day = electricity_consumption_year/365
    #Array mit stündlichen Erzeugungs- und Verbrauchswerten
    list_electricity_generation_day = [0, 0, 0, 0, 0, 0, 0, round((0.01*electricity_pv_generation_day),3), round((0.02*electricity_pv_generation_day),3), round((0.05*electricity_pv_generation_day),3), round((0.08*electricity_pv_generation_day), 3), round((0.11*electricity_pv_generation_day), 3), round((0.12*electricity_pv_generation_day), 3), round((0.13*electricity_pv_generation_day), 3), round((0.13*electricity_pv_generation_day), 3), round((0.12*electricity_pv_generation_day), 3), round((0.10*electricity_pv_generation_day), 3), round((0.08*electricity_pv_generation_day), 3), round((0.04*electricity_pv_generation_day), 3), round((0.01*electricity_pv_generation_day), 3), 0, 0, 0, 0]
    list_electricity_consumption_day = [round((0.0197*electricity_consumption_day), 3), round((0.0168*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0160*electricity_consumption_day), 3), round((0.0219*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0518*electricity_consumption_day), 3), round((0.0539*electricity_consumption_day), 3), round((0.0481*electricity_consumption_day), 3), round((0.0466*electricity_consumption_day), 3), round((0.0466*electricity_consumption_day), 3), round((0.0510*electricity_consumption_day), 3), round((0.0474*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0401*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0547*electricity_consumption_day), 3), round((0.062*electricity_consumption_day), 3), round((0.0729*electricity_consumption_day), 3), round((0.062*electricity_consumption_day), 3), round((0.051*electricity_consumption_day), 3), round((0.0437*electricity_consumption_day), 3), round((0.0306*electricity_consumption_day), 3)]
    #Initilisieren
    battery_status = 0 
    ueberschuss_energie = 0
    electricity_sold_grid = 0
    electricity_saved = 0
    #Wann kann das Auto geladen werden -> extra wegen Home Office
    if departure_time == "Home Office" or arrival_time == "Home Office":
        ev_connected_time = 0
        ev_deconnected_time = 24
    else: 
        ev_connected_time = departure_time
        ev_deconnected_time = arrival_time
        
   
    ev_needed_electricity_kWh = round(int(driving_profile)*0.2,2)
    ev_charged_electricity = 0
    print("----------------------------PV------------------------------")
    #Für jede Stunde am Tag
    for i in range(len(list_electricity_consumption_day)):
        #Wenn die PV Erzeugung den Hausverbrauch übersteigt -> speichern oder verkaufen // oder EV laden
        if list_electricity_consumption_day[i] < list_electricity_generation_day[i]:
            #PV dominant
            #Eigenverbrauch gedeckt
            electricity_saved = electricity_saved + list_electricity_consumption_day[i]
            
            #Überschussstrom 1. versuchen EV laden, 2. Speicher, 3. verkaufen
            #Auto laden wenn es angeschlossen ist
            #Wenn Home Office, kann immer geladen werden
            if departure_time == "Home Office" or arrival_time == "Home Office":
                #Wenn EV noch nicht voll, dann laden
                if ev_charged_electricity < ev_needed_electricity_kWh:
                    #Die Batterie nur soweit laden, bis Sie voll ist, sonst Strom verkaufen
                    if (list_electricity_generation_day[i]-list_electricity_consumption_day[i]) < (ev_needed_electricity_kWh-ev_charged_electricity):
                        ev_charged_electricity = ev_charged_electricity + (list_electricity_generation_day[i]-list_electricity_consumption_day[i])
                    else:
                        #ueberschuss energie, die nicht mehr in EV gespeichert werden kann.
                        #Verfuegbarer Strom der Stunde - Restkapazität Batterie
                        ueberschuss_energie_ev = (list_electricity_generation_day[i]-list_electricity_consumption_day[i])-(ev_needed_electricity_kWh-ev_charged_electricity)
                        ev_charged_electricity = ev_needed_electricity_kWh
                        #ueberschuss_energie_ev
                        print("EV Überschuss")
                        print(ueberschuss_energie_ev)
                #Wenn Batterie noch nicht voll, dann laden
                elif battery_status < battery_kWh:
                    #Die Batterie nur soweit laden, bis Sie voll ist, sonst Strom verkaufen
                    if (list_electricity_generation_day[i]-list_electricity_consumption_day[i]) < (battery_kWh-battery_status):
                        battery_status = battery_status + (list_electricity_generation_day[i]-list_electricity_consumption_day[i])
                    else:
                        #ueberschuss energie, die nicht mehr in Batterie gespeichert werden kann.
                        #Verfuegbarer Strom der Stunde - Restkapazität Batterie
                        ueberschuss_energie = (list_electricity_generation_day[i]-list_electricity_consumption_day[i])-(battery_kWh-battery_status)
                        battery_status = battery_kWh
                        print("Batterie Überschuss")
                        print(ueberschuss_energie)
                #Sonst ins Netz verkaufen
                else:
                    electricity_sold_grid = electricity_sold_grid + ueberschuss_energie_ev+ ueberschuss_energie + (list_electricity_generation_day[i]- list_electricity_consumption_day[i])
                    #Überschuss verrechnet
                    ueberschuss_energie_ev = 0
                    ueberschuss_energie = 0

            #Wenn die Uhrzeit i=0 -> 1 Uhr vor der Abfahrtszeit oder nach der Ankunftszeit liegt, laden
            #Wenn EV um 8 Uhr losfährt, kann es bis i < 7 laden
            #Wenn EV um 17 Uhr wiederkommt, kann es ab i >= 16 laden
            elif i < (int(departure_time)-1) or i >= (int(arrival_time)-1):
                #Wenn EV noch nicht voll, dann laden
                if ev_charged_electricity < ev_needed_electricity_kWh:
                    #Die Batterie nur soweit laden, bis Sie voll ist, sonst Strom verkaufen
                    if (list_electricity_generation_day[i]-list_electricity_consumption_day[i]) < (ev_needed_electricity_kWh-ev_charged_electricity):
                        ev_charged_electricity = ev_charged_electricity + (list_electricity_generation_day[i]-list_electricity_consumption_day[i])
                    else:
                        #ueberschuss energie, die nicht mehr in EV gespeichert werden kann.
                        #Verfuegbarer Strom der Stunde - Restkapazität Batterie
                        ueberschuss_energie_ev = (list_electricity_generation_day[i]-list_electricity_consumption_day[i])-(ev_needed_electricity_kWh-ev_charged_electricity)
                        ev_charged_electricity = ev_needed_electricity_kWh
                        print("EV Überschuss")
                        print(ueberschuss_energie_ev)
                #Wenn Batterie noch nicht voll, dann laden
                elif battery_status < battery_kWh:
                    #Die Batterie nur soweit laden, bis Sie voll ist, sonst Strom verkaufen
                    if (list_electricity_generation_day[i]-list_electricity_consumption_day[i]) < (battery_kWh-battery_status):
                        battery_status = battery_status + (list_electricity_generation_day[i]-list_electricity_consumption_day[i])
                    else:
                        #ueberschuss energie, die nicht mehr in Batterie gespeichert werden kann.
                        #Verfuegbarer Strom der Stunde - Restkapazität Batterie
                        ueberschuss_energie = (list_electricity_generation_day[i]-list_electricity_consumption_day[i])-(battery_kWh-battery_status)
                        battery_status = battery_kWh
                        print("EV Überschuss")
                        print(ueberschuss_energie)
                #Sonst ins Netz verkaufen
                else:
                    print("verkaufe Strom ins Netz")
                    electricity_sold_grid = electricity_sold_grid + ueberschuss_energie + (list_electricity_generation_day[i]- list_electricity_consumption_day[i])
                    #Überschuss verrechnet
                    ueberschuss_energie = 0


            #Auto gerade nicht angeschlossen
            else:
                #Wenn Batterie noch nicht voll, dann laden
                if battery_status < battery_kWh:
                    #Die Batterie nur soweit laden, bis Sie voll ist, sonst Strom verkaufen
                    if (list_electricity_generation_day[i]-list_electricity_consumption_day[i]) < (battery_kWh-battery_status):
                        battery_status = battery_status + (list_electricity_generation_day[i]-list_electricity_consumption_day[i])
                    else:
                        #ueberschuss energie, die nicht mehr in Batterie gespeichert werden kann.
                        #Verfuegbarer Strom der Stunde - Restkapazität Batterie
                        ueberschuss_energie = (list_electricity_generation_day[i]-list_electricity_consumption_day[i])-(battery_kWh-battery_status)
                        battery_status = battery_kWh
                        print("Batterie voll")
                        print(ueberschuss_energie)
                #Sonst ins Netz verkaufen
                else:
                    electricity_sold_grid = electricity_sold_grid + ueberschuss_energie + (list_electricity_generation_day[i]- list_electricity_consumption_day[i])
                    #Überschuss verrechnet
                    ueberschuss_energie = 0
        #Wenn Verbrauch Immobilie, PV Erzeugung nicht übersteigt, dann selber verbrauchen
        else:
            electricity_saved = electricity_saved + list_electricity_generation_day[i]
    
    
    result = [
        battery_status, 
        electricity_pv_generation_day, 
        electricity_consumption_day, 
        electricity_sold_grid, 
        electricity_saved,
        ev_connected_time, 
        ev_deconnected_time,
        ev_needed_electricity_kWh,
        ev_charged_electricity
        ]
    return result

    
def get_electricity_consumption_year(property_type, number_properties, water_heating, number_persons):
    print("---get_electricity_consumption_year")
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

    result = round((result*int(number_properties)),2)
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
   
    result = round((int(kw_peak)*int(solar_radiation)*factor_tilt_orientation*0.8335), 2)
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