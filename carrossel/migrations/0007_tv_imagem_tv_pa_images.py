# Generated by Django 4.2.4 on 2023-12-21 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrossel', '0006_remove_tv_pa_images_delete_tv_imagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tv_Imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_da_imagem', models.CharField(default='Imagem', max_length=100)),
                ('imagem', models.ImageField(upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('adicionado_em', models.DateField(auto_now_add=True)),
                ('pa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carrossel.tv_pa')),
            ],
        ),
        migrations.AddField(
            model_name='tv_pa',
            name='images',
            field=models.ManyToManyField(to='carrossel.tv_imagem'),
        ),
    ]
