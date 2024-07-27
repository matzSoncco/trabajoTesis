from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Material(models.Model):
    idMaterial = models.CharField(verbose_name=_('ID'), primary_key=True, editable=False, max_length=10)
    name = models.CharField(verbose_name=_('Nombre'), null=False, max_length=20)
    quantity = models.IntegerField(verbose_name=_('Cantidad'), validators=[MinValueValidator(0)], null=False, default=0)
    stock = models.IntegerField(null=False, default=0)
    guideNumber = models.IntegerField(verbose_name=_('Número de Guía'), null=False, default=0)
    unit = models.CharField(verbose_name=_('Unidad'), null=False, max_length=20, default='')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    creationDate = models.DateField(auto_now_add=False, blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.idMaterial or not self.idMaterial.startswith('M-'):
            # Obtiene el número autoincrementable
            last_id = Material.objects.all().order_by('-idMaterial').first()
            if last_id:
                # Intenta obtener el número del último idMaterial
                try:
                    last_id_number = int(last_id.idMaterial.split('-')[1]) + 1
                except IndexError:
                    # Si hay un IndexError, asigna 1 como el siguiente número
                    last_id_number = 1
            else:
                last_id_number = 1
            
            self.idMaterial = f'M-{last_id_number:04}'  # '04' asegura que siempre tenga 4 dígitos
        
        super(Material, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s %s" %(self.idMaterial, self.name, self.quantity, self.stock)