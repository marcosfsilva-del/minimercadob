# Banco De 120 requisitos

Este documento organiza 120 requisitos em 40 módulos independentes. Cada aluno pode assumir um módulo completo com 3 requisitos.

Regra pedagógica:

- cada módulo deve funcionar sozinho;
- cada aluno cria as 3 requisitos do seu módulo no GitHub;
- cada aluno trabalha em uma branch própria;
- cada aluno cria testes para as 3 entregas;
- cada aluno cria a própria CI da branch;
- não alterar `app/core/*` sem justificativa e aprovação.

Formato sugerido de branch:

```text
feature/<numero-requisito>-<slug>
```

Exemplo:

```text
feature/42-product-search
```

## Módulo 01 - Pesquisa De Produtos

### requisito 001 - Campo De Busca No Catálogo

Implementar busca por nome do produto no catálogo.

Critérios de aceitação:

- o usuário consegue digitar um termo de busca;
- produtos cujo nome contém o termo continuam visíveis;
- produtos que não correspondem ao termo ficam ocultos;
- busca vazia mostra todos os produtos.

### requisito 002 - Busca Por Descrição

Expandir a busca para considerar também a descrição do produto.

Critérios de aceitação:

- a busca encontra produtos pelo nome;
- a busca encontra produtos pela descrição;
- a busca não diferencia maiúsculas e minúsculas.

### requisito 003 - Testes Da Pesquisa

Criar testes da feature de pesquisa.

Critérios de aceitação:

- existe teste para busca por nome;
- existe teste para busca por descrição;
- existe teste para busca vazia;
- `python3 tasks.py test` passa.

## Módulo 02 - Categorias

### requisito 004 - Filtro Por Categoria

Implementar filtro de produtos por categoria.

Critérios de aceitação:

- o catálogo exibe uma lista de categorias;
- selecionar uma categoria filtra os produtos;
- existe opção para voltar a ver todas as categorias.

### requisito 005 - Contador Por Categoria

Exibir a quantidade de produtos em cada categoria.

Critérios de aceitação:

- cada categoria mostra um contador;
- o contador considera os produtos cadastrados;
- categorias sem produto não aparecem.

### requisito 006 - Testes De Categoria

Criar testes para filtro e contadores de categoria.

Critérios de aceitação:

- existe teste para filtro por categoria;
- existe teste para opção "todas";
- existe teste para contador;
- `python3 tasks.py test` passa.

## Módulo 03 - Ordenação

### requisito 007 - Ordenar Por Nome

Adicionar ordenação alfabetica no catálogo.

Critérios de aceitação:

- existe controle de ordenação por nome;
- produtos podem ser ordenados de A a Z;
- produtos podem ser ordenados de Z a A.

### requisito 008 - Ordenar Por Preço

Adicionar ordenação por preço.

Critérios de aceitação:

- produtos podem ser ordenados do menor preço para o maior;
- produtos podem ser ordenados do maior preço para o menor;
- a ordenação funciona junto com a listagem base.

### requisito 009 - Testes De Ordenação

Criar testes da ordenação.

Critérios de aceitação:

- existe teste para nome crescente;
- existe teste para nome decrescente;
- existe teste para preço crescente;
- existe teste para preço decrescente.

## Módulo 04 - Detalhes Do Produto

### requisito 010 - Página De Detalhes

Criar página de detalhes para cada produto.

Critérios de aceitação:

- cada produto possui link para detalhes;
- a página exibe nome, descrição, categoria, preço e estoque;
- produto inexistente retorna página de erro amigável.

### requisito 011 - Botão Adicionar Nos Detalhes

Permitir adicionar produto ao carrinho pela página de detalhes.

Critérios de aceitação:

- a página de detalhes possui botão de adicionar;
- o botão adiciona o produto correto;
- usuário volta ou segue para o carrinho sem erro.

### requisito 012 - Testes Dos Detalhes

Criar testes da página de detalhes.

Critérios de aceitação:

