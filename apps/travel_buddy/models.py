# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, IntegrityError
from dateutil.parser import parse
from datetime import datetime
from ..login_registration.models import User


# Create your models here.
class TripManager(models.Manager):
    def addTrip(self, postData):
        results = {'status': True, 'errors': []}
        if not postData['owner']:
            results['status'] = False
            results['errors'].append('Authentication Error, please login and try again.')
        if not len(postData['dest']) > 1:
            results['status'] = False
            results['errors'].append('You must enter a destination')
        if not len(postData['desc']) > 1:
            results['status'] = False
            results['errors'].append('You must enter a description')
        if not len(postData['dFrom']) > 1:
            results['status'] = False
            results['errors'].append('You must enter a From date')
        if not len(postData['dTo']) > 1:
            results['status'] = False
            results['errors'].append('You must enter an To date')

        dFrom = datetime.strptime(postData['dFrom'], '%Y-%m-%d').date()
        dTo = datetime.strptime(postData['dTo'], '%Y-%m-%d').date()

        if dFrom > dTo:
            results['status'] = False
            results['errors'].append('From date cannot be after To date')
        if dFrom < datetime.now().date():
            results['status'] = False
            results['errors'].append('From date cannot be before today!')

        if results['status']:
            try:
                owner = User.objects.get(id=postData['owner'])
                dest = postData['dest']
                desc = postData['desc']
                dFrom = postData['dFrom']
                dTo = postData['dTo']

                trip = Trip.objects.create(
                    owner=owner,
                    dest=dest,
                    desc=desc,
                    dFrom=dFrom,
                    dTo=dTo,
                )

                trip.save()

            except IntegrityError as e:
                results['status'] = False
                results['errors'].append(e.message)

        return results

    def joinTrip(self, trip_id, user_id):
        results = {'status': True, 'errors': []}
        try:
            trip = Trip.objects.get(id=trip_id)
            trip.joined.add(user_id)
        except IntegrityError as e:
            results['status'] = False
            results['errors'].append(e.message)

        return results


class Trip(models.Model):
    owner = models.ForeignKey('login_registration.User', related_name='trips')
    joined = models.ManyToManyField('login_registration.User', related_name='joined')
    dest = models.CharField(max_length=30, null=False)
    desc = models.CharField(max_length=100, null=False)
    dFrom = models.DateField()
    dTo = models.DateField()

    objects = TripManager()
