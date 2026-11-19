# Módulo de Carrinho de Compras — AP2

**Instituição:** UNICATÓLICA  
**Curso:** Sistemas de Informação  
**Disciplina:** Análise e Projeto de Sistemas I  
**Aluno:** João Victor Costa dos Santos

## Objetivo
Prototipar um módulo de carrinho de compras com cálculo de subtotal, frete e cupons de desconto, demonstrando modelagem UML e padrões de projeto.

## Padrões aplicados
- **Strategy (comportamental):** `EstrategiaFrete` permite trocar o algoritmo de frete sem alterar o carrinho. Implementações: `FretePadrao`, `FreteExpresso` e `RetiradaLoja`.
- **Factory Method (criacional):** `CouponFactory` centraliza a criação de cupons percentuais e de valor fixo, evitando espalhar a lógica de instanciação pelo sistema.

## Requisitos
- Python 3.10 ou superior.
- Não utiliza bibliotecas externas.

## Como executar
```bash
python main.py
```

## Como executar os testes
```bash
python -m unittest discover -s tests -v
```

## Regras de negócio implementadas
1. Não é permitido adicionar quantidades menores ou iguais a zero.
2. Preços de produtos não podem ser negativos.
3. Frete padrão custa R$ 15,00 para subtotal inferior a R$ 200,00; acima disso é grátis.
4. Frete expresso custa R$ 25,00 abaixo de R$ 300,00; a partir daí custa R$ 12,50.
5. Retirada na loja não possui custo de frete.
6. Cupom percentual aceita valores entre 0% e 100%.
7. Cupom fixo não pode gerar desconto superior ao subtotal.
8. O total é subtotal menos desconto mais frete.

## Estrutura
```text
AP2_Carrinho_Compras/
├── docs/
│   └── DOCUMENTACAO_AP2.pdf
├── src/
│   ├── __init__.py
│   └── carrinho.py
├── tests/
│   ├── __init__.py
│   └── test_carrinho.py
├── main.py
└── README.md
```

## Diagramas UML
Os diagramas e a justificativa detalhada estão no PDF `docs/DOCUMENTACAO_AP2.pdf`.

## Autor
João Victor Costa dos Santos — trabalho acadêmico individual.