- teste cobre produto existente;
- teste cobre produto inexistente;
- teste cobre adicionar ao carrinho pelos detalhes.

## Módulo 05 - Produtos Promocionais

### requisito 013 - Filtro De Promocoes

Criar filtro para mostrar apenas produtos promocionais.

Critérios de aceitação:

- existe ação "ver promoções";
- apenas produtos promocionais aparecem;
- usuário consegue voltar ao catálogo completo.

### requisito 014 - Destaque Visual De Promoção

Melhorar o destaque visual de produtos promocionais.

Critérios de aceitação:

- produto promocional possui destaque claro;
- produto não promocional não recebe destaque;
- o destaque não quebra o layout mobile.

### requisito 015 - Testes De Promocoes

Criar testes para filtro e destaque promocional.

Critérios de aceitação:

- teste cobre filtro de promoção;
- teste cobre produto com flag promocional;
- teste cobre produto sem flag promocional.

## Módulo 06 - Estoque Baixo

### requisito 016 - Sinalizar Estoque Baixo

Exibir aviso quando o produto estiver com estoque baixo.

Critérios de aceitação:

- produtos com estoque igual ou menor que 5 exibem aviso;
- produtos acima do limite não exibem aviso;
- o limite fica documentado na feature.

### requisito 017 - Filtro De Estoque Baixo

Criar filtro para listar apenas produtos com estoque baixo.

Critérios de aceitação:

- existe ação para filtrar estoque baixo;
- somente produtos dentro do limite aparecem;
- busca sem resultado exibe mensagem amigável.

### requisito 018 - Testes De Estoque Baixo

Criar testes da feature de estoque baixo.

Critérios de aceitação:

- teste cobre produto abaixo do limite;
- teste cobre produto acima do limite;
- teste cobre filtro sem resultados.

## Módulo 07 - Produtos Esgotados

### requisito 019 - Sinalizar Produto Esgotado

Exibir estado de produto esgotado.

Critérios de aceitação:

- estoque zero mostra texto "esgotado";
- botão de adicionar fica desabilitado;
- produto continua visivel no catálogo.

### requisito 020 - Filtro De Esgotados

Criar filtro para produtos esgotados.

Critérios de aceitação:

- usuário consegue listar apenas esgotados;
- usuário consegue voltar ao catálogo completo;
- mensagem aparece quando não há esgotados.

### requisito 021 - Testes De Esgotados

Criar testes para produtos esgotados.

Critérios de aceitação:

- teste cobre exibição de esgotado;
- teste cobre botão desabilitado;
- teste cobre filtro de esgotados.

## Módulo 08 - Limite De Estoque No Carrinho

### requisito 022 - Bloquear Quantidade Acima Do Estoque

Impedir que o usuário coloque no carrinho quantidade maior que o estoque.

Critérios de aceitação:

- quantidade maxima respeita o estoque;
- tentativa acima do estoque mostra aviso;
- o carrinho mantem quantidade valida.

### requisito 023 - Mensagem De Estoque Disponivel

Exibir estoque disponível no item do carrinho.

Critérios de aceitação:

- cada item mostra o estoque atual;
- a mensagem atualiza após alterar quantidade;
- layout continua legível em telas pequenas.

### requisito 024 - Testes De Limite De Estoque

Criar testes para limite de estoque no carrinho.

Critérios de aceitação:

- teste cobre quantidade valida;
- teste cobre quantidade acima do estoque;
- teste cobre mensagem de estoque disponível.

## Módulo 09 - Limpar Carrinho

### requisito 025 - Botão Limpar Carrinho

Adicionar ação para remover todos os itens do carrinho.

Critérios de aceitação:

- botão aparece quando ha itens;
- clicar remove todos os itens;
- carrinho vazio mostra mensagem correta.

### requisito 026 - Confirmação Para Limpar Carrinho

Adicionar confirmação antes de limpar o carrinho.

Critérios de aceitação:

- usuário precisa confirmar a limpeza;
- cancelar mantem os itens;
- confirmar remove todos os itens.

