from django.shortcuts import render

from .models import AdminSite

def admin_index(request):
    return render(request, "admin_customizer/admin_index.html", {
        'admins': AdminSite.objects.all(),

    })
