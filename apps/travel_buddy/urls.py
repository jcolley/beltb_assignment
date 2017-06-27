from django.conf.urls import url
from.import views

app_name = 'tb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.addPlan, name='addPlan'),
    url(r'^addTrip$', views.addTrip, name='addTrip'),
    url(r'^dest/(?P<trip_id>\d+)$', views.dest, name='dest'),
    url(r'^joinTrip/(?P<trip_id>\d+)/(?P<user_id>\d+)$', views.joinTrip, name='joinTrip'),
]