### requisito 027 - Testes De Limpeza Do Carrinho

Criar testes para limpar carrinho.

Critérios de aceitação:

- teste cobre exibição do botão;
- teste cobre cancelamento;
- teste cobre limpeza confirmada.

## Módulo 10 - Subtotal No Carrinho

### requisito 028 - Exibir Subtotal Por Item

Mostrar subtotal de cada item no carrinho.

Critérios de aceitação:

- subtotal usa preço vezes quantidade;
- subtotal aparece em cada linha;
- valores usam formato monetario brasileiro.

### requisito 029 - Atualizar Subtotal Ao Alterar Quantidade

Recalcular subtotal quando a quantidade muda.

Critérios de aceitação:

- alterar quantidade altera subtotal;
- total geral permanece coerente;
- não há necessidade de recarregar dados externos.

### requisito 030 - Testes De Subtotal

Criar testes para subtotal por item.

Critérios de aceitação:

- teste cobre calculo inicial;
- teste cobre alteração de quantidade;
- teste cobre formato monetario.

## Módulo 11 - Contador Do Carrinho

### requisito 031 - Contador No Menu

Exibir quantidade total de itens no menu do carrinho.

Critérios de aceitação:

- contador aparece ao lado do link Carrinho;
- contador soma quantidades, não apenas produtos diferentes;
- contador desaparece ou zera quando carrinho está vazio.

### requisito 032 - Atualização Do Contador

Atualizar contador ao adicionar, remover ou alterar quantidade.

Critérios de aceitação:

- adicionar item aumenta contador;
- remover item reduz contador;
- alterar quantidade atualiza contador.

### requisito 033 - Testes Do Contador

Criar testes para contador do carrinho.

Critérios de aceitação:

- teste cobre carrinho vazio;
- teste cobre adicionar item;
- teste cobre remover item.

## Módulo 12 - Confirmação De Remoção

### requisito 034 - Confirmar Remoção De Item

Adicionar confirmação antes de remover item do carrinho.

Critérios de aceitação:

- clicar em remover pede confirmação;
- cancelar mantem o item;
- confirmar remove o item.

### requisito 035 - Mensagem Apos Remover Item

Exibir mensagem após remoção de item.

Critérios de aceitação:

- mensagem informa produto removido;
- mensagem aparece uma vez;
- carrinho reflete a remoção.

### requisito 036 - Testes De Remoção

Criar testes para confirmação de remoção.

Critérios de aceitação:

- teste cobre cancelamento;
- teste cobre confirmação;
- teste cobre mensagem de sucesso.

## Módulo 13 - Cupom Simples

### requisito 037 - Campo De Cupom

Criar campo para informar cupom no carrinho.

Critérios de aceitação:

- campo aparece no resumo do carrinho;
- usuário consegue enviar um código;
- cupom desconhecido mostra mensagem amigável.

### requisito 038 - Cupom DEVOPS10

Implementar cupom `DEVOPS10` com 10% de desconto.

Critérios de aceitação:

- cupom valido aplica 10% de desconto;
- total final exibe desconto;
- cupom invalido não altera total.

### requisito 039 - Testes De Cupom

Criar testes para cupom simples.

Critérios de aceitação:

- teste cobre cupom valido;
- teste cobre cupom invalido;
- teste cobre total com desconto.

## Módulo 14 - Desconto Por Categoria

### requisito 040 - Regra De Desconto Por Categoria

Criar regra de desconto para uma categoria específica.

Critérios de aceitação:

- uma categoria definida recebe desconto;
- outras categorias não recebem desconto;
- regra fica documentada na feature.

### requisito 041 - Exibir Desconto Por Categoria

Mostrar desconto aplicado no resumo do carrinho.

Critérios de aceitação:

- resumo exibe valor do desconto;
- resumo exibe total final;
- layout continua claro com ou sem desconto.

### requisito 042 - Testes De Desconto Por Categoria

Criar testes da regra de desconto por categoria.

Critérios de aceitação:

