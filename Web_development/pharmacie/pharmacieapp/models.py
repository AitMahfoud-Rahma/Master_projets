from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

class Medicament(models.Model):
    ID_medic = models.AutoField(primary_key=True)
    Nom_medic = models.CharField(max_length=100, null=False)
    Lot_medic = models.CharField(max_length=20, null=False)
    DCI = models.CharField(max_length=100, null=False)
    Dosage_medic = models.IntegerField()
    Prix_médic = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    Prix_achat = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    Forme_medic = models.CharField(max_length=20, choices=[('Sirop', 'Sirop'), ('Comprimé', 'Comprimé'), ('Suppo', 'Suppo')])
    Prémption_medic = models.DateField()
    Quantite_medic = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(Dosage_medic__gt=0), name='positive_dosage'),
            models.CheckConstraint(check=models.Q(Prix_médic__gt=models.F('Prix_achat')), name='selling_price_higher_than_purchase_price'),
        ]
    def __str__(self):
        return self.Nom_medic

class Fournisseur(models.Model):
    ID_fournisseur = models.AutoField(primary_key=True)
    Nom_fournisseur = models.CharField(max_length=100, null=False)
    Adresse_fournisseur = models.CharField(max_length=200, null=False)
    Tel_fournisseur = models.IntegerField(null=False)
    Mail_fournisseur = models.EmailField(null=False)
    def __str__(self):
        return self.Nom_fournisseur

class Client(models.Model):
    ID_client = models.AutoField(primary_key=True)
    Nom_client = models.CharField(max_length=100, null=False)
    Prenom_client = models.CharField(max_length=100, null=False)
    Age_Client = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    Num_sec_social_client = models.CharField(max_length=13, unique=True, validators=[RegexValidator(r'^\d{13}$', message='Num_sec_social_client must be 13 digits.')])
    def __str__(self):
        return self.Nom_client + " " + self.Prenom_client
class Commande(models.Model):
    Id_fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    ID_medic = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    Date_commande = models.DateField(null=False)
    Quantite_commande = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    def save(self, *args, **kwargs):
        medicament = self.ID_medic
        medicament.Quantite_medic += self.Quantite_commande
        medicament.save()
        super(Commande, self).save(*args, **kwargs)

class Vente(models.Model):
    ID_medic = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    ID_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Date_vente = models.DateField(null=False)
    Quantite_vendue = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    def save(self, *args, **kwargs):
        medicament = self.ID_medic
        medicament.Quantite_medic -= self.Quantite_vendue
        medicament.save()
        super(Vente, self).save(*args, **kwargs)


class Assurance(models.Model):
    ID_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Type_assurance = models.IntegerField(null=False, validators=[MinValueValidator(1)])
