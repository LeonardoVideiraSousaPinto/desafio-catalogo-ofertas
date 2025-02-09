from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Produto

def listar_produtos(request):
    produtos = Produto.objects.all()

    # Filtro por frete grátis
    if 'frete_gratis' in request.GET:
        produtos = produtos.filter(frete_gratis=True)

    # Filtro por entrega pelo Full
    if 'full' in request.GET:
        produtos = produtos.filter(full=True)

    # Filtro por vendedor oficial
    if 'loja_oficial' in request.GET:
        produtos = produtos.filter(loja_oficial=True)

    # Filtro por texto
    if 'pesquisa' in request.GET:
        termo = request.GET['pesquisa']
        produtos = produtos.filter(nome__icontains=termo)



    # Ordenação por preço
    if 'order_by' in request.GET:
        if request.GET['order_by'] == 'preco_asc':
            produtos = produtos.order_by('valor_com_desc')
        elif request.GET['order_by'] == 'preco_desc':
            produtos = produtos.order_by('-valor_com_desc')
        elif request.GET['order_by'] == 'pcto_asc':
            produtos = produtos.order_by('pcto_desc')            
        elif request.GET['order_by'] == 'pcto_desc':
            produtos = produtos.order_by('-pcto_desc')



    # Paginação
    
    paginator = Paginator(produtos, 48) 
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'listar_produtos/produtos.html', {'page_obj': page_obj})
