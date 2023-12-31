# Generated by Django 4.2.4 on 2023-12-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrossel', '0002_tv_imagem_delete_tv_imagens'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tv_PA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_do_PA', models.CharField(max_length=100)),
                ('imagem_00', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_01', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_02', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_03', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_04', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_05', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_06', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_07', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_08', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_09', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_10', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_11', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_12', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_13', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_14', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_15', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_16', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_17', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_18', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_19', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
                ('imagem_20', models.ImageField(blank=True, upload_to='Tv_imagens/carrossel/%Y/%m/')),
            ],
        ),
        migrations.DeleteModel(
            name='Tv_Imagem',
        ),
    ]
