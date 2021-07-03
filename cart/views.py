# import self as self
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
# from .models import items
from django.http import JsonResponse
# from django.contrib
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import items, OrderItem, Order, Address, Payment, Category, Review, ReviewForm, Brand, Color, Person
from django.db.models import Q
from django.template.loader import render_to_string
import stripe
from django.contrib import messages
from .forms import checkout_form, SearchForm
from django.core.paginator import Paginator


stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

class HomeView(ListView):
    context_object_name = 'name'
    template_name = 'index.html'
    queryset = items.objects.all()
    ordering = ['id']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['product'] = items.objects.all()
        context['colors'] = Color.objects.filter()
        context['person_type'] = Person.objects.all()
        return context


class ItemDetailView(DetailView):
    model = items
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter()
        context['product'] = self.queryset
        return context

def categories(request, category_slug=None):
    categories = Category.objects.all()
    product = items.objects.filter(available=True)
    colors= Color.objects.all()
    person_type= Person.objects.all()
    brands=Brand.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = items.objects.filter(category=category)
    context = {'category': category,
               'product': product,
               'categories': categories,
               'brands':brands,
               'colors' :colors,
               'person_type' :person_type,
               }
    return render(request, "index.html", context)

def brands(request, brand_slug=None):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    product = items.objects.filter(available=True)
    colors = Color.objects.all()
    person_type = Person.objects.all()
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        product = items.objects.filter(brand=brand)
    context = {
        'brand': brand,
        'product': product,
        'brands': brands,
        'colors':colors,
        'person_type':person_type,
        'categories' :categories,
    }
    return render(request, "index.html", context)

# Filter Data
def filter_data(request):
    colors = request.GET.getlist('color[]')
    person = request.GET.getlist('person[]')
    allProducts = items.objects.all().order_by('-id').distinct()
    if len(colors) > 0:
        allProducts = allProducts.filter(color__id__in=colors).distinct()
    if len(person) > 0:
        allProducts = allProducts.filter(person__id__in=person).distinct()

    t = render_to_string('filter_product_list.html', {'data': allProducts})
    return JsonResponse({'data': t})

def product(request, slug, id):
    products = get_object_or_404(items, id=id, slug=slug, available=True)
    context = {
        'products': products,
    }
    return render(request, 'cart.html', context)


@login_required
def cart_add_item(request, slug):
    item = get_object_or_404(items, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    details = Order.objects.filter(user=request.user, ordered=False)
    if details.exists():
        order = details[0]
        if order.product.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "item is updated to cart")
            return redirect("cart:product", slug=slug)
        else:
            order.product.add(order_item)
            messages.info(request, "item is added to cart")
            return redirect("cart:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        messages.info(request, "item is added to cart")
        order.product.add(order_item)
        return redirect("cart:product", slug=slug)


@login_required
def home_add_item(request, slug):
    item = get_object_or_404(items, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    details = Order.objects.filter(user=request.user, ordered=False)
    if details.exists():
        order = details[0]
        # if order item is in the order
        if order.product.filter(item__slug=item.slug).exists():
            messages.info(request, "item is already in cart")
            return redirect("/")
        else:
            order.product.add(order_item)
            messages.info(request, "item is added to cart")
            return redirect("/", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_item)
        messages.info(request, "item is added to cart")
        return redirect("/", slug=slug)


@login_required
def add_qty(request, slug):
    item = get_object_or_404(items, slug=slug)
    details = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if details.exists():
        order = details[0]
        if order.product.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity += 1
            order_item.save()
            return redirect("cart:order-details")


@login_required
def delete_item(request, slug):
    item = get_object_or_404(items, slug=slug)
    details = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if details.exists():
        order = details[0]
        # check if the order item is in the order
        if order.product.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                user=request.user,
                item=item,
                ordered=False
            )[0]
            order.product.remove(order_item)
            order_item.delete()
            messages.info(request, "This item is removed from your cart.")
            return redirect("cart:product", slug=slug)
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("cart:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:product", slug=slug)


@login_required
def remove_qty(request, slug):
    item = get_object_or_404(items, slug=slug)
    details = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if details.exists():
        order = details[0]
        # check if the order item is in the order
        if order.product.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                Order.product.remove(order_item)
            return redirect("cart:order-details")


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_details.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No active order")
            return redirect("/")


class checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user).last()
        form = checkout_form()
        context = {
            'form': form,
            'order': order,
        }
        return render(self.request, "checkout.html", context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if request.method == 'POST':
            full_name = request.POST['full_name']
            address = request.POST['address']
            address2 = request.POST['address2']
            form_checkout = checkout_form(request.POST)
            if form_checkout.is_valid():
                country = form_checkout.cleaned_data['country']
            state = request.POST['state']
            city = request.POST['city']
            zip = request.POST['zip']
            print(full_name, address, address2, country, state, city, zip)
            bill_address = Address(
                user=self.request.user,
                full_name=full_name,
                address=address,
                address2=address2,
                country=country,
                state=state,
                city=city,
                zip=zip,
            )
            bill_address.save()
            messages.info(request, "Address Saved Successfully!")
            return redirect("cart:checkout")
        messages.warning(request, "failed to checkout")
        return redirect("cart:checkout")

class payment(View):
    def get(self, *rgs, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        add=Address.objects.filter(user=self.request.user)
        if add.exists():
            context = {
            'order': order,
        }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("cart:checkout")
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        # token = self.request.POST.get('stripeToken')
        amount = int(order.get_total()* 100)
        try:
            payment = Payment()
            # payment.stripe_charges_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()
            order.ordered = True  # assign the payment to the  return render(request,) order
            order.payment = payment
            order.save()

            messages.success(request,"Your Order was successfully Done!.......... Buy Again")
            return redirect("/")
        except stripe.error.CardError as e:
            body = e.json_body
            error = body.get('error', {})

            messages.error(self.request, f"{error.get('message')}")
            return redirect("cart:payment")

        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Rate limit error")

        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid Parameter")
            return redirect("cart:payment")
        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Authentication Error")
            return redirect("cart:payment")
        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network connection Error")
            return redirect("cart:payment")
        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong,Please Try Again!!!!")
            return redirect("cart:payment")
        # messages.warning(self.request, "Invalid data received")
        # return redirect("cart:payment")

def wish_list(request):
    return render(request, "final_notify.html")


def search(request):
    categories = Category.objects.all()
    colors = Color.objects.all()
    person_type = Person.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        query = request.POST['query']
        if query:
            if len(query) > 78:
                result = items.objects.none()
            else:
                result = items.objects.filter(title__icontains=query)
            if result.count() == 0:
                messages.warning(request, "no search result found. Please refine your query")
            context = {
                'result': result,
                'query': query,
                'brands': brands,
                'colors': colors,
                'person_type': person_type,
                'categories': categories,
            }
            return render(request, 'search.html', context)

    #


def review(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # check post
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = Review()  # create relation with model
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.item_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            print("comment")
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