- teste cobre categoria com desconto;
- teste cobre categoria sem desconto;
- teste cobre total final.

## Módulo 15 - Frete Gratis

### requisito 043 - Regra De Frete Gratis

Criar regra de frete grátis para compras acima de um valor mínimo.

Critérios de aceitação:

- valor mínimo fica documentado;
- compras acima do valor exibem frete grátis;
- compras abaixo exibem mensagem de quanto falta.

### requisito 044 - Indicador De Progresso Para Frete

Exibir progresso até atingir frete grátis.

Critérios de aceitação:

- indicador aparece no carrinho;
- indicador chega a 100% quando atingir o mínimo;
- indicador não quebra layout mobile.

### requisito 045 - Testes De Frete Gratis

Criar testes da feature de frete grátis.

Critérios de aceitação:

- teste cobre compra abaixo do mínimo;
- teste cobre compra acima do mínimo;
- teste cobre mensagem de valor restante.

## Módulo 16 - Leve 3 Pague 2

### requisito 046 - Regra Leve 3 Pague 2

Implementar promoção "leve 3 pague 2" para uma categoria ou produto.

Critérios de aceitação:

- regra aplica desconto a cada grupo de 3;
- quantidade menor que 3 não recebe desconto;
- produto/categoria da regra fica documentado.

### requisito 047 - Exibir Economia Da Promoção

Mostrar economia gerada pela promoção.

Critérios de aceitação:

- carrinho mostra valor economizado;
- total final considera economia;
- mensagem aparece apenas quando regra se aplica.

### requisito 048 - Testes Leve 3 Pague 2

Criar testes da promoção.

Critérios de aceitação:

- teste cobre 2 itens sem desconto;
- teste cobre 3 itens com desconto;
- teste cobre 6 itens com dois descontos.

## Módulo 17 - Compra Mínima

### requisito 049 - Bloquear Checkout Abaixo Do Minimo

Definir valor mínimo para finalizar compra.

Critérios de aceitação:

- checkout fica bloqueado abaixo do mínimo;
- usuário vê quanto falta para atingir o mínimo;
- compras acima do mínimo podem finalizar.

### requisito 050 - Mensagem De Compra Mínima

Exibir mensagem clara no carrinho e checkout.

Critérios de aceitação:

- carrinho mostra regra de compra mínima;
- checkout mostra bloqueio quando necessario;
- mensagem desaparece quando total e suficiente.

### requisito 051 - Testes De Compra Mínima

Criar testes da regra de compra mínima.

Critérios de aceitação:

- teste cobre total abaixo do mínimo;
- teste cobre total igual ao mínimo;
- teste cobre total acima do mínimo.

## Módulo 18 - Nome Do Cliente

### requisito 052 - Nome Obrigatorio No Checkout

Tornar nome do cliente obrigatorio no checkout.

Critérios de aceitação:

- checkout exige nome;
- nome vazio mostra erro;
- pedido salvo contém nome informado.

### requisito 053 - Validação De Tamanho Do Nome

Validar tamanho mínimo e máximo do nome.

Critérios de aceitação:

- nome curto demais mostra erro;
- nome longo demais mostra erro;
- nome valido permite finalizar.

### requisito 054 - Testes De Nome Do Cliente

Criar testes para validação de nome.

Critérios de aceitação:

- teste cobre nome vazio;
- teste cobre nome invalido;
- teste cobre nome valido.

## Módulo 19 - CPF Do Cliente

### requisito 055 - Campo CPF No Checkout

Adicionar campo de CPF no checkout.

Critérios de aceitação:

- checkout exibe campo CPF;
- CPF é salvo junto ao pedido ou cliente;
- campo aceita CPF com ou sem pontuação.

### requisito 056 - Validação Simples De CPF

Criar validação simples de formato do CPF.

Critérios de aceitação:

- CPF com 11 digitos é aceito;
- CPF com tamanho invalido é rejeitado;
- mensagem de erro é clara.

### requisito 057 - Testes De CPF

Criar testes para campo e validação de CPF.

