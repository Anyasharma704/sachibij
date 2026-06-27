from django.shortcuts import render
from verification.models import Product

def home(request):
    result = None
    result_type = None
    if request.GET.get('barcode'):
        barcode = request.GET.get('barcode')
        try:
            product = Product.objects.get(barcode=barcode)
            if product.company.is_verified:
                result = "✅ GENUINE — " + product.name + " by " + product.company.name
                result_type = "genuine"
            else:
                result = "⚠️ WARNING — Company not verified!"
                result_type = "warning"
        except Product.DoesNotExist:
            result = "❌ NOT FOUND — Barcode not in our database"
            result_type = "notfound"
    return render(request, 'verification/index.html', {'result': result, 'result_type': result_type})