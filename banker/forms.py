from django import forms

from banker.models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'
