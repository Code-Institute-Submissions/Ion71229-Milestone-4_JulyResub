from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from .models import MenuItem, OrderModel

from .forms import MenuForm


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        total_revenue = 0

        unshipped_orders = []

        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)
        
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }
        return render(request, 'restaurant/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class Order(View):
    def get(self, request, *args, **kwargs):
        starters = MenuItem.objects.filter(category__name__contains='Starter')
        maincourses = MenuItem.objects.filter(category__name__contains='MainCourse')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')

        context = {
            'starters': starters,
            'maincourses': maincourses,
            'desserts': desserts,
            'drinks': drinks,
        }
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        # Get input fields at the bottom of the order template
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        town = request.POST.get('town')
        county = request.POST.get('county')
        post_code = request.POST.get('post')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menuitem = MenuItem.objects.get(pk=item)
            item_data = {
                'id': menuitem.pk,
                'name': menuitem.name,
                'price': menuitem.price,
            }
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            town=town,
            county=county,
            post_code=post_code
        )
        order.items.add(*item_ids)

        return render(request, 'customer/order_confirmation.html', context)

class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {'order': order}

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()
        
        context = {'order': order}
        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class Menu(View):
    def get(self, request, *args, **kwargs):
        menuitem = MenuItem.objects.all()

        context = {
            'menuitem': menuitem,
        }

        return render(request, 'restaurant/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menuitems = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menuitems': menuitems
        }
        return render(request, 'restaurant/menu.html', context)


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('menu'))
    else:
        form = MenuForm()
    template = 'restaurant/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, menuitem):
    """ Edit a product in the store """
    menuitem = get_object_or_404(MenuItem, pk=menuitem)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menuitem)
        if form.is_valid():
            form.save()
            return redirect(reverse('menu'))
    else:
        form = MenuForm(instance=menuitem)

    template = 'restaurant/edit_product.html'
    context = {
        'form': form,
        'menuitem': menuitem,
    }

    return render(request, template, context)
