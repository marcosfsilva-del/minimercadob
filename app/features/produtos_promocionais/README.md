# Produtos promocionais

Implementa o **Requisito 013**, da [Issue #15](https://github.com/marcosfsilva-del/minimercadob/issues/15): permitir visualizar apenas produtos promocionais e retornar ao catálogo completo.

Branch da entrega: `feature/15-filtros-produtos-promocionais`.

## Comportamento

- No catálogo `/`, a ação **Ver promoções** abre `/produtos-promocionais`.
- O backend seleciona produtos com `promotional=True`, ordenados por nome.
- A visualização filtrada mostra **Exibindo apenas produtos promocionais** e a ação **Ver todos os produtos**, que retorna para `/`.
- Sem promoções, aparece **Nenhum produto em promoção no momento.**, mantendo o retorno disponível.
- Produtos promocionais com estoque zero continuam visíveis, com o botão de compra desabilitado pelo template existente.

O filtro apenas consulta os dados: não altera preços, estoque ou o status de promoção. Não calcula descontos nem cria uma API JSON adicional.

## Integração com o projeto

A implementação fica neste pacote, sem alterações em `app/core/`.

| Arquivo | Responsabilidade |
| --- | --- |
| `manifest.py` | Registra o Blueprint e a contribuição ao slot `PRODUCT_LIST_TOOLBAR` |
| `routes.py` | Atende `GET /produtos-promocionais` e renderiza o `catalog.html` existente |
| `service.py` | Consulta os produtos cujo campo `promotional` é verdadeiro |
| `templates/produtos_promocionais/toolbar.html` | Mostra os links, o filtro ativo e a mensagem de ausência de promoções |
| `tests/test_produtos_promocionais.py` | Verifica filtragem, retorno, ausência de promoções e estoque zero |

O registry do core descobre o `manifest.py` ao iniciar a aplicação. O slot adiciona os controles à barra do catálogo. O renderer usa o endpoint da requisição para identificar se a visualização promocional está ativa. A rota consulta o banco e reutiliza o template do catálogo, preservando os cartões e botões de compra.

## Execução local

Execute os comandos a partir da raiz do repositório. Exemplo para Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Para preparar os produtos de demonstração:

```bash
python tasks.py db-seed
```

**Atenção:** o seed redefine os preços e estoques dos produtos iniciais. Pule essa etapa se já houver dados que deseja preservar. As contagens abaixo consideram um banco contendo apenas os produtos do seed.

Inicie a aplicação:

```bash
python tasks.py dev
```

Abra `http://localhost:3000`. Para encerrar o servidor, pressione `Ctrl+C`.

## Roteiro de demonstração

1. Abra `/`: devem aparecer os 10 produtos do seed e a ação **Ver promoções**.
2. Acione **Ver promoções** e confira a URL `/produtos-promocionais`.
3. Confira os quatro produtos: **Arroz, Café, Sabonete e Refrigerante**. Produtos comuns, como Feijão, não devem aparecer.
4. Confira o texto **Exibindo apenas produtos promocionais**.
5. Acione **Ver todos os produtos**: a URL volta para `/` e os 10 produtos reaparecem.
6. Execute os testes abaixo para verificar também os cenários sem promoções e com estoque zero, sem editar manualmente o banco da aplicação.

## Critérios de aceitação e testes

| Critério ou cenário | Teste que o verifica |
| --- | --- |
| Ação “Ver promoções”, inclusão dos promocionais e exclusão dos demais | `test_promotional_catalog_filters_products` |
| Ação de retorno funcional e restauração do catálogo completo | `test_return_link_restores_full_catalog` |
| Mensagem e retorno quando não há promoções | `test_catalog_without_promotions_shows_message_and_return_link` |
| Produto promocional sem estoque permanece visível, com compra desabilitada | `test_out_of_stock_promotional_product_remains_visible` |

Cada teste da feature cria um banco SQLite em memória com dados controlados. A fixture substitui temporariamente o engine e a fábrica de sessões; ao terminar, restaura as referências e descarta o engine. Os testes da feature não dependem do seed nem modificam o banco da aplicação.

Para executar somente os quatro testes da feature:

```bash
python -m pytest app/features/produtos_promocionais/tests/ -v
```

Para verificar a estrutura, lint, suíte completa e compilação:

```bash
python tasks.py feature-check produtos-promocionais
python tasks.py lint
python tasks.py test
python tasks.py build
```

Os testes antigos da suíte completa usam a configuração de banco da aplicação. Para isolar também esses testes, pode-se executar, no lugar de `python tasks.py test`:

```bash
DATABASE_URL="sqlite:///$(mktemp -d)/tests.db" python tasks.py test
```

Na entrega desta feature, a suíte contém **8 testes**, dos quais **4** são deste pacote. O build usa `compileall` para verificar a compilação do código Python; não substitui os testes nem garante que todos os imports funcionem em execução.

Com o servidor ativo, execute em outro terminal, na raiz do projeto e com o ambiente virtual ativado:

```bash
python tasks.py smoke
```

O smoke verifica respostas HTTP do frontend, da API, do health e do catálogo de produtos. A filtragem é comprovada pelos testes específicos e pelo roteiro de demonstração.

## CI e evidências da AP1

O workflow está em [`.github/workflows/pipeline.yml`](../../../.github/workflows/pipeline.yml) e é disparado por `push`.

```text
lint → test → build
```

- `lint` executa Ruff.
- `test` declara `needs: lint` e executa Pytest após o sucesso do lint.
- `build` declara `needs: test` e executa `compileall` após o sucesso dos testes.

Cada job faz checkout, configura Python 3.12 e instala as dependências, pois executa em ambiente próprio. Se o lint falhar, os jobs seguintes são pulados; se os testes falharem, o build é pulado.

A validação local não comprova uma execução no GitHub Actions. Após enviar a branch, abra a aba **Actions**, localize a execução correspondente ao commit enviado e confira os três jobs e seus logs.

Para a demonstração da AP1, relacione a Issue #15, a branch, os commits com referência `#15`, a consulta no serviço, os testes específicos e a execução da pipeline. Conforme o guia da avaliação, a entrega termina na branch: sem PR, merge ou fechamento da Issue.
