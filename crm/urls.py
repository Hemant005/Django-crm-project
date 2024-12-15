from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    path('',views.home,name='home'),
    path('clients',views.clients_view,name='clients'),
    path('opportunities',views.opportunities_view,name='opportunities'),
    path('products',views.products_view,name='products'),
    path('invoices',views.invoice_view,name='invoices'),
    path('add_client/', views.add_client, name='add_client'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_opportunity/', views.add_opportunity, name='add_opportunity'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('create_shippings/',views.create_shipping,name='create_shipping'),
    path('shippings/',views.Shipping_view,name='shippings'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('login/', LoginView.as_view(template_name='crm/login.html'), name='login'),
    path('logout/', views.Logout_View, name='logout'),
    path('clients/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:client_id>/',views.delete_client, name='delete_client'),
    path('opportunities/edit/<int:opportunity_id>/', views.edit_opportunity, name='edit_opportunity'),
    path('opportunities/delete/<int:opportunity_id>/',views.delete_opportunity, name='delete_opportunity'),
    path('invoices/edit/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('invoices/delete/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('shippings/edit/<int:shipping_id>/', views.edit_shipping, name='edit_shipping'),
    path('shippings/delete/<int:shipping_id>/', views.delete_shipping, name='delete_shipping'),
    path('profile/',views.profile_view,name='profile'),
    path('export_invoices/', views.export_invoices, name='export_invoices'),
    path('export_invoice/<int:invoice_id>/', views.export_invoice_pdf, name='export_invoice_pdf'),
    path('top-orders/', views.top_orders_view, name='top_orders'),
]