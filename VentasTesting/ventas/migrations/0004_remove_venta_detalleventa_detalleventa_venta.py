# Generated by Django 4.2.7 on 2024-11-18 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_venta_eliminado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='detalleVenta',
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='detalleVenta', to='ventas.venta'),
            preserve_default=False,
        ),
    ]