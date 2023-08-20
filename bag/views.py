from django.shortcuts import (render, redirect,
                              reverse, HttpResponse, get_object_or_404)
from products.models import Product
from django.contrib import messages


# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # Check to see if 'bag' exists in session, else init empty dic
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                # If an item of the same size already exists, increment
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} '
                                 f'{product.name} quantity to '
                                 f'{bag[item_id]["items_by_size"][size]}.')
            else:
                # If an item of the same size doesn't exist, set
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} '
                                 f'{product.name} to your bag.')
        else:
            # If item is not already in bag, add
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} '
                             f'{product.name} to your bag.')
    else:
        # If no size, run below
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name}'
                             f'quantity to {bag[item_id]}.')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag.')

    # Add new/updated bag dictionary to session
    request.session['bag'] = bag

    # Returns the user to the same page
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} '
                                      f'{product.name} quantity to '
                                      f'{bag[item_id]["items_by_size"][size]}'
                                      f'.')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} '
                                 f'{product.name} from your bag.')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name}'
                             f'quantity to {bag[item_id]}.')
        else:
            bag.pop(item_id)
            messages.succes(f'Removed {product.name} from your bag.')
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove item from the bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} '
                                      f'{product.name} from your bag.')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag.')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
