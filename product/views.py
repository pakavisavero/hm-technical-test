from django.urls import path
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from engine.decorators import role_required

@method_decorator([login_required, role_required(["manager", "user", "public"])], name="dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"

@method_decorator([login_required, role_required(["manager", "user"])], name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = "/product"

    def form_valid(self, form):
        messages.success(self.request, "Product added successfully!")
        return super().form_valid(form)

@method_decorator([login_required, role_required(["manager", "user"])], name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = "/product"

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully!")
        return super().form_valid(form)

@method_decorator([login_required, role_required(["manager"])], name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product/product_confirm_delete.html"
    success_url = "/product"

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Product deleted successfully!")
        return super().post(request, *args, **kwargs)

