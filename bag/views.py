from django.shortcuts import render, redirect


# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    # Check to see if 'bag' exists in session, else init empty dic
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # Add new/updated bag dictionary to session
    request.session['bag'] = bag

    # Returns the user to the same page
    return redirect(redirect_url)
