from collections import deque
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponse


from app.estate_mgt.models import *
from app.user.decorators import is_estate_manager, is_tenant, is_security
from app.user.models import User, RoleManagement
from app.vistor_mgt.models import NewVistor

# Create your views here.

ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = getattr(
    settings, 'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS', False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR','')
    if x_forwarded_for:
        ip = x_forwarded_for
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def __country_name(request):
    ip_address = get_client_ip(request)
    post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
    response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
    geodata = response.json()
    return geodata['country_name']

def __country_code(request):
    ip_address = get_client_ip(request)
    post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
    response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
    geodata = response.json()
    return geodata['country_code']

def __ip_address(request):
    ip_address = get_client_ip(request)
    post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
    response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
    geodata = response.json()
    return geodata['ip']

def __state(request):
    ip_address = get_client_ip(request)
    post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
    response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
    geodata = response.json()
    return geodata['city']

def home(request):
    return render(request, 'site/home.html')

@csrf_exempt
@login_required()
def redirect_user(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    data = {'site_url':site_url, 'site_name': site_name}

    if request.user.role.pk == 1:
        return redirect('site_mgt:estate_manager_dashboard')
    elif request.user.role.pk == 2:
        return redirect('site_mgt:landlord_dashboard')
    elif request.user.role.pk == 3:
        return redirect('site_mgt:tenant_dashboard')
    elif request.user.role.pk == 4:
        return redirect('site_mgt:security_dashboard')

@login_required
@is_estate_manager
def estate_manager_dashboard(request):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    all_buildings = Building.objects.filter(street__in=all_streets)
    all_apartments = Apartment.objects.filter(street__in=all_streets)
    all_titles = Salutation.objects.order_by('date_created')
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    estate_members = User.objects.all().filter(estate=request.user.estate).count()

    if request.method == 'POST':
        estate = Estate.objects.get(estate_name=request.user.estate)
        vistor_first_name = request.POST.get('vistor_first_name')
        vistor_last_name = request.POST.get('vistor_last_name')
        vistor_mobile_number = request.POST.get('vistor_mobile_number')
        create_invite = NewVistor.objects.create(vistor_first_name=vistor_first_name,vistor_last_name=vistor_last_name,
                                                 vistor_mobile_number=vistor_mobile_number,whom_to_see=request.user, estate=estate)

    data = {'site_url': site_url, 'site_name': site_name, 'estate_members': estate_members,
            'all_streets': all_streets, 'all_buildings': all_buildings, 'all_apartments': all_apartments,
            'all_titles': all_titles}
    return render(request, 'site/estate_manager/dashboard.html', context=data)

@login_required
@is_estate_manager
def estate_members(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    estate = User.objects.all().filter(estate=request.user.estate)
    count = 0
    count_list = []
    for i in estate:
        count += 1
        count_list.append(count)
    estate_members= zip(estate, count_list)

    data = {'site_url': site_url, 'site_name': site_name, 'estate_members':estate_members}
    return render(request, 'site/estate_manager/estate_members.html', context=data)

@login_required
def visitor_log(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    visitor = NewVistor.objects.all().filter(whom_to_see=request.user).order_by('-pk')
    count = 0
    count_list = []
    for i in visitor:
        count += 1
        count_list.append(count)
    visitor_log= zip(visitor, count_list)

    data = {'site_url': site_url, 'site_name': site_name, 'visitor_log':visitor_log}
    return render(request, 'site/dashboard/visitor_log.html', context=data)

@login_required
@is_estate_manager
def estate_visitor_log(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    estate = Estate.objects.get(estate_name=request.user.estate)

    visitor = NewVistor.objects.all().filter(estate=estate).order_by('-pk')
    count = 0
    count_list = []
    for i in visitor:
        count += 1
        count_list.append(count)
    visitor_log= zip(visitor, count_list)

    data = {'site_url': site_url, 'site_name': site_name, 'visitor_log':visitor_log}
    return render(request, 'site/estate_manager/estate_visitor_log.html', context=data)

@login_required
def profile(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')

        if date_of_birth == '':
            date_of_birth = None
        else:
            date_of_birth = request.POST.get('date_of_birth')

        a = []
        if date_of_birth:
            for i in date_of_birth:
                if i == '/':
                    i = '-'
                a.append(i)
            date_list = deque(a)
            date_list.rotate(-6)
            date_list.insert(4,'-')
            date_list.pop()
            date = ''.join(date_list)
        notes = request.POST.get('notes')

        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage(location='media/estate/{}/users/{}/profile_image/'.format(request.user.estate,request.user))
            image_file = fs.save(image.name, image)
            image= 'estate/{}/users/{}/profile_image/{}'.format(request.user.estate,request.user,image_file)

            try:
                update_user = User.objects.filter(pk=request.user.pk).update(first_name=first_name,last_name=last_name,gender=gender,
                                                              date_of_birth=date,notes=notes,image=image)
            except:
                update_user = User.objects.filter(pk=request.user.pk).update(first_name=first_name, last_name=last_name,
                                                                             gender=gender,
                                                                             date_of_birth=date_of_birth, notes=notes,
                                                                             image=image)

        else:
            try:
                update_user = User.objects.filter(pk=request.user.pk).update(first_name=first_name,last_name=last_name,gender=gender,
                                                              date_of_birth=date,notes=notes)
            except:
                update_user = User.objects.filter(pk=request.user.pk).update(first_name=first_name, last_name=last_name,
                                                                             gender=gender,
                                                                             date_of_birth=date_of_birth, notes=notes)

        return redirect('site_mgt:profile')

    data = {'site_url': site_url, 'site_name': site_name}
    return render(request, 'site/dashboard/profile.html', context=data)


@login_required
@is_tenant
def tenant_dashboard(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    estate_members = NewVistor.objects.all().filter(whom_to_see=request.user).count()

    if request.method == 'POST':
        estate = Estate.objects.get(estate_name=request.user.estate)
        vistor_first_name = request.POST.get('vistor_first_name')
        vistor_last_name = request.POST.get('vistor_last_name')
        vistor_mobile_number = request.POST.get('vistor_mobile_number')
        create_invite = NewVistor.objects.create(vistor_first_name=vistor_first_name,vistor_last_name=vistor_last_name,
                                                 vistor_mobile_number=vistor_mobile_number,whom_to_see=request.user, estate=estate)

    data = {'site_url': site_url, 'site_name': site_name, 'estate_members':estate_members}
    return render(request, 'site/tenant/dashboard.html', context=data)


@login_required
@is_security
def security_dashboard(request):
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    check_in = False
    error_check_in = False
    error_check_out = False
    estate = Estate.objects.get(estate_name=request.user.estate)

    visitor = NewVistor.objects.all().filter(estate=estate, checked_in=True).order_by('-checked_in_date')
    count = 0
    count_list = []
    for i in visitor:
        count += 1
        count_list.append(count)
    visitor_log= zip(visitor, count_list)

    if request.method == "POST":

        visitor_code_in = request.POST.get('vistor_code_in')
        visitor_code_out = request.POST.get('vistor_code_out')
        print(visitor_code_in)
        print(visitor_code_out)


        # Verify code and Check in User
        if visitor_code_in is not None:
            try:
                check_visitor = NewVistor.objects.filter(unique_code_is_active=True,checked_in=False ).get(vistor_unique_code=visitor_code_in)
                if check_visitor:
                    check_in_visitor = NewVistor.objects.filter(vistor_unique_code=visitor_code_in).update(checked_in=True,checked_in_date=datetime.now())
                    check_in = True
                    return redirect('site_mgt:security_dashboard')

            except:
                error_check_in = True

        elif visitor_code_out is not None:
            try:
                check_visitor = NewVistor.objects.filter(unique_code_is_active=True,checked_in=True,checked_out=False).get(vistor_unique_code=visitor_code_out)
                if check_visitor:
                    check_in_visitor = NewVistor.objects.filter(vistor_unique_code=visitor_code_out).update(checked_out=True,checked_out_date=datetime.now())
                    return redirect('site_mgt:security_dashboard')

            except:
                error_check_out = True


    data = {'site_url': site_url, 'site_name': site_name, 'visitor_log':visitor_log,
            'error_check_in':error_check_in,'error_check_out':error_check_out,'check_in':check_in}
    return render(request, 'site/security/dashboard.html', context=data)


@login_required
@is_estate_manager
def add_member(request):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    all_estates = Estate.objects.order_by('date_created')
    all_apartments = Apartment.objects.order_by('date_created')
    all_titles = Salutation.objects.order_by('date_created')
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    apk_file = 'http://clanit.herokuapp.com/clannit.apk'
    suc_msg = 2
    try:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile_number = request.POST['mobile_number']
            username = User.objects.make_random_password()
            email = request.POST['email']
            title = request.POST['title']
            first_name = str(title) + " " + str(first_name)
            apassword = User.objects.make_random_password()
            password = make_password(apassword)
            pswd = apassword
            gender = request.POST['gender']
            role = request.POST['role']
            if request.user.is_superuser != 1:
                street = Street.objects.filter(pk=request.POST.get('street', 'Address Would be fixed soon')).first()
                building = Building.objects.filter(pk=request.POST.get('building', 'Address Would be fixed soon')).first()
                address = str(building) + ", " + str(street)
            if role == 4:
                address = "Security Post"
            if request.user.is_superuser == 1:
                estate = request.POST['estate']
            else:
                estate = Estate.objects.get(pk=request.user.estate_id)
            rolex = RoleManagement.objects.get(pk=role)
            country = __country_name(request)
            country_short = __country_code(request)
            ip_address = __ip_address(request)
            state = __state(request)
            if gender == 'M':
                image = 'images/male.png'
            elif gender == 'F':
                image = 'images/female.png'

            create_user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,
                                              gender=gender,estate=estate, role=rolex,country=country,country_short=country_short,ip_address=ip_address,
                                              state=state,image=image,mobile_number=mobile_number, address=address)
            if create_user:
                suc_msg = True

                estate_name = request.user.estate.estate_name

                subject = 'You have been added to {} via {} platform'.format(estate_name, site_name)
                message = "Hi {} {}, \n \n" \
                          "A profile has just been created for you on {} as an {} within {} (Estate). \n \n" \
                          "Kindly find your credentials, login url and mobile app download link below: \n \n" \
                          "Your username is {}, and your password is {} \n \n" \
                          "You may log in to the website at {}/accounts/login/ \n \n" \
                          "The {} Mobile App is also available (for Android devices only) for download at {} \n \n" \
                          "Kind regards, \n \n" \
                          "The {} Team".format(create_user.first_name, create_user.last_name, 
                            site_name, create_user.role, create_user.estate,
                            create_user.email, pswd,site_url, site_name, apk_file ,
                            site_name.upper())
                try:
                    send_mail(subject, message, (settings.SENDER_TITLE + ' ' + settings.EMAIL_SENDER), [create_user.email],
                              fail_silently=False)
                except:
                    pass

            return redirect('site_mgt:estate_members')

    except:
        suc_msg = False

    data = {'site_url': site_url, 'site_name': site_name,'suc_msg':suc_msg, 'all_streets': all_streets,
            'all_estates': all_estates, 'all_titles': all_titles, 'all_apartments': all_apartments,
            'pword': User.objects.make_random_password()}
    return render(request, 'site/estate_manager/add_member.html', context=data)


@login_required
@is_estate_manager
def add_estate_manager(request):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    all_estates = Estate.objects.order_by('date_created')
    all_titles = Salutation.objects.order_by('title_name')
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    suc_msg = 2
    try:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile_number = request.POST['mobile_number']
            username = request.POST['username']
            email = request.POST['email']
            title = request.POST['title']
            first_name = str(title) + " " + str(first_name)
            password = make_password(request.POST['password'])
            pswd = request.POST.get('password')
            gender = request.POST['gender']
            # role = request.POST['role']
            estate = request.POST['estate']
            rolex = RoleManagement.objects.get(pk=1)
            country = __country_name(request)
            country_short = __country_code(request)
            ip_address = __ip_address(request)
            state = __state(request)
            if gender == 'M':
                image = 'images/male.png'
            elif gender == 'F':
                image = 'images/female.png'

            create_user = User.objects.create(password=password, username=username, first_name=first_name, last_name=last_name,
                                              image=image, email=email, mobile_number=mobile_number, estate_id=estate,
                                              role=rolex, gender=gender, country=country,
                                              country_short=country_short, ip_address=ip_address,)

            if create_user:
                suc_msg = True

                estate_name = request.user.estate.estate_name

                subject = 'YOU HAVE BEEN ADDED TO {} VIA {} PLATFORM'.format(estate_name.upper(), site_name.upper())
                message = "Hi {} {} You have just been created and added to the {} platform as a {} personal in {}. \n" \
                          "Kindly find your login details \n \n" \
                          "Email : {} \n" \
                          "\n Password: {} \n click to login {}accounts/login/ \n \n" \
                          "\n Regards {} Management".format(create_user.first_name, create_user.last_name, site_name,
                                                            create_user.role, create_user.estate,
                                                            create_user.email, pswd, site_url, site_name.upper())
                try:
                    send_mail(subject, message, (settings.SENDER_TITLE + ' ' + settings.EMAIL_SENDER), [create_user.email],
                              fail_silently=False)
                except:
                    pass

    except:
        suc_msg = False

    data = {'site_url': site_url, 'site_name': site_name,'suc_msg':suc_msg, 'all_streets': all_streets,
            'all_estates': all_estates, 'all_titles': all_titles}
    return render(request, 'site/estate_manager/add_member.html', context=data)


@login_required
@is_estate_manager
def my_estates(request):
    all_estates = Estate.objects.order_by('date_created')
    form = NewEstateForm()
    count = 0
    count_list = []
    for i in all_estates:
        count += 1
        count_list.append(count)

    abc = Estate.objects.count()

    estates = zip(all_estates, count_list)
    estate_dict = {'estates': estates, 'form': form, 'abc': abc}

    if request.method == "POST":
        form = NewEstateForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return my_estates(request)

    return render(request, 'site/estate_manager/my_estates.html', context=estate_dict)


@login_required
@is_estate_manager
def my_streets(request):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    form1 = NewStreetForm()
    suc_msg = True

    count = 0
    count_list = []
    for i in all_streets:
        count += 1
        count_list.append(count)

    streets = zip(all_streets, count_list)
    if request.method == "POST":
        estate_id_1 = request.POST['estate_id']
        street_name = request.POST['street_name']
        street_id = estate_id()

        if all_streets.filter(street_name=street_name).exists():
            suc_msg = False 
        else:
            new_street = Street(street_name=street_name, estate_id=estate_id_1, street_id=street_id)
            new_street.save()
            return redirect('site_mgt:my_streets')
    return render(request, 'site/estate_manager/my_streets.html', {'streets': streets, 'form1': form1, 'suc_msg': suc_msg})


@login_required
@is_estate_manager
def my_buildings(request):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    all_buildings = Building.objects.filter(street__in=all_streets)
    form2 = NewBuildingForm()
    form2.fields['street'].queryset = Street.objects.filter(estate=request.user.estate)
    suc_msg = True

    count = 0
    count_list = []
    for i in all_buildings:
        count += 1
        count_list.append(count)

    buildings = zip(all_buildings, count_list)
    
    if request.method == "POST":
        # form2 = NewBuildingForm(request.POST)
        building_id = estate_id()
        street_id = request.POST['street']
        building_number = request.POST['building_number']
        building_type = request.POST['building_type']

        if all_buildings.filter(building_number=building_number).exists():
            suc_msg = False 

        else:
            new_building = Building(building_id=building_id, street_id=street_id, building_number=building_number,
                                    building_type=building_type)
            new_building.save()

            return redirect('site_mgt:my_buildings')

    return render(request, 'site/estate_manager/my_buildings.html', {'buildings': buildings, 'form2': form2, 'all_streets': all_streets, 'suc_msg':suc_msg})


@login_required
@is_estate_manager
def my_apartments(request):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    all_apartments = Apartment.objects.filter(street__in=all_streets)
    all_buildings = Building.objects.filter(street__in=all_streets)
    form3 = NewApartmentForm()
    suc_msg = True

    count = 0
    count_list = []
    for i in all_apartments:
        count += 1
        count_list.append(count)

    apartments = zip(all_apartments, count_list)
    if request.method == "POST":
        apartment_id = estate_id()
        street_id = request.POST['street']
        building_id = request.POST['building']
        apartment = request.POST['apartment_number']
        buildings_apartment = Apartment.objects.filter(building_id=building_id)
        apartment_check = buildings_apartment.filter(apartment_number=apartment)

        if apartment_check.exists():
            suc_msg = False 

        else:
            new_apartment = Apartment(apartment_id=apartment_id, building_id=building_id, apartment_number=apartment, street_id=street_id)
            new_apartment.save()
            return redirect('site_mgt:my_apartments')

    return render(request, 'site/estate_manager/my_apartments.html', {'apartments': apartments, 'form3': form3, 'all_streets': all_streets,
                      'all_buildings': all_buildings, 'suc_msg':suc_msg})


@login_required
@is_estate_manager
def salutation(request):
    all_salutations = Salutation.objects.order_by('date_created')
    form = NewSalutationForm()
    suc_msg = 2

    count = 0
    count_list = []
    for i in all_salutations:
        count += 1
        count_list.append(count)

    salutations = zip(all_salutations, count_list)
    
    if request.method == "POST":
        title_id = estate_id()
        title_name = request.POST['title_name']

        if all_salutations.filter(title_name = title_name).exists():
            suc_msg = False
        else:
            new_salutation = Salutation(title_id=title_id, title_name=title_name)
            new_salutation.save()
            suc_msg = True
            return redirect('site_mgt:salutation')

    salutation_dict = {'salutations': salutations, 'form': form, 'suc_msg':suc_msg}

    return render(request, 'site/estate_manager/salutation.html', context=salutation_dict)


@login_required
@is_estate_manager
def estate_edit(request, pk):
    estate = get_object_or_404(Estate, pk=pk)
    if request.method == "POST":
        form = NewEstateForm(request.POST, instance=estate)
        if form.is_valid():
            estate = form.save(commit=False)
            estate.save()
            return my_estates(request)
    else:
        form = NewEstateForm(instance=estate)
    return render(request, 'site/estate_manager/update_estate.html', {'form5': form})


@login_required
@is_estate_manager
def delete_estate(request, pk):
    Estate.objects.filter(pk=pk).delete()
    return redirect('site_mgt:my_estates')


@login_required
@is_estate_manager
def street_edit(request, pk):
    street = Street.objects.get(pk=pk)

    if request.method == "POST":
        street.street_name = request.POST['street_name']
        street.save()

        return redirect('site_mgt:my_streets')
    return render(request, 'site/estate_manager/update_street.html', {'street': street})


@login_required
@is_estate_manager
def delete_street(request, pk):
    Street.objects.filter(pk=pk).delete()
    return redirect('site_mgt:my_streets')


@login_required
@is_estate_manager
def building_edit(request, pk):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    building = Building.objects.get(pk=pk)

    if request.method == "POST":
        building.street_id = request.POST['street']
        building.building_number = request.POST['building_number']
        building.building_type = request.POST['building_type']
        building.save()

        return redirect('site_mgt:my_buildings')

    return render(request, 'site/estate_manager/update_building.html', {'all_streets': all_streets, 'building': building})


@login_required
@is_estate_manager
def delete_building(request, pk):
    Building.objects.filter(pk=pk).delete()
    return redirect('site_mgt:my_buildings')


@login_required
@is_estate_manager
def apartment_edit(request, pk):
    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    apartment = Apartment.objects.get(pk=pk)

    if request.method == "POST":
        apartment.street_id = request.POST['street']
        apartment.building_id = request.POST['building']
        apartment.apartment_number = request.POST['apartment_number']
        apartment.save()

        return redirect('site_mgt:my_apartments')

    return render(request, 'site/estate_manager/update_apartment.html', {'all_streets': all_streets, 'apartment': apartment})


@login_required
@is_estate_manager
def delete_apartment(request, pk):
    Apartment.objects.filter(pk=pk).delete()
    return redirect('site_mgt:my_apartments')


#Get buildings  from street select box
@login_required
@is_estate_manager
def get_details(request):
    street_name = request.POST.get('street_name')

    all_buildings = Building.objects.filter(street=street_name).filter(building_type=1)

    result_set = []

    for building in all_buildings:
        result_set.append({'building_id': building.building_id, 'building_number': building.building_number,
                           'building_type': building.building_type})

    return JsonResponse(result_set, safe=False)

@login_required
@is_estate_manager
def get_details_build(request):
    street_name = request.POST.get('street_name')

    all_buildings = Building.objects.filter(street=street_name)

    result_set = []

    for building in all_buildings:
        result_set.append({'building_id': building.building_id, 'building_number': building.building_number,
                           'building_type': building.building_type})

    return JsonResponse(result_set, safe=False)


@login_required
@is_estate_manager
def get_details_apartment(request):
    building_id = request.POST.get('building_id')

    apartments = Apartment.objects.filter(building=building_id)

    result_set1 = []

    for apartment in apartments:
        result_set1.append({'apartment_id': apartment.apartment_id, 'apartment_number': apartment.apartment_number})

    return JsonResponse(result_set1, safe=False)


@csrf_exempt
def profile_status(request):
    if request.POST.get('abc'):
        print("HEY")
    else:
        user_id = request.POST.get('user_id')
        password = request.POST.get('password1')
        password = make_password(password)

        u_status = User.objects.get(pk=user_id)
        u_status.profile_status = 1
        u_status.password = password
        u_status.save()
        return JsonResponse({'success': 'all'}, safe=False)


@login_required
@is_estate_manager
def add_street(request):
    suc_msg = True
    street_name = request.POST.get('streetname')
    estate_id = request.POST.get('estate_id')
    all_streets = Street.objects.filter(estate=estate_id).order_by('date_created')

    if all_streets.filter(street_name=street_name).exists():
        suc_msg = False 
    else:
        new_street = Street(street_name=street_name, estate_id=estate_id)
        new_street.save()

    return HttpResponse(suc_msg)

@login_required
@is_estate_manager
def add_building(request):
    suc_msg = True
    street_id = request.POST.get('street_id')
    building_number = request.POST.get('building')
    building_type = request.POST.get('building_type')

    all_buildings = Building.objects.filter(street=street_id)
    building_check = all_buildings.filter(building_number=building_number)

    if building_check.exists():
        suc_msg = False 
    else:
        new_building = Building(street_id=street_id, building_number=building_number, building_type=building_type)
        new_building.save()

    return HttpResponse(suc_msg)

def userEstateReg(request):
    suc_msg = True

    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    apk_file = 'http://clanit.herokuapp.com/clannit.apk'
    try:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')
            email = request.POST.get('email')

            estate_name = request.POST.get('estatename')
            address1 = request.POST.get('address')
            city1 = request.POST.get('city')
            state1 = request.POST.get('state')

            

            estate_address =  str(address1) + ", " + str(city1) + ", " + str(state1)

            username = User.objects.make_random_password()
            apassword = User.objects.make_random_password()
            password = make_password(apassword)
            pswd = apassword
            role = 1
            rolex = RoleManagement.objects.get(pk=role)
            country = __country_name(request)
            country_short = __country_code(request)
            ip_address = __ip_address(request)
            state = __state(request)
            gender = 'M'
            if gender == 'M':
                image = 'images/male.png'
            elif gender == 'F':
                image = 'images/female.png'

            new_estate = Estate(estate_name=estate_name, estate_address=estate_address)
            new_estate.save()

            create_user = User.objects.create(estate_id=new_estate.estate_id, username=username,first_name=first_name,last_name=last_name,email=email,password=password,
                                              gender=gender,role=rolex,country=country,country_short=country_short,ip_address=ip_address,
                                              state=state,image=image,mobile_number=mobile_number, address=estate_address)

            if create_user:
                suc_msg = True

                subject = 'You have been added to {} via {} platform'.format(estate_name, site_name)
                message = "Hi {} {}, \n \n" \
                            "A profile has just been created for you on {} as an {} within {} (Estate). \n \n" \
                            "Kindly find your credentials, login url and mobile app download link below: \n \n" \
                            "Your username is {}, and your password is {} \n \n" \
                            "You may log in to the website at {}/accounts/login/ \n \n" \
                            "The {} Mobile App is also available (for Android devices only) for download at {} \n \n" \
                            "Kind regards, \n \n" \
                            "The {} Team".format(create_user.first_name, create_user.last_name, 
                            site_name, create_user.role, create_user.estate,
                            create_user.email, pswd,site_url, site_name, apk_file ,
                            site_name.upper())
                try:
                    send_mail(subject, message, (settings.SENDER_TITLE + ' ' + settings.EMAIL_SENDER), [create_user.email],
                              fail_silently=False)
                except:
                    pass

    except:
        suc_msg = False

    return HttpResponse(suc_msg)

def add_apartment(request):
    suc_msg = True
    street_id = request.POST.get('street_id')
    building_id = request.POST.get('building')
    apartment = request.POST.get('apartment')

    buildings_apartment = Apartment.objects.filter(building_id=building_id)
    apartment_check = buildings_apartment.filter(apartment_number=apartment)

    if apartment_check.exists():
        suc_msg = False
    else:
        new_apartment = Apartment(apartment_number=apartment, building_id=building_id, street_id=street_id)
        new_apartment.save()

    return HttpResponse(suc_msg)

def get_all_streets(request):
    estate_id = request.POST.get('estate_id')
    all_streets = Street.objects.filter(estate=estate_id).order_by('date_created')

    result_set = []

    for streets in all_streets:
        result_set.append({'street_id': streets.street_id, 'street_name': streets.street_name})

    return JsonResponse(result_set, safe=False)

@login_required
@is_estate_manager
def add_residents(request):
    suc_msg = True

    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    apk_file = 'http://clanit.herokuapp.com/clannit.apk'
    
    try:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')
            email = request.POST.get('email')
            username = User.objects.make_random_password()
            title = request.POST.get('title_resd')
            first_name = str(title) + " " + str(first_name)
            apassword = User.objects.make_random_password()
            password = make_password(apassword)
            pswd = apassword
            gender = request.POST.get('gender')
            role = request.POST.get('role')
            building = request.POST.get('building')
            street = request.POST.get('street')
            apartment = request.POST.get('apartment')
            address = str(building) + ", " + str(street)
            estate = Estate.objects.get(pk=request.user.estate_id)
            if role == 4:
                address = "Security Post"
                
            rolex = RoleManagement.objects.get(pk=role)
            country = __country_name(request)
            country_short = __country_code(request)
            ip_address = __ip_address(request)
            state = __state(request)
            if gender == 'M':
                image = 'images/male.png'
            elif gender == 'F':
                image = 'images/female.png'
            if User.objects.filter(email=email).exists():
                suc_msg = False
            else:
                create_user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,
                                                gender=gender,estate=estate, role=rolex,country=country,country_short=country_short,ip_address=ip_address,
                                                state=state,image=image,mobile_number=mobile_number, address=address)

                if create_user:
                    suc_msg = True

                    estate_name = request.user.estate.estate_name

                    subject = 'You have been added to {} via {} platform'.format(estate_name, site_name)
                    message = "Hi {} {}, \n \n" \
                            "A profile has just been created for you on {} as an {} within {} (Estate). \n \n" \
                            "Kindly find your credentials, login url and mobile app download link below: \n \n" \
                            "Your username is {}, and your password is {} \n \n" \
                            "You may log in to the website at {}/accounts/login/ \n \n" \
                            "The {} Mobile App is also available (for Android devices only) for download at {} \n \n" \
                            "Kind regards, \n \n" \
                            "The {} Team".format(create_user.first_name, create_user.last_name, 
                            site_name, create_user.role, create_user.estate,
                            create_user.email, pswd,site_url, site_name, apk_file ,
                            site_name.upper())




                    try:
                        send_mail(subject, message, (settings.SENDER_TITLE + ' ' + settings.EMAIL_SENDER), [create_user.email],
                                fail_silently=False)
                    except:
                        pass
    except:
        suc_msg = False

    return HttpResponse(suc_msg)


@login_required
@is_estate_manager
def resident_edit(request, pk):
    resident = User.objects.get(pk=pk)

    all_streets = Street.objects.filter(estate=request.user.estate).order_by('date_created')
    all_estates = Estate.objects.order_by('date_created')
    all_apartments = Apartment.objects.order_by('date_created')
    all_titles = Salutation.objects.order_by('date_created')
    site_name = settings.SITE_NAME
    site_url = settings.SITE_URL
    apk_file = 'http://clanit.herokuapp.com/clannit.apk'
    suc_msg = 2

    if request.method == "POST":
        resident.first_name = request.POST['first_name']
        resident.last_name = request.POST['last_name']
        resident.mobile_number = request.POST['mobile_number']
        resident.email = request.POST['email']
        title = request.POST['title']
        resident.gender = request.POST['gender']

        role = request.POST['role']
        resident.rolex = RoleManagement.objects.get(pk=role)
        building = request.POST['building']
        street = request.POST['street']
        apartment = request.POST['apartment']
        resident.address = str(building) + ", " + str(street)

        resident.save()
        return redirect('site_mgt:estate_members')

    data = {'site_url': site_url, 'site_name': site_name,'suc_msg':suc_msg, 'all_streets': all_streets,
            'all_estates': all_estates, 'all_titles': all_titles, 'all_apartments': all_apartments, 'resident': resident}
    
    return render(request, 'site/estate_manager/update_resident.html', context=data)


@login_required
@is_estate_manager
def delete_resident(request, pk):
    User.objects.filter(pk=pk).delete()
    return redirect('site_mgt:estate_members')