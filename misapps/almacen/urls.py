from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home, register_admin, login, exit
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('ppe/create/', views.create_ppe, name='create_ppe'),
    path('ppe/create/table/', views.PersonalProtectionEquipment, name='table_created_ppe'),
    path('ppe/duration/table/', views.show_duration, name='table_duration_ppe'),
    path('update-ppe-duration/', views.update_ppe_duration, name='update_ppe_duration'),
    path('ppe/show/table/', views.set_duration, name='show_duration_table'),
    path('ppe/add/', views.add_ppe, name='add_ppe'),
    path('ppe/add/table/', views.show_added_ppe, name='table_added_ppe'),
    path('add_quantity/<str:id>/', views.add_quantity, name='add_ppe_quantity'),
    path('ppe/modify/<str:id>/', views.modify_ppe, name='modify_ppe'),
    path('ppe/delete/<str:id>/', views.delete_ppe, name='delete_ppe'),
    path('ppe/total_ppe_stock/', views.total_ppe_stock, name='total_ppe_stock'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/delete/<str:id>/', views.delete_equipment, name='delete_equipment'),
    path('equipment/modify/<str:id>/', views.modify_equipment, name='modify_equipment'),
    path('equipment/create/', views.create_equipment, name='create_equipment'),
    path('equipment/total_equipment_stock/', views.total_equipment_stock, name='total_equipment_stock'),
    path('material/', views.material_list, name='material_list'),
    path('material/create/', views.create_material, name='create_material'),
    path('materials/modify/<str:id>/', views.modify_material, name='modify_material'),
    path('materials/delete/<str:id>/', views.delete_material, name='delete_material'),
    path('materials/total_material_stock/', views.total_material_stock, name='total_material_stock'),
    path('tool/', views.tool_list, name='tool_list'),
    path('tool/create/', views.create_tool, name='create_tool'),
    path('tool/delete/<str:id>/', views.delete_tool, name='delete_tool'),
    path('tool/modify/<str:id>/', views.modify_tool, name='modify_tool'),
    path('tool/total_tool_stock/', views.total_tool_stock, name='total_tool_list'),
    path('worker/', views.worker_list, name='worker_list'),
    path('worker/create/', views.create_worker, name='create_worker'),
    path('worker/delete/<int:id>/', views.delete_worker, name='delete_worker'),
    path('worker/modify/<int:id>/', views.modify_worker, name='modify_worker'),
    path('loan/', views.loan_list, name='loan_list'),
    path('loan/create/', views.create_loan, name='create_loan'),
    path('loan/delete/<int:id>/', views.delete_loan, name='delete_loan'),
    path('loan/modify/<int:id>/', views.modify_loan, name='modify_loan'),
    path('ppeloan/', views.ppe_loan_list, name='ppe_loan_list'),
    path('ppeloan/create/', views.create_ppe_loan, name='create_ppe_loan'),
    path('ppeloan/create/exception/', views.exception_ppe_loan, name='exception_ppe_loan'),
    path('ppeloan/delete/<int:id>/', views.delete_ppe_loan, name='delete_ppe_loan'),
    path('ppeloan/modify/<int:id>/', views.modify_ppe_loan, name='modify_ppe_loan'),
    path('register_admin/', register_admin, name='register_admin'),
    path('login/', login, name='login'),
    path('logout/', exit, name='exit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)