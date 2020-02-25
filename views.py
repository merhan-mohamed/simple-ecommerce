

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import View
from django.conf import settings
from post import POST
from urllib3 import HTTPResponse
from Cart.forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from Cart.models import Item, OrderItem, Order, Payment, Coupon, Refund, UserProfile, BillingAddress, Address
from django.contrib.auth.models import User

import stripe
import random
import string
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


#ref_code

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20 ))


# the cart
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, orderd=False)
    order_qs = Order.objects.filter(user=request.user, orderd=False)
    if order_qs.exists():
        print(order_qs)
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated')
            return redirect('Cart:order_summary')
        else:
            order.item.add(order_item)
            messages.info(request, 'This item was added to your cart')
            return redirect('Cart:order_summary')
    else:
        orderd_date = timezone.now()
        order = Order.objects.create(user=request.user, orderd_date= orderd_date)
        order.item.add(order_item)
        messages.info(request, 'This item was added to your cart')
        return redirect('Cart:order_summary')


@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, orderd=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, orderd=False)[0]
            order.item.remove(order_item)
            messages.info(request, 'This item was removed from your cart')

        else:
           messages.info(request, 'This item was not in your cart')
    else:
       messages.info(request, 'you do not have an active order')
    return redirect('Cart:order_summary')

class OrderSummaryView(LoginRequiredMixin , View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,orderd=False)
            return render(self.request, 'order_summary.html', {'object':order})
        except ObjectDoesNotExist:
            messages.error(self.request,'you do not have an active order')
            return redirect('/product/')



def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, orderd=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, orderd=False)[0]
            if order_item.quantity > 1 :
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            messages.info(request, 'This item quantity was updated')

        else:
           messages.info(request, 'This item was not in your cart')
    else:
       messages.info(request, 'you do not have an active order')
    return redirect('Cart:order_summary')



def is_valid_form(values):
    valid = True
    for field in values:
        if field =='':
            valid = False
    return valid

