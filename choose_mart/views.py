from django.shortcuts import render
from store.models import Product


from django.conf import settings
def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products
    }
    return render(request, 'home.html', context)

    