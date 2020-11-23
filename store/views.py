from .models import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.generic import ListView, DetailView, View

# Create your views here.
def home(request):
   books = Book.objects.filter(is_featured=True).order_by('?')
   context = {
      'books': books,
   }
   return render(request, 'store/home.html', context)


def product(request):
   books = Book.objects.all()
   context = {'books': books}
   return render(request, 'store/product.html', context)


class BookDetailView(DetailView):
   model = Book
   """ paginate_by = 20"""
   #queryset = Product.objects.get(pk=pk)
   template_name = "store/detail.html"
   
   def get_context_data(self, *args, **kwargs):
      context = super(BookDetailView, self).get_context_data(*args, **kwargs)
      context['featured'] = Book.objects.filter(is_featured=True)
      return context

def add_to_cart(request, slug):
   book = get_object_or_404(Book, slug=slug)
   order_item, created = OrderBook.objects.get_or_create(
      book=book,
      user= request.user,
      ordered = False
      )
   order_qs =  Order.objects.filter(user=request.user, ordered=False)
   if order_qs.exists():
      order = order_qs[0]
      # Checks if book is in order
      if  order.books.filter(book__slug=book.slug).exists():
         order_item.quantity += 1
         order_item.save()
         messages.success(request, "This book's quantity has been updated.")
         
      else:
         order.books.add(order_item)
         messages.success(request, "This book has been added to your cart.")
         
         
   else:
      ordered_date = timezone.now()
      order = Order.objects.create(user=request.user, ordered_date=ordered_date)
      order.books.add(order_item)
      
   return redirect('book-detail', slug=slug)


class CartSummaryView(LoginRequiredMixin, View):
   def get(self, *args, **kwargs):
      try:
         order = Order.objects.filter(user=self.request.user, ordered=False)
         
         context = {
            'object':order,
         }
         return render(self.request, 'store/cart.html', context)
      except ObjectDoesNotExist:
         messages.warning(self.request, "You don't have any active Orders")
         return redirect("/")
      return render(self.request, 'store/cart.html')


class SearchBooks(ListView):
   template_name = 'store/search.html'
   paginate_by = 10
   
   def get(self, *args, **kwargs):
      #category = Category.objects.all()

      context = {
         #'category':category
      }
      return render(self.request, 'store/search.html', context)
   
   def get_queryset(self, *args, **Kwargs): 
      request = self.request
      query = request.GET.get('q')
      if query is not None:
         lookups = Q(name__icontains=query)|Q(brand__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query)
         return Book.objects.filter(lookups).distinct()
      return Book.objects.none()