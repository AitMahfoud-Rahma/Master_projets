from datetime import date

from django import forms

from .models import Medicament, Fournisseur, Client, Commande, Vente

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = '__all__'
        widgets = {
            'Prémption_medic': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }
    def clean_Prémption_medic(self):
        expiration_date = self.cleaned_data.get('Prémption_medic')

        if expiration_date and expiration_date <= date.today():
            raise forms.ValidationError("Expiration date must be greater than today.")

        return expiration_date
class FournisseurForm(forms.ModelForm):
    class Meta:
        model=Fournisseur
        fields = '__all__'
class ClientForm(forms.ModelForm):
    Type_assurance = forms.IntegerField()
    class Meta:
        model=Client
        fields = '__all__'
class CommandeForm(forms.ModelForm):
    class Meta:
        model= Commande
        fields = '__all__'
class VenteForm(forms.ModelForm):
    class Meta:
        model= Vente
        fields = '__all__'