from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .models import Product, Category

def is_htmx(request):
    return request.headers.get('HX-Request') == 'true'

@cache_page(60 * 15)
@vary_on_headers('HX-Request')
def catalog_list(request, slug=None):
    category = None
    products = Product.objects.filter(is_active=True).prefetch_related('images')

    categories = Category.objects.filter(parent__isnull=True)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    # Filtering
    shape = request.GET.get('shape')
    material = request.GET.get('material')
    sort_by = request.GET.get('sort')

    if shape:
        products = products.filter(shape__iexact=shape)
    if material:
        products = products.filter(frame_material__iexact=material)

    # Sorting
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # Get available filters (this could be cached in production)
    shapes = Product.objects.values_list('shape', flat=True).distinct().order_by('shape')
    materials = Product.objects.values_list('frame_material', flat=True).distinct().order_by('frame_material')

    context = {
        'products': products,
        'categories': categories,
        'category': category,
        'is_htmx': is_htmx(request),
        'available_shapes': shapes,
        'available_materials': materials,
        'current_filters': {
            'shape': shape,
            'material': material,
            'sort': sort_by
        }
    }

    if is_htmx(request):
        return render(request, 'catalog/partials/list_content.html', context)
    
    return render(request, 'catalog/list.html', context)

@cache_page(60 * 15)
@vary_on_headers('HX-Request')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Related products: Same category, exclude current, random 2
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id).prefetch_related('images').order_by('?')[:2]
    
    context = {
        'product': product,
        'related_products': related_products,
        'is_htmx': is_htmx(request)
    }

    if is_htmx(request):
        return render(request, 'catalog/partials/detail_content.html', context)
    
    return render(request, 'catalog/detail.html', context)



from django.db.models import Q

def search_products(request):
    """
    HTMX: Returns filtered product rows.
    """
    query = request.GET.get('q', '')
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        , is_active=True).select_related('category').prefetch_related('images')[:10]

    return render(request, 'catalog/partials/search_results.html', {'products': products})
