from django.db import models
from .Ppe import Ppe
from .Worker import Worker
from django.utils import timezone

class PpeLoan(models.Model):
    idPpeLoan = models.AutoField(primary_key=True, editable=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='worker', null=True)
    workerPosition = models.CharField(max_length=100, null=True)
    workerDni = models.CharField(max_length=20, null=True)
    loanDate = models.DateField(default=timezone.now)
    newLoanDate = models.DateField(default=timezone.now)
    manager = models.CharField(max_length=20, default='')
    loanAmount = models.IntegerField(default=0)
    ppe = models.ForeignKey(Ppe, on_delete=models.CASCADE, null=True)
    confirmed = models.BooleanField(default=False)