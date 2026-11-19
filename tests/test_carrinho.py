import unittest
from decimal import Decimal

from src.carrinho import (
    Produto, Carrinho, FretePadrao, FreteExpresso, RetiradaLoja,
    CouponFactory
)


class CarrinhoTests(unittest.TestCase):
    def setUp(self):
        self.produto = Produto(1, "Teclado", Decimal("100.00"))

    def test_adicionar_e_subtotal(self):
        carrinho = Carrinho()
        carrinho.adicionar(self.produto, 2)
        self.assertEqual(carrinho.subtotal, Decimal("200.00"))

    def test_frete_padrao_gratis_a_partir_de_200(self):
        carrinho = Carrinho(estrategia_frete=FretePadrao())
        carrinho.adicionar(self.produto, 2)
        self.assertEqual(carrinho.frete, Decimal("0.00"))

    def test_frete_express(self):
        carrinho = Carrinho(estrategia_frete=FreteExpresso())
        carrinho.adicionar(self.produto, 1)
        self.assertEqual(carrinho.frete, Decimal("25.00"))

    def test_retirada_gratis(self):
        carrinho = Carrinho(estrategia_frete=RetiradaLoja())
        carrinho.adicionar(self.produto)
        self.assertEqual(carrinho.frete, Decimal("0.00"))

    def test_cupom_percentual(self):
        carrinho = Carrinho()
        carrinho.adicionar(self.produto, 2)
        carrinho.cupom = CouponFactory.criar("percentual", Decimal("10"))
        self.assertEqual(carrinho.desconto, Decimal("20.00"))

    def test_cupom_fixo_nao_supera_subtotal(self):
        carrinho = Carrinho()
        carrinho.adicionar(self.produto)
        carrinho.cupom = CouponFactory.criar("fixo", Decimal("150.00"))
        self.assertEqual(carrinho.desconto, Decimal("100.00"))

    def test_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            carrinho = Carrinho()
            carrinho.adicionar(self.produto, 0)

    def test_tipo_cupom_invalido(self):
        with self.assertRaises(ValueError):
            CouponFactory.criar("misterioso", Decimal("5"))


if __name__ == "__main__":
    unittest.main()
