from django import forms


class searchForm(forms.Form):
    search_field = forms.CharField(max_length=100, required=False)
