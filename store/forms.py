from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Category

class CheckOutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    create_account = forms.BooleanField(required=False, label="Create an account")
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            try:
                profile = user.profile
                self.fields['shipping_address'].initial = profile.address
            except Profile.DoesNotExist:
                pass
            # Hide account creation fields for authenticated users
            self.fields['create_account'].widget = forms.HiddenInput()
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['password'].widget = forms.HiddenInput()
            self.fields['confirm_password'].widget = forms.HiddenInput()
        

    def clean(self):
        cleaned_data = super().clean()
        create_account = cleaned_data.get('create_account')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if create_account:
            if not username or not email or not password or not confirm_password:
                raise forms.ValidationError("All account fields are required to create an account.")
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already taken.")
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already in use.")
            return cleaned_data
        else:
            # If not creating an account, ensure username and email are not provided
            if username or email or password or confirm_password:
                raise forms.ValidationError("Account fields should not be filled if not creating an account.")
            return cleaned_data

class ProductSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label="Search")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )

    def clean(self):
        cleaned_data = super().clean()
        search_query = cleaned_data.get('search_query')
        category = cleaned_data.get('category')
        prohibited_characters ='!@#$%^&*()_+={}[]|\\:;"\`~<>,.?/'
        if search_query:
            if any(char in search_query for char in prohibited_characters):
                raise forms.ValidationError("Search query contains prohibited characters.")
        if category and not isinstance(category, Category):
            raise forms.ValidationError("Invalid category selected.")
        return super().clean()

# from django.urls import reverse_lazy
# from django.views.generic.edit import FormView
# # # This code defines a Django form for checking out, allowing users to enter their shipping address.
# # using set_user method to set the initial value of the shipping address field based on the user's profile.
# class CheckOutFormSet(forms.Form):
#     shipping_address = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your shipping address'})
#     )

#     def set_user(self, user):
#         if user and user.is_authenticated:
#             try:
#                 profile = user.profile
#                 if profile.address:
#                     self.fields['shipping_address'].initial = profile.address
#             except Profile.DoesNotExist:
#                 pass

# class CheckoutView(FormView):
#     template_name = 'store/checkout.html'
#     form_class = CheckOutFormSet
#     success_url = reverse_lazy('store:order_confirmation')

#     def get_form(self):
#         form = super().get_form()
#         form.set_user(self.request.user)
#         return form