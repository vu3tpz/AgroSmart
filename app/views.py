from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

#<-----For check user is Admin, Visitor and Officer----->#
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_visitor(user):
    return user.groups.filter(name='VISITOR').exists()
def is_officer(user):
    return user.groups.filter(name='OFFICER').exists()
def is_seller(user):
    return user.groups.filter(name='SELLER').exists()

#<-----LogOut For All----->#
def logout_view(request):
    logout(request)
    return redirect('/')

#<-------------------------------------------->#
#<---------------Admin Functions-------------->#
#<-------------------------------------------->#

#<-----Login For Admin----->#
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='ADMIN'):
                    login(request,user)
                    return redirect('admin_home')
                else:
                    messages.success(request, 'Your account is not found in Admin..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = AdminLoginForm()           
    return render(request, 'admin/admin_login.html',{'form':form})


#<-----Home Page for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'admin/admin_home.html')

#<-----Profile Page for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_profile(request):
    return render(request, 'admin/admin_profile.html')

#<-----Change password----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def change_password_admin(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'admin/change_password_admin.html', {'form': form})

#<-----Admin Approvall for visitors----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_visitor(request):
    visitors = Visitor.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_visitor.html',{'visitors':visitors})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_visitor(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    visitor.status=True
    visitor.save()
    return redirect(reverse('admin_approve_visitor'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_visitor(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    user=User.objects.get(id=visitor.user_id)
    user.delete()
    visitor.delete()
    return redirect(reverse('admin_approve_visitor'))

#<-----Admin Approvall for sellers----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_seller(request):
    sellers = Seller.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_seller.html',{'sellers':sellers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def detail_seller(request, id):
    sellers = Seller.objects.all().get(id=id)
    data={'sellers':sellers}
    return render(request, 'admin/detail_seller.html',data)

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_seller(request):
    seller=get_object_or_404(Seller, pk=request.GET.get('seller_id'))
    seller.status=True
    seller.save()
    return redirect(reverse('admin_approve_seller'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_seller(request):
    seller=get_object_or_404(Seller, pk=request.GET.get('seller_id'))
    user=User.objects.get(id=seller.user_id)
    user.delete()
    seller.delete()
    return redirect(reverse('admin_approve_seller'))

#<-----Admin Approvall for officer----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_officer(request):
    officers = Officer.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_officer.html',{'officers':officers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_officer(request):
    officer=get_object_or_404(Officer, pk=request.GET.get('officer_id'))
    officer.status=True
    officer.save()
    return redirect(reverse('admin_approve_officer'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_officer(request):
    officer=get_object_or_404(Officer, pk=request.GET.get('officer_id'))
    user=User.objects.get(id=officer.user_id)
    user.delete()
    officer.delete()
    return redirect('admin_approve_officer')

#<-----Admin add Admin----->#
def admin_add_admin(request):
    if request.method=='POST':
        form1=AdminUserForm(request.POST)
        form2=AdminExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_admin_group=Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('admin_active_admin')
    else:
        form1=AdminUserForm()
        form2=AdminExtraForm()
    return render(request, 'admin/admin_add_admin.html',{'form1':form1,'form2':form2})

#<-----Active Admin View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_admin(request):
    admins = Admin.objects.all()
    return render(request, 'admin/admin_active_admin.html',{'admins':admins})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_admin_active(request):
    admin=get_object_or_404(Admin, pk=request.GET.get('admin_id'))
    user=User.objects.get(id=admin.user_id)
    user.delete()
    admin.delete()
    return redirect(reverse('admin_active_admin'))

#<-----Active Visitor View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_visitor(request):
    visitors = Visitor.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_visitor.html',{'visitors':visitors})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_visitor_active(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    user=User.objects.get(id=visitor.user_id)
    user.delete()
    visitor.delete()
    return redirect(reverse('admin_active_visitor'))

#<-----Active Seller View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_seller(request):
    sellers = Seller.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_seller.html',{'sellers':sellers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def detail_active_seller(request, id):
    sellers = Seller.objects.all().get(id=id)
    data={'sellers':sellers}
    return render(request, 'admin/detail_active_seller.html',data)

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_seller_active(request):
    seller=get_object_or_404(Seller, pk=request.GET.get('seller_id'))
    user=User.objects.get(id=seller.user_id)
    user.delete()
    seller.delete()
    return redirect(reverse('admin_active_seller'))

#<-----Active Officer View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_officer(request):
    officers = Officer.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_officer.html',{'officers':officers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_officer_active(request):
    officer=get_object_or_404(Officer, pk=request.GET.get('officer_id'))
    user=User.objects.get(id=officer.user_id)
    user.delete()
    officer.delete()
    return redirect(reverse('admin_active_officer'))

#<---------------------------------------------->#
#<---------------Visitor Functions-------------->#
#<---------------------------------------------->#

#<-----Signup For Visitor----->#
def visitor_signup(request):
    if request.method=='POST':
        form1=VisitorUserForm(request.POST)
        form2=VisitorExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_visitor_group=Group.objects.get_or_create(name='VISITOR')
            my_visitor_group[0].user_set.add(user)

            messages.success(request, 'Request send for approval, Try Login after 24 Hours..')

            return HttpResponseRedirect('/')
    else:
        form1=VisitorUserForm()
        form2=VisitorExtraForm()
    return render(request, 'visitor/visitor_signup.html',{'form1':form1,'form2':form2})

#<-----Login For Visitor----->#
def visitor_login(request):
    if request.method == 'POST':
        form = VisitorLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='VISITOR'):
                    if Visitor.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('visitor_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Visitor..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = VisitorLoginForm()           
    return render(request, 'visitor/visitor_login.html',{'form':form})

#<-----Home Page for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_home(request):
    return render(request, 'visitor/visitor_home.html')

#<-----Profile Page for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_profile(request):
    return render(request, 'visitor/visitor_profile.html')

#<-----Change password----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def change_password_visitor(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('visitor_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'visitor/change_password_visitor.html', {'form': form})

#<-----Add soil By Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_add_soil(request):
    if request.method=='POST':
        form=SoilAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Your Contibution send for Verification, If detail is genuine it may reflect in Soil after 24 Hours..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=SoilAddForm()
    return render(request, 'visitor/visitor_add_soil.html',{'form':form})

def load_regions(request):
    district_id = request.GET.get('district_id')
    regions = Region.objects.filter(district_id=district_id).all()
    return render(request, 'dropdown_list_region.html', {'regions':regions})

#<-----Find Soil for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_soil(request):
    soils = None
    if request.method == 'POST':
        form = FindSoilForm(request.POST)
        if form.is_valid():
            district = request.POST['district']
            soils = SoilLocationDetail.objects.all().filter(district=district, status=True)
    else:
        form = FindSoilForm()
    return render(request, 'visitor/visitor_find_soil.html',{'form':form,'soils':soils})

#<-----Find Soil Detail for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_soil_detail(request):
    soils = None
    if request.method == 'POST':
        form = FindSoilDetailForm(request.POST)
        if form.is_valid():
            soil = request.POST['soil']
            soils = SoilDetail.objects.all().filter(soil=soil)
    else:
        form = FindSoilDetailForm()
    return render(request, 'visitor/visitor_find_soil_detail.html',{'form':form,'soils':soils})

#<-----Find Rainfall for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_rainfall(request):
    rainfalls = None
    if request.method == 'POST':
        form = FindRainfallForm(request.POST)
        if form.is_valid():
            district = request.POST['district']
            rainfalls = RainfallDetail.objects.all().order_by('year').filter(district=district)
    else:
        form = FindRainfallForm()
    return render(request, 'visitor/visitor_find_rainfall.html',{'form':form,'rainfalls':rainfalls})

#<-----Find Crop for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_crop(request):
    result=''

    if request.method == 'POST':
        form = FindCropForm(request.POST)
            
        nitrogen = request.POST['nitrogen']
        phosphorus = request.POST['phosphorus']
        potassium = request.POST['potassium']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']

        df = pd.read_csv("Mechine Learning\Crop_recommendation.csv")

        features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
        target = df['label']
        #features = df[['temperature', 'humidity', 'ph', 'rainfall']]
        labels = df['label']

        # Initialzing empty lists to append all model's name and corresponding name
        acc = []
        model = []

        # Splitting into train and test data
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

        RF = RandomForestClassifier(n_estimators=20, random_state=0)
        RF.fit(Xtrain.values,Ytrain.values)

        predicted_values = RF.predict(Xtest.values)

        x = metrics.accuracy_score(Ytest, predicted_values)
        acc.append(x)
        model.append('RF')

        data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = RF.predict(data)
        result = "The predicted crop is "+ str(prediction).replace("'","")[1:-1]

    else:
        form=FindCropForm()
    return render(request, 'visitor/visitor_find_crop.html',{'form':form,'result':result})

#<-----Add Crop Detail By Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_add_crop(request):
    if request.method=='POST':
        form=CropAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Your Contibution send for Verification, If detail is genuine it may reflect in Soil after 24 Hours..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=CropAddForm()
    return render(request, 'visitor/visitor_add_crop.html',{'form':form})

#<-----Request seed by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_get_seed(request):
    if request.method=='POST':
        form=RequestSeedForm(request.POST)
        if form.is_valid():
            
            username = request.user.username
            name = request.user.visitor.get_name
            email = request.user.visitor.email
            district = str(request.user.visitor.district)
            gender = request.user.visitor.gender
            address = request.POST.get('address')
            crop = request.POST.get('crop')
            quantity = request.POST.get('quantity')

            req=RequestSeed.objects.create(username=username, name=name, email=email, district=district, gender=gender, address=address, crop=crop, quantity=quantity)
            req.save()
            
            messages.success(request, 'Your application in process it may take some time..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=RequestSeedForm()
    return render(request, 'visitor/visitor_get_seed.html',{'form':form})

#<-----Request seed by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_get_fertilizer(request):
    if request.method=='POST':
        form=RequestFertilizerForm(request.POST)
        if form.is_valid():
            
            username = request.user.username
            name = request.user.visitor.get_name
            email = request.user.visitor.email
            district = str(request.user.visitor.district)
            gender = request.user.visitor.gender
            address = request.POST.get('address')
            fertilizer = request.POST.get('fertilizer')
            quantity = request.POST.get('quantity')

            req=RequestFertilizer.objects.create(username=username, name=name, email=email, district=district, gender=gender, address=address, fertilizer=fertilizer, quantity=quantity)
            req.save()
            
            messages.success(request, 'Your application in process it may take some time..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=RequestFertilizerForm()
    return render(request, 'visitor/visitor_get_fertilizer.html',{'form':form})

#<-----Application for seed request view by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_seed_request(request):
    username=request.user.username
    seeds = RequestSeed.objects.all().filter(username=username)
    return render(request, 'visitor/visitor_seed_request.html',{'seeds':seeds})

#<-----Application for fertilizer request view by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_fertilizer_request(request):
    username=request.user.username
    ferts = RequestFertilizer.objects.all().filter(username=username)
    return render(request, 'visitor/visitor_fertilizer_request.html',{'ferts':ferts})

#<-----Visitor Virtual Market Home----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_market_home(request):
    return render(request, 'visitor/visitor_market_home.html')

#<---------------------------------------------->#
#<---------------Officer Functions-------------->#
#<---------------------------------------------->#

#<-----Signup For Officer----->#
def officer_signup(request):
    if request.method=='POST':
        form1=OfficerUserForm(request.POST)
        form2=OfficerExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_visitor_group=Group.objects.get_or_create(name='OFFICER')
            my_visitor_group[0].user_set.add(user)

            messages.success(request, 'Request send for approval, Try Login after 24 Hours..')

            return HttpResponseRedirect('/')
    else:
        form1=OfficerUserForm()
        form2=OfficerExtraForm()
    return render(request, 'officer/officer_signup.html',{'form1':form1,'form2':form2})

#<-----Login For Officer----->#
def officer_login(request):
    if request.method == 'POST':
        form = OfficerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='OFFICER'):
                    if Officer.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('officer_home')
                    else:
                       messages.success(request, 'Your Request is in processing, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found..')
            else:
                messages.success(request, 'Invalid Username and Password..')
    else:
         form = OfficerLoginForm()           
    return render(request, 'officer/officer_login.html',{'form':form})

#<-----Home Page for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_home(request):
    return render(request, 'officer/officer_home.html')

#<-----Profile Page for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_profile(request):
    return render(request, 'officer/officer_profile.html')

#<-----Change password----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def change_password_officer(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('officer_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'officer/change_password_officer.html', {'form': form})

#<-----Active Soils View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_soil(request):
    soils = SoilLocationDetail.objects.all().filter(status=True)
    return render(request, 'officer/officer_active_soil.html',{'soils':soils})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_soil_active(request):
    soil=get_object_or_404(SoilLocationDetail, pk=request.GET.get('soil_id'))
    soil.delete()
    return redirect(reverse('officer_active_soil'))

#<-----Add soil By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_soil(request):
    if request.method=='POST':
        form=SoilAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.status=True
            user.save()

            messages.success(request, 'Soil Save Sucssesfully..')

            return HttpResponseRedirect('officer_active_soil')
    else:
        form=SoilAddForm()
    return render(request, 'officer/officer_add_soil.html',{'form':form})

#<-----Active Detail of Soil View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_soil_detail(request):
    soils = SoilDetail.objects.all()
    return render(request, 'officer/officer_active_soil_detail.html',{'soils':soils})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_soil_detail_active(request):
    soil=get_object_or_404(SoilDetail, pk=request.GET.get('soil_id'))
    soil.delete()
    return redirect(reverse('officer_active_soil_detail'))

#<-----Add soil Detail By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_soil_detail(request):
    if request.method=='POST':
        form=SoilDetailAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Soil Detail Save Sucssesfully..')

            return HttpResponseRedirect('officer_active_soil_detail')
    else:
        form=SoilDetailAddForm()
    return render(request, 'officer/officer_add_soil_detail.html',{'form':form})

#<-----Officer Approvall for Soils----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_approve_soil(request):
    soils = SoilLocationDetail.objects.all().filter(status=False)
    return render(request, 'officer/officer_approve_soil.html',{'soils':soils})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def approve_soil(request):
    soil=get_object_or_404(SoilLocationDetail, pk=request.GET.get('soil_id'))
    soil.status=True
    soil.save()
    return redirect(reverse('officer_approve_soil'))

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_soil(request):
    soil=get_object_or_404(SoilLocationDetail, pk=request.GET.get('soil_id'))
    soil.delete()
    return redirect(reverse('officer_approve_soil'))

#<-----Active Detail of Rainfall View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_rainfall(request):
    rainfalls = RainfallDetail.objects.all()
    return render(request, 'officer/officer_active_rainfall.html',{'rainfalls':rainfalls})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_rainfall_active(request):
    rainfall=get_object_or_404(RainfallDetail, pk=request.GET.get('rainfall_id'))
    rainfall.delete()
    return redirect(reverse('officer_active_rainfall'))

#<-----Add Rainfall Detail By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_rainfall(request):
    if request.method=='POST':
        form=RainfallDetailAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Rainfall Detail Save Sucssesfully..')

            return HttpResponseRedirect('officer_active_rainfall')
    else:
        form=RainfallDetailAddForm()
    return render(request, 'officer/officer_add_rainfall.html',{'form':form})

#<-----Active Crop for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_crop(request):
    crops = CropDetail.objects.all().filter(status=True)
    return render(request, 'officer/officer_active_crop.html',{'crops':crops})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_crop_active(request):
    crop=get_object_or_404(CropDetail, pk=request.GET.get('crop_id'))
    crop.delete()
    return redirect(reverse('officer_active_crop'))

#<-----Add Crop Detail By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_crop(request):
    if request.method=='POST':
        form=CropAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.status=True
            user.save()

            messages.success(request, 'Crop Detail Save Sucssesfully..')

            return HttpResponseRedirect('officer_active_crop')
    else:
        form=CropAddForm()
    return render(request, 'officer/officer_add_crop.html',{'form':form})

#<-----Officer Approvall for Crop----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_approve_crop(request):
    crops = CropDetail.objects.all().filter(status=False)
    return render(request, 'officer/officer_approve_crop.html',{'crops':crops})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def approve_crop(request):
    crop=get_object_or_404(CropDetail, pk=request.GET.get('crop_id'))
    crop.status=True
    crop.save()
    return redirect(reverse('officer_approve_crop'))

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_crop(request):
    crop=get_object_or_404(CropDetail, pk=request.GET.get('crop_id'))
    crop.delete()
    return redirect(reverse('officer_approve_crop'))

#<-----Request for seed View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_seed_request(request):
    seeds = RequestSeed.objects.all().filter(reject=False, approve=False)
    return render(request, 'officer/officer_seed_request.html',{'seeds':seeds})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def reject_seed_request(request):
    seed=get_object_or_404(RequestSeed, pk=request.GET.get('seed_id'))
    seed.reject=True
    seed.approve=False
    seed.save()
    return redirect(reverse('officer_seed_request'))

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def approve_seed_request(request):
    seed=get_object_or_404(RequestSeed, pk=request.GET.get('seed_id'))
    seed.reject=False
    seed.approve=True
    seed.save()
    return redirect(reverse('officer_seed_request'))

#<-----Approved seed request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_approve_seed_request(request):
    seeds = RequestSeed.objects.all().filter(reject=False, approve=True)
    return render(request, 'officer/officer_approve_seed_request.html',{'seeds':seeds})

#<-----Rejected seed request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_reject_seed_request(request):
    seeds = RequestSeed.objects.all().filter(reject=True, approve=False)
    return render(request, 'officer/officer_reject_seed_request.html',{'seeds':seeds})

#<-----Request for fertilizer View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_fertilizer_request(request):
    ferts = RequestFertilizer.objects.all().filter(reject=False, approve=False)
    return render(request, 'officer/officer_fertilizer_request.html',{'ferts':ferts})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def reject_fertilizer_request(request):
    fertilizer=get_object_or_404(RequestFertilizer, pk=request.GET.get('fertilizer_id'))
    fertilizer.reject=True
    fertilizer.approve=False
    fertilizer.save()
    return redirect(reverse('officer_fertilizer_request'))

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def approve_fertilizer_request(request):
    fertilizer=get_object_or_404(RequestFertilizer, pk=request.GET.get('fertilizer_id'))
    fertilizer.reject=False
    fertilizer.approve=True
    fertilizer.save()
    return redirect(reverse('officer_fertilizer_request'))

#<-----Approved fertilizer request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_approve_fertilizer_request(request):
    ferts = RequestFertilizer.objects.all().filter(reject=False, approve=True)
    return render(request, 'officer/officer_approve_fertilizer_request.html',{'ferts':ferts})

#<-----Rejected fertilizer request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_reject_fertilizer_request(request):
    ferts = RequestFertilizer.objects.all().filter(reject=True, approve=False)
    return render(request, 'officer/officer_reject_fertilizer_request.html',{'ferts':ferts})

#<--------------------------------------------->#
#<---------------Seller Functions-------------->#
#<--------------------------------------------->#

#<-----Signup For Seller----->#
def seller_signup(request):
    if request.method=='POST':
        form1=SellerUserForm(request.POST)
        form2=SellerExtraForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_seller_group=Group.objects.get_or_create(name='SELLER')
            my_seller_group[0].user_set.add(user)

            #subject = 'Welcome Note'
            #message = 'welcome to Agrosmart Virtual market please wait for our conformation mail to access our market..!\nwe also send an mail if your request will reject..\nIt is an auto generated mauil system Do not reply to this mail'
            #recipient = form2.cleaned_data.get('email')
            #send_mail(subject, 
            #  message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

            messages.success(request, 'Request send for approval, If request is accept we send you a Email..')

            return HttpResponseRedirect('/')
    else:
        form1=SellerUserForm()
        form2=SellerExtraForm()
    return render(request, 'seller/seller_signup.html',{'form1':form1,'form2':form2})

#<-----Login For Seller----->#
def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='SELLER'):
                    if Seller.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('seller_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Seller..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = VisitorLoginForm()           
    return render(request, 'seller/seller_login.html',{'form':form})

#<-----Home Page for Seller----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def seller_home(request):
    return render(request, 'seller/seller_home.html')

#<-----Seller product page----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def product(request):
    products = Product.objects.all().filter(garden=request.user.seller.garden)
    return render(request, 'seller/product.html',{'products':products})

#<-----Detail view of product----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def detail_product_seller(request, id):
    products = Product.objects.all().get(id=id)
    if request.method=='POST':
        form=EditPriceForm(request.POST)
        if form.is_valid():
            obj = Product.objects.all().get(id=id)
            obj.price = request.POST.get('price')
            obj.save()

            messages.success(request, 'Your Price update successfully..')

            return HttpResponseRedirect('detail_product_seller')
    else:
        form=EditPriceForm()
    return render(request, 'seller/detail_product_seller.html',{'products':products,'form':form})

#<-----Seller add new product page----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def add_product(request):
    if request.method=='POST':
        form=ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            
            product_name = request.POST.get('product_name')
            describe = request.POST.get('describe')
            image_1 = request.FILES.get('image_1')
            image_2 = request.FILES.get('image_2')
            image_3 = request.FILES.get('image_3')
            image_4 = request.FILES.get('image_4')
            district = str(request.user.seller.district)
            garden = request.user.seller.garden
            price = request.POST.get('price')
            price_per_quantity = request.POST.get('price_per_quantity')

            req=Product.objects.create(product_name=product_name, describe=describe, image_1=image_1, image_2=image_2, image_3=image_3, image_4=image_4, district=district, garden=garden, price=price, price_per_quantity=price_per_quantity)
            req.save()

            return HttpResponseRedirect('seller_home')
    else:
        form=ProductAddForm()
    return render(request, 'seller/add_product.html',{'form':form})

#<-----Make out of stock----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def outofstock(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.stock=False
    product.save()
    return redirect(reverse('product'))

#<-----Make out of stock----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def instock(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.stock=True
    product.save()
    return redirect(reverse('product'))

#<-----Delete product----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def delete_product_seller(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.delete()
    return redirect(reverse('product'))