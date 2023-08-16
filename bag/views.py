from django.shortcuts import render, redirect


# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of specified product to the shopping bag """

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
            else:
                # If an item of the same size doesn't exist, set
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # If item is not already in bag, add
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # If no size, run below
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # Add new/updated bag dictionary to session
    request.session['bag'] = bag

    # Returns the user to the same page
    return redirect(redirect_url)