Critérios de aceitação:

- teste cobre CPF valido;
- teste cobre CPF invalido;
- teste cobre persistencia do CPF.

## Módulo 20 - Forma De Pagamento

### requisito 058 - Selecionar Forma De Pagamento

Adicionar selecao de forma de pagamento no checkout.

Critérios de aceitação:

- opcoes incluem dinheiro, pix e cartao;
- usuário precisa selecionar uma opção;
- pedido registra a forma escolhida.

### requisito 059 - Resumo Da Forma De Pagamento

Exibir forma de pagamento no resumo do pedido.

Critérios de aceitação:

- pedidos mostram a forma selecionada;
- API retorna forma de pagamento;
- valor aparece de forma legível.

### requisito 060 - Testes De Pagamento

Criar testes para forma de pagamento.

Critérios de aceitação:

- teste cobre opção obrigatoria;
- teste cobre pedido com pix;
- teste cobre exibição no histórico.

## Módulo 21 - Forma De Entrega

### requisito 061 - Selecionar Forma De Entrega

Adicionar retirada ou entrega no checkout.

Critérios de aceitação:

- usuário éscolhe retirada ou entrega;
- pedido registra a escolha;
- retirada não exige endereço.

### requisito 062 - Endereco Para Entrega

Exigir endereço quando forma for entrega.

Critérios de aceitação:

- entrega exige endereço;
- retirada não exige endereço;
- pedido de entrega salva endereço.

### requisito 063 - Testes De Entrega

Criar testes para forma de entrega.

Critérios de aceitação:

- teste cobre retirada;
- teste cobre entrega sem endereço;
- teste cobre entrega com endereço.

## Módulo 22 - Código Do Pedido

### requisito 064 - Gerar Código Publico Do Pedido

Gerar código público para cada pedido.

Critérios de aceitação:

- cada pedido possui código legível;
- código é diferente do id interno ou formatado;
- código aparece após finalizar compra.

### requisito 065 - Buscar Pedido Por Código

Criar busca de pedido pelo código público.

Critérios de aceitação:

- usuário informa código;
- pedido encontrado e exibido;
- código inexistente mostra mensagem amigável.

### requisito 066 - Testes De Código Do Pedido

Criar testes para código de pedido.

Critérios de aceitação:

- teste cobre geração do código;
- teste cobre busca existente;
- teste cobre busca inexistente.

## Módulo 23 - Tela De Sucesso

### requisito 067 - Criar Tela De Sucesso

Criar tela específica após finalizar compra.

Critérios de aceitação:

- usuário é redirecionado após compra;
- tela mostra número ou código do pedido;
- tela mostra total da compra.

### requisito 068 - Ações Na Tela De Sucesso

Adicionar acoes para voltar ao catálogo e ver pedidos.

Critérios de aceitação:

- existe ação para voltar ao catálogo;
- existe ação para ver histórico de pedidos;
- acoes funcionam corretamente.

### requisito 069 - Testes Da Tela De Sucesso

Criar testes para tela de sucesso.

Critérios de aceitação:

- teste cobre redirecionamento;
- teste cobre exibição do pedido;
- teste cobre links de ação.

## Módulo 24 - Histórico De Pedidos

### requisito 070 - Filtro No Histórico

Adicionar filtro por nome do cliente no histórico de pedidos.

Critérios de aceitação:

- usuário filtra por nome;
- filtro não diferencia maiúsculas e minúsculas;
- sem termo mostra todos os pedidos.

### requisito 071 - Ordenação Do Histórico

Adicionar ordenação por data e total.

Critérios de aceitação:

- usuário ordena por data;
- usuário ordena por total;
- ordenação funciona com filtro aplicado.

### requisito 072 - Testes Do Histórico

Criar testes para histórico de pedidos.

Critérios de aceitação:

- teste cobre filtro por cliente;
- teste cobre ordenação por data;
- teste cobre ordenação por total.

## Módulo 25 - Repetir Compra

### requisito 073 - Botão Repetir Compra

