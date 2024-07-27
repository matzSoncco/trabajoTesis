from django.db import models
from .Ppe import Ppe
from .Worker import Worker
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class PpeLoan(models.Model):
    idPpeLoan = models.AutoField(primary_key=True, editable=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
    loanDate = models.DateField(verbose_name=_('Fecha de Entrega'), default=timezone.now)
    newLoanDate = models.DateField(verbose_name=_('Fecha de Nueva Entrega'), default=timezone.now)
    manager = models.CharField(verbose_name=_('Nombre del Responsable'), null=False, max_length=20, default='')
    description = models.TextField(verbose_name=_('Descripción'), null=False, default='Es su primera entrega.', editable=True)

class PpeLoanDetail(models.Model):
    ppeLoan = models.ForeignKey(PpeLoan, related_name='details', on_delete=models.CASCADE)
    ppe = models.ForeignKey(Ppe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('Cantidad'))