from django.shortcuts import render
from verification.models import Product
from django.utils import timezone

def home(request):
    result = None
    result_type = None
    if request.GET.get('barcode'):
        barcode = request.GET.get('barcode')
        try:
            product = Product.objects.get(barcode=barcode)
            if not product.company.is_verified:
                result = "❌ Nakli — Company verified nahi hai!"
                result_type = "notfound"
            else:
                batch = product.batch_set.order_by('-manufacturing_date').first()
                if batch and batch.expiry_date < timezone.now().date():
                    result = "⚠️ Expired — Yeh batch expire ho chuka hai!"
                    result_type = "warning"
                else:
                    result = "✅ Asli — " + product.name + " by " + product.company.name
                    result_type = "genuine"
        except Product.DoesNotExist:
            result = "❌ Nakli — Barcode hamare database mein nahi hai"
            result_type = "notfound"
    return render(request, 'verification/index.html', {'result': result, 'result_type': result_type})