class  CheckoutView(View):
    def get(self, *args,**kwargs):
        try:
            order = Order.objects.get(user= self.request.user,orderd=False)
            form = CheckoutForm()
            context = {
                 'form': form,
                 'couponform': CouponForm(),
                 'order': order,
                 'DISPLAY_COUPON_FORM':True
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                  user=self.request.user,
                  address_type='B',
                  default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            return render(self.request, 'checkout.html',context)
        except ObjectDoesNotExist:
             messages.info(self.request,'you do not have an active order')
             return redirect('Cart:order_summary')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None )
        try:
            order = Order.objects.get(user=self.request.user, orderd=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping :
                      print('Using the default shipping address')
                      address_qs = Address.objects.filter(
                          user=self.request.user,
                          address_type='S',
                          default=True
                      )
                      if address_qs.exists():
                           shipping_address = address_qs[0]
                           order.shipping_address = shipping_address
                           order.save()
                      else:
                          messages.info(self.request,'No default shipping address available')
                          return redirect('Cart:checkout')
                else:
                    print('User is entering a new shipping address')
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get(' shipping_zip')
                    print(' shipping_address1','shipping_address2 ','shipping_country ','shipping_zip')
                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user =self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip= shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, 'please fill in the required shipping address fields')


                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                if same_billing_address :
                    billing_address = shipping_address
                    billing_address.pk =None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print('Using the default billing address')
                    address_qs = BillingAddress.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()


                    else:
                        messages.info(self.request, 'No default billing address available')
                        return redirect('Cart:checkout')
                else:
                    print('User is entering a new shipping address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get(' billing_zip')
                    print('billing_address1', 'billing_country','billing_zip')
                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user = self.request.user,
                            street_address= street_address,
                            apartment_address= apartment_address,
                            country=country,
                            zip=zip,
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                        else:
                            messages.info(self.request, 'please fill in the required billing address fields')
            payment_option = form.cleaned_data.get('payment_option')
            if payment_option == 'S':
                return redirect('Cart:payment', payment_option ='stripe')
            elif payment_option == 'P':
                return redirect('Cart:payment', payment_option = 'paypal')
            else:
                messages.warning(self.request, 'Invalid payment option selected')
                return redirect('Cart:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect('Cart:order_summary')


class PaymentView(View):
   def get(self, *args, **kwargs):
     order = Order.objects.get(user=self.request.user, orderd=False)
     context = {
                 'order':order,
                  'DISPLAY_COUPON_FORM':False
               }
     return render(self.request, 'payment_info.html', context)
     userprofile = self.request.user.userprofile
     if userprofile.one_click_purchasing:
         cards = stripe.Customer.list_sources(userprofile.stripe_customer_id,Limit=3,object='card')
         card_list = cards['data']
         if len(card_list) > 0 :
            context.update({'card':card_list[0]})
         return render(self.request, 'payment_info.html',context)
   def post (self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, orderd=False)
        form =PaymentForm(self.request.POST or None)
        userprofile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if form.is_valid():
           token = self.request.POST.get('stripeToken')
           save = form.cleaned_data.get('save')
           use_default = form.cleaned_data.get('use_default')
           amount = int(order.get_total())*100
           if save:
                if not userprofile.stripe_customer_id:
                    customer = stripe.Customer.create(email=self.request.user.email, source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()
                else:
                  stripe.Customer.create_source(userprofile.stripe_customer_id, source=token)
        try:
            if use_default:
                 charge = stripe.Charge.create(
                 amount=amount,
                 currency='usd',
                 customer = userprofile.stripe_customer_id
            )
            else:
                charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source= token
            )
                payment = Payment()
                payment.stripe_charge_id = charge
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()
                order_items = order.item.all()
                order_items.update(orderd=True)
                for item in order_items:
                  item.save()
                  order.orderd = True
                  order.payment = payment
                  order.ref_code =create_ref_code()
                  order.save()
                  messages.success(self.request,'your order was successful')
                return redirect("products:product")
        except stripe.error.CardError as e:
               body = e.json_body
               err = body.get('error',{})
               messages.error(self.request, f"{err.get('message')}")
               return redirect('Cart:order_summary')


        except stripe.error.RateLimitError as e:
              # Too many requests made to the API too quickly
               messages.error(self.request, 'Rate Limit Error')
               return redirect('Cart:order_summary')


        except stripe.error.InvalidRequestError as e:
               #Invalid parameters were supplied to Stripe API
               messages.error(self.request, 'Invalid parameters')
               return redirect('Cart:order_summary')


        except stripe.error.AuthenticationError as e:
              #Authentication with Stripes API failed (maybe you changed API keys recently)
              messages.error(self.request, 'Not authenticated')
              return redirect('Cart:order_summary')


        except stripe.error.APIConnectionError as e:
              #Network communication with Stripe failed
              messages.error(self.request, 'Network error')
              return redirect('Cart:order_summary')


        except stripe.error.StripeError as e:
              #Display a very generic error to the user, and maybe send yourself an email
             messages.error(self.request, 'something went wrong.You were not charged.Please try again')
             return redirect('Cart:order_summary')


        except Exception as e:
             #Something else happened, completely unrelated to Stripe
             messages.error(self.request, 'A serious error occurred . We have been notified')
             return redirect('Cart:order_summary')


   def get_coupon(request,code):
        try:
           coupon = Coupon.objects.get(code=code)
           return coupon
        except ObjectDoesNotExist:
            messages.info(request,'This coupon does not exist')
            return redirect('Cart:checkout')

class AddCouponView(View):
   def post(self,*args,**kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, orderd=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'successfully added coupon')
                return redirect('Cart:checkout')
            except ObjectDoesNotExist:
                messages.info(self.request,'you do not have an active order')
                return redirect('Cart:checkout')

            return None

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {'form': form}
        return render(self.request, 'request_refund.html', context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
           ref_code = form.cleaned_data.get('ref_code')
           message = form.cleaned_data.get('message')
           email = form.cleaned_data.get('email')
           try:
               order = Order.objects.get(ref_code=ref_code)
               order.refund_requested = True
               order.save()
               refund = Refund()
               refund.order = order
               refund.reason = message
               refund.email = email
               refund.save()
               messages.info(self.request,'your request was respond')
               return redirect('Cart:RequestRefund')
           except ObjectDoesNotExist:
                messages.info(self.request, 'THis order does not exist')
                return redirect('Cart:RequestRefund')

















