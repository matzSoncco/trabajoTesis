from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from .models.Ppe import Ppe
from .models.PpeLoan import PpeLoan, PpeLoanDetail
from .models.Equipment import Equipment
from .models.Worker import Worker
from .models.Material import Material
from .models.Loan import Loan
from .models.Tool import Tool
from .forms import AdminSignUpForm, PpeForm, MaterialForm, WorkerForm, EquipmentForm, ToolForm, LoanForm, PpeLoanForm, Ppe, ExceptionPpeLoanForm, PpeLoanDetailForm, PpeLoanDetailForm, CreatePpeForm


logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'home.html')

#DURACIÓN
@login_required
def set_duration(request):
    form = PpeForm()
    return render(request, 'show_duration_table.html', {'form': form})

@require_POST
@csrf_exempt  # Solo para pruebas, eliminar en producción
def update_ppe_duration(request):
    ppe_id = request.POST.get('ppe_id')
    new_duration = request.POST.get('duration')
    
    logger.info(f"Recibida solicitud de actualización: PPE ID {ppe_id}, Nueva duración {new_duration}")
    
    try:
        ppe = Ppe.objects.get(idPpe=ppe_id)
        logger.info(f"PPE encontrado: {ppe}")
        
        ppe.duration = new_duration
        ppe.save()
        
        logger.info(f"PPE actualizado: {ppe}")
        return JsonResponse({'success': True})
    except Ppe.DoesNotExist:
        logger.error(f"PPE no encontrado: ID {ppe_id}")
        return JsonResponse({'success': False, 'error': 'PPE not found'})
    except Exception as e:
        logger.error(f"Error al actualizar PPE: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})
    
@login_required
def show_duration(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    return render(request, 'table_duration_ppe.html', {'epp': epp, 'query': query})

#PPE
@login_required
def PersonalProtectionEquipment(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    print(f"Número de PPEs encontrados: {epp.count()}")  # Añade este print
    return render(request, 'table_created_ppe.html', {'epp': epp, 'query': query})

def show_added_ppe(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    print(f"Número de PPEs encontrados: {epp.count()}")  # Añade este print
    return render(request, 'table_added_ppe.html', {'epp': epp, 'query': query})

@login_required
def create_ppe(request):
    if request.method == 'POST':
        form = CreatePpeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                ppe = form.save()
                print(f"PPE creado: {ppe.idPpe} - {ppe.name}")
                messages.success(request, f'PPE "{ppe.name}" creado exitosamente.')
                return redirect('create_ppe')
            except Exception as e:
                print(f"Error al guardar PPE: {str(e)}")
                messages.error(request, f'Error al crear PPE: {str(e)}')
        else:
            print("Errores del formulario:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Campo {field}: {error}")
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CreatePpeForm()
    return render(request, 'create_ppe.html', {'form': form})

@login_required
def add_ppe(request):
    if request.method == 'POST':
        form = PpeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_ppe')
    else:
        form = PpeForm()
    return render(request, 'add_ppe.html', {'form': form})

@login_required
def add_quantity(request, id):
    try:
        epp = get_object_or_404(Ppe, idPpe=id)
        form = AddQPpeForm(request.POST)
        if form.is_valid():
            quantity_to_add = form.cleaned_data['quantity']
            epp.quantity += quantity_to_add
            epp.save()
            return JsonResponse({'success': True, 'new_quantity': epp.quantity})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Esto imprimirá el traceback completo en la consola del servidor
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def delete_ppe(request, id):
    epp = get_object_or_404(Ppe, idPpe=id)
    
    if request.method == 'DELETE':
        epp.delete()
        return redirect('ppe')
    else:
        return render(request, 'delete_ppe.html', {'epp': epp})

@login_required
def modify_ppe(request, id):
    epp = get_object_or_404(Ppe, idPpe=id)
    form = PpeForm(instance=epp)

    if request.method == 'POST':
        form = PpeForm(request.POST, instance=epp)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('add_ppe')
    else:
        return render(request, 'modify_ppe.html', {'form': form, 'id': id})

@login_required 
def total_ppe_stock(request):
    total_stock = Ppe.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#EQUIMENT
@login_required
def equipment_list(request):
    query = request.GET.get('q')
    if query:
        equipment = Equipment.objects.filter(name__icontains=query)
    else:
        equipment = Equipment.objects.all()
    return render(request, 'equipment_list.html', {'equipment': equipment, 'query': query})

@login_required
def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'create_equipment.html', {'form': form})

@login_required
def delete_equipment(request, id):
    equipment = get_object_or_404(Equipment, idEquipment=id)
    
    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment_list')
    else:
        return render(request, 'delete_ppe.html', {'equipment': equipment})

@login_required
def modify_equipment(request, id):
    equipment = get_object_or_404(Equipment, idEquipment=id)
    form = EquipmentForm(instance=equipment)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('equipment_list')
    else:
        return render(request, 'modify_equipment.html', {'form': form})

login_required
def total_equipment_stock(request):
    total_stock = Equipment.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#MATERIAL
@login_required
def material_list(request):
    query = request.GET.get('q')
    if query:
        materials = Material.objects.filter(name__icontains=query)
    else:
        materials = Material.objects.all()
    return render(request, 'material_list.html', {'materials': materials, 'query': query})

@login_required
def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'create_material.html', {'form': form})

@login_required
def delete_material(request, id):
    material = get_object_or_404(Material, idMaterial=id)
    
    if request.method == 'POST':
        material.delete()
        return redirect('material_list')
    else:
        return render(request, 'delete_material.html', {'material': material})

@login_required   
def modify_material(request, id):
    material = get_object_or_404(Material, idMaterial=id)
    form = MaterialForm(instance=material)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('material_list')
    else:
        return render(request, 'modify_material.html', {'form': form})

@login_required 
def total_material_stock(request):
    total_stock = Material.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#TOOLS
@login_required
def tool_list(request):
    query = request.GET.get('q')
    if query:
        tools = Tool.objects.filter(name__icontains=query)
    else:
        tools = Tool.objects.all()
    return render(request, 'tool_list.html', {'tools': tools, 'query': query})

@login_required
def create_tool(request):
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tool_list')
    else:
        form = ToolForm()
    return render(request, 'create_tool.html', {'form': form})

@login_required
def delete_tool(request, id):
    tools = get_object_or_404(Tool, idTool=id)
    
    if request.method == 'POST':
        tools.delete()
        return redirect('tool_list')
    else:
        return render(request, 'delete_ppe.html', {'tools': tools})

@login_required
def modify_tool(request, id):
    tools = get_object_or_404(Tool, idTool=id)
    form = ToolForm(instance=tools)

    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tools)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('tool_list')
    else:
        return render(request, 'modify_tool.html', {'form': form})

login_required
def total_tool_stock(request):
    total_stock = Tool.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#WORKER
@login_required
def worker_list(request):
    query = request.GET.get('q')
    if query:
        workers = Worker.objects.filter(name__icontains=query)
    else:
        workers = Worker.objects.all()
    return render(request, 'worker_list.html', {'workers': workers, 'query': query})

@login_required
def create_worker(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save()
            return JsonResponse({'success': True, 'message': 'Trabajador creado con éxito'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = WorkerForm()
    return render(request, 'create_worker.html', {'form': form})

@login_required
def delete_worker(request, id):
    workers = get_object_or_404(Worker, dni=id)

    if request.method == 'POST':
        workers.delete()
        return redirect('worker_list')
    else:
        return render(request, 'delete_worker.html', {'workers': workers})
    
@login_required
def modify_worker(request, id):
    workers = get_object_or_404(Worker, dni=id)
    form = WorkerForm(instance=workers)

    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=workers)
        if form.is_valid():
            form.save()
            return redirect('worker_list')
    else:
        return render(request, 'modify_worker.html', {'form': form})

#LOAN
@login_required
def loan_list(request):
    query = request.GET.get('q')
    if query:
        loans = Loan.objects.filter(worker__name__icontains=query)
    else:
        loans = Loan.objects.all()
    return render(request, 'loan_list.html', {'loans': loans, 'query': query})

@login_required
def create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'create_loan.html', {'form': form})

@login_required
def delete_loan(request, id):
    loans = get_object_or_404(Loan, idLoan=id)
    
    if request.method == 'POST':
        loans.delete()
        return redirect('loan_list')
    else:
        return render(request, 'delete_loan.html', {'loans': loans})
    
@login_required
def modify_loan(request, id):
    loans = get_object_or_404(Loan, idLoan=id)
    form = LoanForm(instance=loans)

    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loans)
        if form.is_valid():
            form.save()
            return redirect('loan_list')
    else:
        return render(request, 'modify_loan.html', {'form': form})
    
#PPELOAN
@login_required
def ppe_loan_list(request):
    query = request.GET.get('q')
    if query:
        ppe_loans = PpeLoan.objects.filter(worker__name_icontains=query)
    else:
        ppe_loans = PpeLoan.objects.all()
    print(f"Número de préstamos: {ppe_loans.count()}")
    print(f"Préstamos: {list(ppe_loans)}")
    return render(request, 'ppe_loan_list.html', {'ppe_loans': ppe_loans, 'query': query})

@login_required
def create_ppe_loan(request):
    PpeLoanDetailFormSet = inlineformset_factory(PpeLoan, PpeLoanDetail, form=PpeLoanDetailForm, extra=1)

    if request.method == 'POST':
        form = PpeLoanForm(request.POST)
        formset = PpeLoanDetailFormSet(request.POST, instance=form.instance)

        if form.is_valid() and formset.is_valid():
            ppe_loan = form.save()
            formset.instance = ppe_loan
            formset.save()

            # Update stock
            for form_detail in formset:
                ppe = form_detail.cleaned_data.get('ppe')
                quantity = form_detail.cleaned_data.get('quantity')
                if ppe and quantity:  # Check if both ppe and quantity are provided
                    ppe.stock -= quantity
                    ppe.save()

            return redirect('ppe_loan_list')
    else:
        form = PpeLoanForm()
        formset = PpeLoanDetailFormSet(instance=form.instance)

    return render(request, 'create_ppe_loan.html', {'form': form, 'formset': formset})

@login_required
def exception_ppe_loan(request):
    if request.method == 'POST':
        form = ExceptionPpeLoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ppe_loan_list')
    else:
        form = ExceptionPpeLoanForm()
    return render(request, 'exception_ppe.html', {'form': form})

@login_required
def delete_ppe_loan(request, id):
    ppe_loans = get_object_or_404(PpeLoan, idPpeLoan=id)
    
    if request.method == 'POST':
        ppe_loans.delete()
        return redirect('ppe_loan_list')
    else:
        return render(request, 'delete_ppe_loan.html', {'ppe_loans': ppe_loans})
    
@login_required
def modify_ppe_loan(request, id):
    ppe_loans = get_object_or_404(PpeLoan, idPpeLoan=id)

    if request.method == 'POST':
        form = PpeLoanForm(request.POST, request.FILES, instance=ppe_loans)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('ppe_loan_list')
    else:
        return render(request, 'modify_ppe_loan.html', {'form': form})
    
#REGISTER
def register_admin(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AdminSignUpForm()
    return render(request, 'register_admin.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('home')