from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin_dashboard$', views.admin_dashboard),
    url(r'^shopping_cart$', views.shopping_cart),
    url(r'^logout$', views.logout),
    url(r'^process_login$', views.process_login),
    url(r'^add_service$', views.add_service),
    url(r'^add_to_cart$', views.add_to_cart),
    url(r'^send_message$', views.send_message),
    url(r'^remove_message$', views.remove_message),
    url(r'^make_purchase$', views.make_purchase),
    url(r'^deliver_order$', views.deliver_order),
    url(r'^delete_delivered$', views.delete_delivered),
    url(r'^remove_existing$', views.remove_existing),
    url(r'^remove_item_from_cart$', views.remove_item_from_cart),
    url(r'^process_registration$', views.process_registration),
]
