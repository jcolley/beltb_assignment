# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Trip, User


# Create your views here.
def index(request):
    checkAuth(request)

    user = User.objects.get(id=request.session['id'])
    trips = Trip.objects.all()

    context = {
        'user': user,
        'trips': trips,
    }
    return render(request, 'travel_buddy/index.html', context)


def addPlan(request):
    checkAuth(request)
    return render(request, 'travel_buddy/addtrip.html')


def addTrip(request):
    checkAuth(request)
    results = Trip.objects.addTrip(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
            return redirect('tb:addPlan')
    else:
        messages.success(request, 'Trip Created!')
    return redirect('tb:index')


def joinTrip(request, trip_id, user_id):
    checkAuth(request)
    results = Trip.objects.joinTrip(trip_id, user_id)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
            return redirect('tb:addPlan')
    else:
        messages.success(request, 'Joined Trip!')
    return redirect('tb:index')


def dest(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trip': trip,
    }
    return render(request, 'travel_buddy/trip.html', context)


def checkAuth(request):  # Force non-authorized user back to login/registration page
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('auth:index')
