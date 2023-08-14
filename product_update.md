By default, no products in the database have 'has_sizes' as a field.

To update, run python3 manage.py shell then execute following:

1. from products.models import Product
2. kdbb = ['kitchen_dining', 'bed_bath']
3. clothes = Product.objects.exclude(category__name__in=kdbb)
4. clothes.count()
5. for item in clothes:
    item.has_sizes = True
    item.save()
6. Product.objects.filter(has_sizes=True).count()