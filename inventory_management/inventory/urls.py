from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, ProductReports, LoginLogoutReportView, StockView

# ProductReports,stock_reports,login_logout_report
from django.contrib.auth import views as auth_views
from .views import LoginLogoutReportView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('product-reports/', ProductReports.as_view(), name='product-reports'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    
    path('stock-reports/', StockView.as_view(template_name='inventory/stock_reports.html'), name='stock_reports'),
    # path('product-report/', product_report, name='product_report'),
    path('login-logout-report/', LoginLogoutReportView.as_view(template_name='inventory/login_logout_report.html'), name='login_logout_report'),
]

# from django.urls import path
# from .views import loginLogoutReport

# urlpatterns = [
#     # ... other patterns
#     path('login-logout-report/', loginLogoutReport.as_view(), name='login-logout-report'),
# ]