Adicionar botão para repetir um pedido anterior.

Critérios de aceitação:

- pedido no histórico possui ação repetir;
- itens do pedido sao adicionados ao carrinho;
- quantidades sao preservadas quando ha estoque.

### requisito 074 - Tratar Falta De Estoque Ao Repetir

Tratar produtos sem estoque suficiente ao repetir compra.

Critérios de aceitação:

- item sem estoque não quebra a repeticao;
- usuário recebe aviso;
- itens disponiveis continuam no carrinho.

### requisito 075 - Testes De Repetir Compra

Criar testes para repetir compra.

Critérios de aceitação:

- teste cobre repeticao com estoque;
- teste cobre repeticao sem estoque;
- teste cobre carrinho resultante.

## Módulo 26 - Baixa Automática De Estoque

### requisito 076 - Confirmar Baixa No Checkout

Garantir baixa de estoque ao finalizar compra.

Critérios de aceitação:

- estoque diminui conforme quantidade comprada;
- pedido registra itens comprados;
- estoque não muda se checkout falhar.

### requisito 077 - Exibir Estoque Atual Apos Compra

Atualizar catálogo com estoque reduzido após compra.

Critérios de aceitação:

- catálogo mostra estoque novo;
- produto pode ficar esgotado;
- usuário não ve estoque antigo após finalizar.

### requisito 078 - Testes De Baixa De Estoque

Criar testes para baixa automática.

Critérios de aceitação:

- teste cobre baixa bem sucedida;
- teste cobre falha sem baixa;
- teste cobre catálogo após compra.

## Módulo 27 - Bloqueio De Estoque Negativo

### requisito 079 - Bloquear Estoque Negativo

Impedir que qualquer fluxo gere estoque negativo.

Critérios de aceitação:

- compra acima do estoque e rejeitada;
- estoque nunca fica menor que zero;
- mensagem informa o problema.

### requisito 080 - Validação Na API

Adicionar validação de estoque na criação de pedido via API.

Critérios de aceitação:

- API rejeita quantidade acima do estoque;
- API retorna status adequado;
- resposta contém mensagem clara.

### requisito 081 - Testes De Estoque Negativo

Criar testes contra estoque negativo.

Critérios de aceitação:

- teste cobre checkout web;
- teste cobre endpoint API;
- teste cobre estoque preservado.

## Módulo 28 - Reposição De Estoque

### requisito 082 - Tela De Reposição

Criar tela simples para repor estoque de produto.

Critérios de aceitação:

- usuário seleciona produto;
- usuário informa quantidade;
- estoque aumenta após confirmar.

### requisito 083 - Registrar Movimento De Reposição

Registrar movimentação de estoque para reposicoes.

Critérios de aceitação:

- reposição cria movimento do tipo reposição;
- movimento registra produto e quantidade;
- dados aparecem em consulta interna ou página da feature.

### requisito 084 - Testes De Reposição

Criar testes para reposição de estoque.

Critérios de aceitação:

- teste cobre aumento de estoque;
- teste cobre quantidade invalida;
- teste cobre movimento registrado.

## Módulo 29 - Movimentações De Estoque

### requisito 085 - Listar Movimentações

Criar página para listar movimentações de estoque.

Critérios de aceitação:

- página lista produto, tipo, quantidade e data;
- movimentações aparecem em ordem recente;
- página lida com lista vazia.

### requisito 086 - Filtrar Movimentações Por Produto

Adicionar filtro por produto na lista de movimentações.

Critérios de aceitação:

- usuário seleciona ou busca produto;
- lista exibe apenas movimentos do produto;
- filtro vazio mostra todos.

### requisito 087 - Testes De Movimentações

Criar testes para movimentações.

Critérios de aceitação:

- teste cobre lista;
- teste cobre filtro;
- teste cobre estado vazio.

## Módulo 30 - Favoritos

### requisito 088 - Marcar Produto Como Favorito

Permitir marcar produto como favorito.

Critérios de aceitação:

