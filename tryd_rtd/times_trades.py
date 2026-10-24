"""Parser e formatação do Times & Trades (comando NEGOCIO_COMPLETO)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .protocol import SEPARADOR_CAMPO, SEPARADOR_REGISTRO, TERMINADOR

# Prefixo + 7 campos: id, hora, preço, quantidade, comprador, vendedor, agressor
_N_CAMPOS = 8


@dataclass(frozen=True)
class Negocio:
    id: str
    hora: str
    preco: str
    qtde: str
    comprador: str
    vendedor: str
    agressor: str


def parse_negocios(mensagem: str) -> List[Negocio]:
    """Converte uma mensagem ``NEGS`` em uma lista de negócios.

    Um campo pode trazer vários negócios separados por ``@``; nesse caso todos
    os campos precisam ter o mesmo número de registros. Mensagens fora do
    formato esperado retornam lista vazia.
    """
    campos = mensagem.strip().rstrip(TERMINADOR).split(SEPARADOR_CAMPO)
    if len(campos) != _N_CAMPOS:
        return []

    colunas = [c.split(SEPARADOR_REGISTRO) for c in campos[1:]]
    n = len(colunas[0])
    if any(len(c) != n for c in colunas):
        return []

    return [Negocio(*(c[i] for c in colunas)) for i in range(n)]


_CORES = {"Comprador": "GREEN", "Vendedor": "RED"}


def formatar(negocio: Negocio, cor: bool = True) -> str:
    """Linha alinhada para o console; agressor colorido se ``cor`` for True."""
    agressor = negocio.agressor
    if cor and agressor in _CORES:
        from colorama import Fore, Style

        agressor = f"{getattr(Fore, _CORES[agressor])}{agressor}{Style.RESET_ALL}"

    return (
        f"{negocio.id:>10} {negocio.hora:>12} {negocio.preco:>10} "
        f"{negocio.qtde:>6} {negocio.comprador:>6} {negocio.vendedor:>6}  {agressor}"
    )
