from django.shortcuts import render
from verification.models import Product
from django.utils import timezone

def home(request):
    result = None
    result_type = None
    lang = request.GET.get('lang', 'hl')
    
    if request.GET.get('barcode'):
        barcode = request.GET.get('barcode')
        try:
            product = Product.objects.get(barcode=barcode)
            if not product.company.is_verified:
                if lang == 'hi':
                    result = "❌ नकली — यह कंपनी verified नहीं है!"
                elif lang == 'hl':
                    result = "❌ Nakli — Company verified nahi hai!"
                else:
                    result = "❌ NOT FOUND — Company not verified!"
                result_type = "notfound"
            else:
                batch = product.batch_set.order_by('-manufacturing_date').first()
                if batch and batch.expiry_date < timezone.now().date():
                    if lang == 'hi':
                        result = "⚠️ समय सीमा समाप्त — यह बैच expire हो चुका है!"
                    elif lang == 'hl':
                        result = "⚠️ Expire ho gaya — Yeh batch purana hai!"
                    else:
                        result = "⚠️ EXPIRED — This batch has passed its expiry date!"
                    result_type = "warning"
                else:
                    if lang == 'hi':
                        result = "✅ असली — " + product.name + " · " + product.company.name
                    elif lang == 'hl':
                        result = "✅ Asli — " + product.name + " · " + product.company.name
                    else:
                        result = "✅ GENUINE — " + product.name + " by " + product.company.name
                    result_type = "genuine"
        except Product.DoesNotExist:
            if lang == 'hi':
                result = "❌ नकली — यह barcode हमारे database में नहीं है"
            elif lang == 'hl':
                result = "❌ Nakli — Barcode hamare database mein nahi hai"
            else:
                result = "❌ NOT FOUND — Barcode not in our database"
            result_type = "notfound"
    return render(request, 'verification/index.html', {'result': result, 'result_type': result_type})