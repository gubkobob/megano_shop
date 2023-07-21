from django import forms


class CartAddProductInShopForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9999)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CouponApplyForm(forms.Form):
    code = forms.CharField()
