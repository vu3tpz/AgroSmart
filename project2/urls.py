"""project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('logout',LogoutView.as_view(next_page='/'),name='logout'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),

    #<-----Admin URLs----->

    path('admin_login',admin_login,name='admin_login'),
    path('admin_home',admin_home,name='admin_home'),
    path('admin_profile', admin_profile, name='admin_profile'),
    path('change_password_admin', change_password_admin, name='change_password_admin'),

    path('admin_approve_visitor', admin_approve_visitor,name='admin_approve_visitor'),
    path('approve_visitor', approve_visitor, name='approve_visitor'),
    path('delete_visitor', delete_visitor, name='delete_visitor'),

    path('admin_approve_seller', admin_approve_seller,name='admin_approve_seller'),
    path('approve_seller', approve_seller, name='approve_seller'),
    path('delete_seller', delete_seller, name='delete_seller'),

    path('admin_approve_officer', admin_approve_officer,name='admin_approve_officer'),
    path('approve_officer', approve_officer, name='approve_officer'),
    path('delete_officer', delete_officer, name='delete_officer'),

    path('admin_add_admin', admin_add_admin, name='admin_add_admin'),
    path('admin_active_admin', admin_active_admin,name='admin_active_admin'),
    path('delete_admin_active', delete_admin_active, name='delete_admin_active'),

    path('admin_active_visitor', admin_active_visitor,name='admin_active_visitor'),
    path('delete_visitor_active', delete_visitor_active, name='delete_visitor_active'),

    path('<int:id>/detail_seller', detail_seller,name='detail_seller'),
    path('<int:id>/detail_active_seller', detail_active_seller,name='detail_active_seller'),

    path('admin_active_seller', admin_active_seller,name='admin_active_seller'),
    path('delete_seller_active', delete_seller_active, name='delete_seller_active'),

    path('admin_active_officer', admin_active_officer,name='admin_active_officer'),
    path('delete_officer_active', delete_officer_active, name='delete_officer_active'),

    path('admin_add_soil', admin_add_soil, name='admin_add_soil'),
    path('admin_add_soil_detail', admin_add_soil_detail, name='admin_add_soil_detail'),
    path('admin_add_rainfall', admin_add_rainfall, name='admin_add_rainfall'),
    path('admin_add_crop', admin_add_crop, name='admin_add_crop'),

    path('admin_approve_soil', admin_approve_soil,name='admin_approve_soil'),
    path('approve_soil_request', approve_soil_request, name='approve_soil_request'),
    path('delete_soil_request', delete_soil_request, name='delete_soil_request'),

    path('admin_active_soil', admin_active_soil,name='admin_active_soil'),
    path('delete_soil_location_active', delete_soil_location_active, name='delete_soil_location_active'),

    path('admin_active_soil_detail', admin_active_soil_detail,name='admin_active_soil_detail'),
    path('delete_soil_detail_active', delete_soil_detail_active, name='delete_soil_detail_active'),
    path('ajax/load-regions/', load_regions, name="ajax_load_regions"),

    path('admin_active_rainfall', admin_active_rainfall,name='admin_active_rainfall'),
    path('delete_rainfall_active', delete_rainfall_active, name='delete_rainfall_active'),

    path('admin_approve_crop', admin_approve_crop,name='admin_approve_crop'),
    path('approve_crop_request', approve_crop_request, name='approve_crop_request'),
    path('delete_crop_request', delete_crop_request, name='delete_crop_request'),

    path('admin_active_crop', admin_active_crop,name='admin_active_crop'),
    path('delete_crop_active', delete_crop_active, name='delete_crop_active'),

    #<-----Visitor URLs----->

    path('visitor_signup',visitor_signup,name='visitor_signup'),
    path('visitor_login',visitor_login,name='visitor_login'),
    path('visitor_home',visitor_home,name='visitor_home'),
    path('visitor_profile', visitor_profile, name='visitor_profile'),
    path('change_password_visitor', change_password_visitor, name='change_password_visitor'),

    path('visitor_add_soil', visitor_add_soil, name='visitor_add_soil'),
    path('visitor_add_crop', visitor_add_crop, name='visitor_add_crop'),

    path('visitor_find_soil',visitor_find_soil, name='visitor_find_soil'),
    path('visitor_find_soil_detail',visitor_find_soil_detail, name='visitor_find_soil_detail'),
    path('visitor_find_rainfall',visitor_find_rainfall, name='visitor_find_rainfall'),
    path('visitor_find_crop',visitor_find_crop, name='visitor_find_crop'),

    path('visitor_get_seed',visitor_get_seed, name='visitor_get_seed'),
    path('visitor_get_fertilizer',visitor_get_fertilizer, name='visitor_get_fertilizer'),
    
    path('visitor_seed_request',visitor_seed_request, name='visitor_seed_request'),
    path('visitor_fertilizer_request',visitor_fertilizer_request, name='visitor_fertilizer_request'),

    path('visitor_market_home',visitor_market_home, name='visitor_market_home'),

    #<-----Officer URLs----->

    path('officer_signup',officer_signup,name='officer_signup'),
    path('officer_login',officer_login,name='officer_login'),
    path('officer_home',officer_home,name='officer_home'),
    path('officer_profile', officer_profile,name='officer_profile'),
    path('change_password_officer', change_password_officer, name='change_password_officer'),

    path('officer_add_soil_detail', officer_add_soil_detail, name='officer_add_soil_detail'),
    path('officer_active_soil_detail', officer_active_soil_detail,name='officer_active_soil_detail'),

    path('officer_add_soil', officer_add_soil, name='officer_add_soil'),
    path('officer_approve_soil', officer_approve_soil,name='officer_approve_soil'),

    path('officer_active_soil', officer_active_soil,name='officer_active_soil'),
    path('approve_soil',approve_soil, name='approve_soil'),
    path('delete_soil',delete_soil, name='delete_soil'),

    path('officer_active_rainfall', officer_active_rainfall,name='officer_active_rainfall'),

    path('officer_add_rainfall', officer_add_rainfall,name='officer_add_rainfall'),

    path('officer_active_crop', officer_active_crop,name='officer_active_crop'),
    path('officer_add_crop', officer_add_crop,name='officer_add_crop'),

    path('officer_approve_crop', officer_approve_crop,name='officer_approve_crop'),
    path('approve_crop', approve_crop, name='approve_crop'),
    path('delete_crop', delete_crop, name='delete_crop'),

    path('officer_seed_request', officer_seed_request,name='officer_seed_request'),
    path('approve_seed_request', approve_seed_request,name='approve_seed_request'),
    path('reject_seed_request', reject_seed_request,name='reject_seed_request'),

    path('officer_approve_seed_request', officer_approve_seed_request,name='officer_approve_seed_request'),
    path('officer_reject_seed_request', officer_reject_seed_request,name='officer_reject_seed_request'),

    path('officer_fertilizer_request', officer_fertilizer_request,name='officer_fertilizer_request'),
    path('approve_fertilizer_request', approve_fertilizer_request,name='approve_fertilizer_request'),
    path('reject_fertilizer_request', reject_fertilizer_request,name='reject_fertilizer_request'),

    path('delete_soil_active', delete_soil_active, name='delete_soil_active' ),

    path('officer_approve_fertilizer_request', officer_approve_fertilizer_request,name='officer_approve_fertilizer_request'),
    path('officer_reject_fertilizer_request', officer_reject_fertilizer_request,name='officer_reject_fertilizer_request'),

    #<-----Sellers URLs----->

    path('seller_signup',seller_signup,name='seller_signup'),
    path('seller_login',seller_login,name='seller_login'),
    path('seller_home',seller_home,name='seller_home'),
    path('product',product,name='product'),
    path('add_product',add_product,name='add_product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)