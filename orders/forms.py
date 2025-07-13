from django import forms
from orders.models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        offer = cleaned_data.get("offer")

        if not product and not offer:
            self.add_error("product", "You must select a product or an offer.")
            self.add_error("offer", "You must select a product or an offer.")

        if product and offer:
            self.add_error("product", "Select only one: product or offer.")
            self.add_error("offer", "Select only one: product or offer.")

        return cleaned_data
