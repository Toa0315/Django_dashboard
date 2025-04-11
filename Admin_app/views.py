from django.contrib.auth.models import User
from .models import Payment
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from .forms import CustomUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


# API for stats (last 5 payments)
def api_stats(request):
    values = list(Payment.objects.order_by('-timestamp').values_list('amount', flat=True)[:5])
    return JsonResponse({'values': values[::-1]})


# Simple homepage
def home_view(request):
    return HttpResponse("Welcome to the custom Django Admin!")


# Staff-only custom dashboard
@staff_member_required
def custom_admin_dashboard(request):
    user_count = User.objects.count()
    total_payments = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'appadmin/custom_admin_dashboard.html', {
        'user_count': user_count,
        'total_payments': total_payments,
        'recent_users': recent_users,
    })



# Registration
def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_staff']  # 👈 set staff status
            user.save()
            return redirect('/admin/')  # or 'login' or 'custom_admin_dashboard'
    else:
        form = CustomUserForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('custom_admin_dashboard')  # ✅ this is good
            else:
                return redirect('home_view')  # only for non-staff
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@staff_member_required
def users_page(request):
    users = User.objects.all()
    return render(request, 'appadmin/users.html', {'users': users})

@staff_member_required
def authorization_page(request):
    return render(request, 'appadmin/authorization.html')

@staff_member_required
def reports_page(request):
    return render(request, 'appadmin/reports.html')