- produto possui ação favoritar;
- favorito fica salvo na sessao ou tabela da feature;
- usuário visualiza estado favoritado.

### requisito 089 - Filtro De Favoritos

Criar tela ou filtro para produtos favoritos.

Critérios de aceitação:

- usuário consegue ver favoritos;
- usuário consegue remover favorito;
- lista vazia mostra mensagem amigável.

### requisito 090 - Testes De Favoritos

Criar testes para favoritos.

Critérios de aceitação:

- teste cobre favoritar;
- teste cobre desfavoritar;
- teste cobre lista de favoritos.

## Módulo 31 - Vistos Recentemente

### requisito 091 - Registrar Produto Visto

Registrar produtos acessados recentemente.

Critérios de aceitação:

- acessar detalhes registra produto;
- lista preserva ordem do mais recente;
- produtos repetidos não duplicam.

### requisito 092 - Exibir Vistos Recentemente

Exibir lista de vistos recentemente.

Critérios de aceitação:

- lista aparece no catálogo ou página própria;
- lista possui limité documentado;
- item da lista leva ao produto.

### requisito 093 - Testes De Vistos Recentemente

Criar testes para vistos recentemente.

Critérios de aceitação:

- teste cobre registro;
- teste cobre ordem;
- teste cobre remoção de duplicados.

## Módulo 32 - Total Gasto Por Cliente

### requisito 094 - Calcular Total Gasto

Calcular total gasto por cliente com base nos pedidos.

Critérios de aceitação:

- cliente com pedidos mostra soma correta;
- cliente sem pedidos mostra zero;
- calculo considera total dos pedidos.

### requisito 095 - Exibir Ranking De Clientes

Criar página de ranking por total gasto.

Critérios de aceitação:

- ranking mostra cliente e total;
- ranking ordena do maior para o menor;
- lista vazia mostra mensagem amigável.

### requisito 096 - Testes De Total Gasto

Criar testes para total gasto por cliente.

Critérios de aceitação:

- teste cobre cliente com um pedido;
- teste cobre cliente com varios pedidos;
- teste cobre ranking.

## Módulo 33 - Ultima Compra Do Cliente

### requisito 097 - Identificar Ultima Compra

Identificar a ultima compra de cada cliente.

Critérios de aceitação:

- cliente com pedidos mostra data da ultima compra;
- cliente sem pedidos mostra estado vazio;
- regra usa pedido mais recente.

### requisito 098 - Exibir Ultima Compra No Histórico

Exibir ultima compra em uma página ou bloco da feature.

Critérios de aceitação:

- mostra nome do cliente;
- mostra data e total da ultima compra;
- permite acessar o pedido relacionado.

### requisito 099 - Testes De Ultima Compra

Criar testes para ultima compra.

Critérios de aceitação:

- teste cobre cliente sem pedidos;
- teste cobre cliente com pedidos;
- teste cobre pedido mais recente.

## Módulo 34 - Health Check Avancado

### requisito 100 - Endpoint De Health Detalhado

Criar endpoint de health detalhado da feature.

Critérios de aceitação:

- endpoint retorna status da aplicação;
- endpoint retorna versão;
- endpoint retorna horario da resposta.

### requisito 101 - Health Do Banco

Adicionar verificação simples de banco no health detalhado.

Critérios de aceitação:

- endpoint verifica conexao com SQLite;
- resposta indica banco ok ou falha;
- falha retorna status adequado.

### requisito 102 - Testes De Health Avancado

Criar testes do health detalhado.

Critérios de aceitação:

- teste cobre status ok;
- teste cobre informacoes de versão;
- teste cobre verificação de banco.

## Módulo 35 - Readiness

### requisito 103 - Endpoint Readiness

Criar endpoint de readiness especifico.

Critérios de aceitação:

- endpoint retorna ready quando aplicação pode receber tráfego;
- endpoint usa formato JSON;
- endpoint fica documentado no README da feature.

### requisito 104 - Readiness Com Banco

Readiness deve considerar acesso ao banco.

Critérios de aceitação:

