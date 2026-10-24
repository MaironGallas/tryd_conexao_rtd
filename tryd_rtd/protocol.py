"""Comandos aceitos pelo servidor RTD do Tryd.

Cada requisição é enviada como ``<COMANDO><ATIVO>#`` (ex.: ``NEGS$S|WINZ26#``).
A resposta usa ``|`` para separar campos, ``@`` para separar vários registros
dentro de um mesmo campo e ``#`` para terminar a mensagem.
"""

from enum import Enum

TERMINADOR = "#"
SEPARADOR_CAMPO = "|"
SEPARADOR_REGISTRO = "@"


class Comando(str, Enum):
    COTACAO = "COT$S|"
    AUTOMATIZADOR = "AUT$S|"
    LIVRO_DE_OFERTAS = "LVL2$S|"
    NEGOCIO = "NEG$S|"
    NEGOCIO_COMPLETO = "NEGS$S|"
    INTERVALO_GRAFICO = "GRF$S|"


def montar_requisicao(comando: Comando, ativo: str) -> bytes:
    """Monta a requisição em bytes para um ativo."""
    return f"{comando.value}{ativo.strip().upper()}{TERMINADOR}".encode()
