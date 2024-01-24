from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView
# from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, loginLogoutReport

# , loginLogoutReport
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
# from .views import LoginLogoutReportView

# from .models import StockIn, StockOut
# from .models import Product
# from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView

# from .views import requestTck, requestLOg  # Make sure this is the correct import path
# from django.views.generic import requestTck, requestLog

# Your views or functions using requestTck and requestLog


class Index(TemplateView):
	template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

		low_inventory = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)

		if low_inventory.count() > 0:
			if low_inventory.count() > 1:
				messages.error(request, f'{low_inventory.count()} items have low inventory')
			else:
				messages.error(request, f'{low_inventory.count()} item has low inventory')

		low_inventory_ids = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

		return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'
# #J9!aLp2wZ$
class ProductReports(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/products_reports.html'
    context_object_name = 'items'
    
class StockView(LoginRequiredMixin, TemplateView):
    model = InventoryItem
    template_name = 'inventory/stock_reports.html'
    # context_object_name = 'items'
#     # return render(request, 'stock_reports.html', {'stock_in_history': stock_in_history, 'stock_out_history': stock_out_history})
    

# # def product_report(request):
# #     products = Product.objects.all()
# #     return render(request, 'product_report.html', {'products': products})
class LoginLogoutReportView(LoginRequiredMixin, TemplateView):  # Updated class name
    model = InventoryItem
    template_name = 'inventory/login_logout_report.html'