- banco acessivel retorna ready;
- banco indisponível retorna not ready;
- status HTTP reflete o estado.

### requisito 105 - Testes De Readiness

Criar testes para readiness.

Critérios de aceitação:

- teste cobre readiness ok;
- teste cobre resposta JSON;
- teste cobre verificação de banco.

## Módulo 36 - Versionamento Da Aplicação

### requisito 106 - Endpoint De Versão

Criar endpoint para retornar versão da aplicação.

Critérios de aceitação:

- endpoint retorna `APP_VERSION`;
- endpoint retorna `COMMIT_SHA`;
- endpoint usa JSON.

### requisito 107 - Exibir Versão No Rodape

Exibir versão da aplicação no frontend.

Critérios de aceitação:

- rodape mostra versão;
- commit aparece quando configurado;
- ausencia de variavel usa valor local.

### requisito 108 - Testes De Versão

Criar testes para versionamento.

Critérios de aceitação:

- teste cobre endpoint;
- teste cobre valor padrão;
- teste cobre exibição no frontend.

## Módulo 37 - Request ID

### requisito 109 - Gerar Request ID

Gerar identificador único para cada requisição.

Critérios de aceitação:

- cada request recebe id;
- id aparece no header de resposta;
- id pode ser reutilizado se cliente enviar header.

### requisito 110 - Exibir Request ID Em Erros

Incluir request id em respostas de erro.

Critérios de aceitação:

- erro web mostra código de rastreio;
- erro API retorna request id no JSON;
- logs incluem request id.

### requisito 111 - Testes De Request ID

Criar testes para request id.

Critérios de aceitação:

- teste cobre geração automática;
- teste cobre header enviado pelo cliente;
- teste cobre resposta de erro.

## Módulo 38 - Métricas Simples

### requisito 112 - Contador De Requisicoes

Criar métrica simples de quantidade de requisições.

Critérios de aceitação:

- contador aumenta a cada requisição;
- endpoint de métricas retorna contador;
- formato é documentado.

### requisito 113 - Métricas Por Rota

Adicionar contagem por rota.

Critérios de aceitação:

- métricas mostram rota;
- métricas mostram quantidade por rota;
- rotas desconhecidas não quebram métricas.

### requisito 114 - Testes De Métricas

Criar testes para métricas.

Critérios de aceitação:

- teste cobre contador geral;
- teste cobre contador por rota;
- teste cobre endpoint de métricas.

## Módulo 39 - Logs De Auditoria

### requisito 115 - Registrar Evento De Pedido

Criar log de auditoria ao finalizar pedido.

Critérios de aceitação:

- pedido criado gera evento;
- evento contém tipo, data e id do pedido;
- evento pode ser consultado.

### requisito 116 - Registrar Evento De Carrinho

Criar log de auditoria para acoes importantes do carrinho.

Critérios de aceitação:

- adicionar produto gera evento;
- remover produto gera evento;
- limpar carrinho gera evento quando existir.

### requisito 117 - Testes De Auditoria

Criar testes para logs de auditoria.

Critérios de aceitação:

- teste cobre evento de pedido;
- teste cobre evento de carrinho;
- teste cobre consulta de eventos.

## Módulo 40 - Acessibilidade E UX Básica

### requisito 118 - Melhorar Labels De Formulários

Revisar formulários para garantir labels claros.

Critérios de aceitação:

- inputs possuem label associado;
- botoes possuem texto claro;
- mensagens de erro ficam proximas ao campo.

### requisito 119 - Estados Vazios Amigaveis

Melhorar estados vazios do catálogo, carrinho e pedidos.

Critérios de aceitação:

- carrinho vazio tem mensagem e ação;
- pedidos vazios tem mensagem clara;
- filtros sem resultado orientam o usuário.

### requisito 120 - Testes De UX Básica

Criar testes para labels e estados vazios.

Critérios de aceitação:

- teste cobre label de formulário;
- teste cobre carrinho vazio;
- teste cobre lista vazia de pedidos.
