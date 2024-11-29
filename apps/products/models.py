from django.db import models


class Hierarchy(models.Model):
    hierar_id = models.AutoField(primary_key=True, verbose_name='JerarquíaID', unique=True, blank=False, null=False)
    hierar_sup = models.ForeignKey('Hierarchy', verbose_name='Jerarquía Superior', on_delete=models.PROTECT, default=0, null=False)
    hierar_name = models.CharField(verbose_name='Nombre de Jerarquía', max_length=150, unique=True, blank=False, null=False)
    hierar_description = models.TextField(verbose_name='Descripción de Jerarquía', blank=False, null=False)
    hierar_icon = models.CharField(verbose_name='Icono de Jerarquía', max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'Hierarchy'
        ordering = ('hierar_id',)
        verbose_name = 'Hierarchy'
        verbose_name_plural = 'Hierarchies'
    
    def __str__(self):
        return f'({self.hierar_id}) {self.hierar_name}'
    
    def clean(self):
        if self.hierar_name:
            self.hierar_name = self.hierar_name.title().strip()
        if self.hierar_description:
            self.hierar_description = self.hierar_description.capitalize().strip()
        if self.hierar_icon:
            self.hierar_icon = self.hierar_icon.lower().strip()


class Value(models.Model):
    val_id = models.AutoField(primary_key=True, verbose_name='ValorID', unique=True, blank=False, null=False)
    hierar_id = models.ForeignKey('Hierarchy', verbose_name='JerarquíaID', on_delete=models.PROTECT, default=0, null=False)
    val_sup = models.ForeignKey('Value', verbose_name='Valor Superior', on_delete=models.PROTECT, default=0, null=False)
    val_name = models.CharField(verbose_name='Nombre de Valor', max_length=150, blank=False, null=False)
    val_description = models.TextField(verbose_name='Descripción de valor', blank=True, null=True)
    val_icon = models.CharField(verbose_name='Icono', max_length=100, blank=True, null=True)
    val_order = models.IntegerField(verbose_name='Orden', default=0, null=False)
    
    class Meta:
        db_table = 'Value'
        ordering = ('val_id', 'hierar_id')
        verbose_name = 'Value'
        verbose_name_plural = 'Values'
        constraints = [
            models.UniqueConstraint(fields=['val_sup', 'hierar_id', 'val_name'], name='unique_hierar_sup_name')
        ]
        
    def __str__(self):
        return self.val_name
    
    def clean(self):
        if self.val_name:
            self.val_name = self.val_name.capitalize().strip()
        if self.val_description:
            self.val_description = self.val_description.strip()
        if self.val_icon:
            self.val_icon = self.val_icon.lower().strip()