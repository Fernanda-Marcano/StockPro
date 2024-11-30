from django.db import models
from django.db.models import Q
from django.db import transaction


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


class Product(models.Model):
    
    GBL_ID_HIERAR_PRODUCT = 10
    GBL_ID_HIERAR_CATEGORY = 11
    GBL_ID_HIERAR_BRAND= 12
    
    pdt_id = models.AutoField(primary_key=True, verbose_name='ProductoID', unique=True, blank=False, null=False)
    id_product = models.ForeignKey('Value', related_name='PDT_id_product', limit_choices_to=Q(hierar_id=GBL_ID_HIERAR_PRODUCT) | Q(hierar_id=0), on_delete=models.PROTECT, default=0, null=False)
    id_category = models.ForeignKey('Value', related_name='PDT_id_category', limit_choices_to=Q(hierar_id=GBL_ID_HIERAR_CATEGORY) | Q(hierar_id=0), on_delete=models.PROTECT, default=0, null=False)
    id_brand = models.ForeignKey('Value', related_name='PDT_id_brand', limit_choices_to=Q(hierar_id=GBL_ID_HIERAR_BRAND) | Q(hierar_id=0), on_delete=models.PROTECT, default=0, null=False)
    pdt_model = models.CharField(verbose_name='Modelo del Producto', max_length=200, blank=False, null=False)
    pdt_name = models.CharField(verbose_name='Nombre del Producto', max_length=200, blank=False, null=False)
    pdt_serial = models.CharField(verbose_name='Serial del Producto', max_length=15, unique=True, blank=False, null=False)
    pdt_stock = models.PositiveIntegerField(verbose_name='Cantidad del Producto', blank=False, null=False)
    pdt_price = models.DecimalField(verbose_name='Precio del Producto', max_digits=10, decimal_places=2, blank=False, null=False)
    pdt_description = models.TextField(verbose_name='Descripcion del Producto', blank=True, null=True)
    pdt_image = models.ImageField(verbose_name='Imagen del Producto', upload_to='product/img/', default='product/img/img.png')
    
    pdt_map = {
        'id_product':GBL_ID_HIERAR_PRODUCT,
        'id_category':GBL_ID_HIERAR_CATEGORY, 
        'id_brand':GBL_ID_HIERAR_BRAND
    }
    
    class Meta:
        db_table = 'Product'
        ordering = ('pdt_id',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.pdt_name
    
    def clean(self):
        if self.pdt_name:
            self.pdt_name = self.pdt_name.capitalize().strip()
        if self.pdt_model:
            self.pdt_model = self.pdt_model.upper().strip()
        if self.pdt_serial:
            self.pdt_serial = self.pdt_serial.upper().strip()
        if self.pdt_description:
            self.pdt_description = self.pdt_description.capitalize().strip()


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True, verbose_name='VentaID', unique=True, blank=False, null=False)
    product_id = models.ForeignKey('Product', verbose_name='ProductoID', related_name='sale_product', on_delete=models.PROTECT, db_column='product_id',  null=False)
    sale_quantity = models.PositiveIntegerField(verbose_name='Cantidad a Vender', blank=False, null=False)
    sale_date = models.DateField(verbose_name='Fecha', auto_now_add=True)
    
    class Meta:
        db_table = 'Sale'
        ordering = ('sale_id',)
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            product = self.product_id
            if product.pdt_stock >= self.sale_quantity:
                product.pdt_stock -= self.sale_quantity
                product.save()
                super().save(*args, **kwargs)
            else:
                raise ValueError('Stock Insuficiente')
