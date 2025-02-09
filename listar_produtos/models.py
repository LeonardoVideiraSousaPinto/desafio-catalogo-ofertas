from django.db import models

class Produto(models.Model):
    link = models.URLField(primary_key=True)
    link_imagem = models.URLField()
    nome = models.CharField(max_length=255)
    valor = models.IntegerField()
    valor_com_desc = models.IntegerField()
    pcto_desc = models.FloatField()
    opcao_parc = models.CharField(max_length=255, blank=True, null=True)
    full = models.BooleanField()
    frete_gratis = models.BooleanField()
    loja_oficial = models.BooleanField()

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'produtos'  # Nome da tabela no banco de dados
