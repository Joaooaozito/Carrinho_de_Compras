"""Núcleo do módulo de carrinho de compras.

Padrões implementados:
- Strategy (comportamental): cada modalidade de frete encapsula seu cálculo.
- Factory Method (criacional): CouponFactory cria o tipo de cupom solicitado.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import List


def dinheiro(valor: Decimal) -> Decimal:
    """Arredonda valores monetários para duas casas decimais."""
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Produto:
    id: int
    nome: str
    preco: Decimal

    def __post_init__(self):
        if self.preco < 0:
            raise ValueError("O preço do produto não pode ser negativo.")


@dataclass
class ItemCarrinho:
    produto: Produto
    quantidade: int

    def __post_init__(self):
        if self.quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

    @property
    def subtotal(self) -> Decimal:
        return dinheiro(self.produto.preco * self.quantidade)


class EstrategiaFrete(ABC):
    """Interface da família de algoritmos de cálculo de frete (Strategy)."""
    @abstractmethod
    def calcular(self, subtotal: Decimal) -> Decimal:
        raise NotImplementedError


class FretePadrao(EstrategiaFrete):
    def calcular(self, subtotal: Decimal) -> Decimal:
        return Decimal("15.00") if subtotal < Decimal("200.00") else Decimal("0.00")


class FreteExpresso(EstrategiaFrete):
    def calcular(self, subtotal: Decimal) -> Decimal:
        return Decimal("25.00") if subtotal < Decimal("300.00") else Decimal("12.50")


class RetiradaLoja(EstrategiaFrete):
    def calcular(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")


class Cupom(ABC):
    @abstractmethod
    def aplicar(self, subtotal: Decimal) -> Decimal:
        raise NotImplementedError


@dataclass(frozen=True)
class CupomPercentual(Cupom):
    percentual: Decimal

    def aplicar(self, subtotal: Decimal) -> Decimal:
        if not Decimal("0") <= self.percentual <= Decimal("100"):
            raise ValueError("O percentual deve estar entre 0 e 100.")
        return dinheiro(subtotal * self.percentual / Decimal("100"))


@dataclass(frozen=True)
class CupomValorFixo(Cupom):
    valor: Decimal

    def aplicar(self, subtotal: Decimal) -> Decimal:
        if self.valor < 0:
            raise ValueError("O valor do cupom não pode ser negativo.")
        return min(dinheiro(self.valor), subtotal)


class CouponFactory:
    """Factory Method simplificado: centraliza a criação de cupons."""
    @staticmethod
    def criar(tipo: str, valor: Decimal) -> Cupom:
        tipo = tipo.strip().lower()
        if tipo == "percentual":
            return CupomPercentual(valor)
        if tipo == "fixo":
            return CupomValorFixo(valor)
        raise ValueError(f"Tipo de cupom não suportado: {tipo}")


@dataclass
class Carrinho:
    itens: List[ItemCarrinho] = field(default_factory=list)
    estrategia_frete: EstrategiaFrete = field(default_factory=FretePadrao)
    cupom: Cupom | None = None

    def adicionar(self, produto: Produto, quantidade: int = 1) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        for item in self.itens:
            if item.produto.id == produto.id:
                item.quantidade += quantidade
                return
        self.itens.append(ItemCarrinho(produto, quantidade))

    def remover(self, produto_id: int) -> None:
        self.itens = [item for item in self.itens if item.produto.id != produto_id]

    @property
    def subtotal(self) -> Decimal:
        return dinheiro(sum((item.subtotal for item in self.itens), Decimal("0.00")))

    @property
    def desconto(self) -> Decimal:
        if self.cupom is None:
            return Decimal("0.00")
        return min(self.cupom.aplicar(self.subtotal), self.subtotal)

    @property
    def frete(self) -> Decimal:
        return dinheiro(self.estrategia_frete.calcular(self.subtotal))

    @property
    def total(self) -> Decimal:
        return dinheiro(self.subtotal - self.desconto + self.frete)

    def resumo(self) -> str:
        linhas = ["\n=== RESUMO DO CARRINHO ==="]
        for item in self.itens:
            linhas.append(
                f"{item.quantidade}x {item.produto.nome}: R$ {item.subtotal:.2f}"
            )
        linhas.extend([
            f"Subtotal: R$ {self.subtotal:.2f}",
            f"Desconto: R$ {self.desconto:.2f}",
            f"Frete: R$ {self.frete:.2f}",
            f"TOTAL: R$ {self.total:.2f}",
        ])
        return "\n".join(linhas)


def demonstracao() -> None:
    notebook = Produto(1, "Notebook", Decimal("2500.00"))
    mouse = Produto(2, "Mouse sem fio", Decimal("120.00"))

    carrinho = Carrinho(estrategia_frete=FreteExpresso())
    carrinho.adicionar(notebook, 1)
    carrinho.adicionar(mouse, 2)
    carrinho.cupom = CouponFactory.criar("percentual", Decimal("10"))

    print(carrinho.resumo())


if __name__ == "__main__":
    demonstracao()
