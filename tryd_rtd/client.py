"""Cliente TCP para o servidor RTD do Tryd."""

from __future__ import annotations

import socket
import time
from typing import Iterator, Optional

from .protocol import TERMINADOR, Comando, montar_requisicao

_TAM_BUFFER = 8192


class TrydClient:
    """Conexão com o RTD do Tryd (por padrão em ``127.0.0.1:12002``).

    Uso::

        with TrydClient() as cli:
            for msg in cli.assinar(Comando.NEGOCIO_COMPLETO, "WINZ26"):
                ...
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 12002, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._buffer = ""

    def __enter__(self) -> "TrydClient":
        self.conectar()
        return self

    def __exit__(self, *exc) -> None:
        self.fechar()

    def conectar(self) -> None:
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)

    def fechar(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def requisitar(self, comando: Comando, ativo: str) -> list[str]:
        """Envia uma requisição e devolve as mensagens completas recebidas.

        As mensagens são delimitadas por ``#``. Pedaços incompletos ficam no
        buffer e são completados na próxima leitura, então nenhum negócio se
        perde quando a resposta passa de 8192 bytes.
        """
        if self._sock is None:
            raise RuntimeError("Cliente não conectado; chame conectar() primeiro.")

        self._sock.sendall(montar_requisicao(comando, ativo))
        while TERMINADOR not in self._buffer:
            chunk = self._sock.recv(_TAM_BUFFER)
            if not chunk:
                raise ConnectionError("Servidor RTD encerrou a conexão.")
            self._buffer += chunk.decode("latin-1")

        *completas, self._buffer = self._buffer.split(TERMINADOR)
        return [m for m in completas if m.strip()]

    def assinar(self, comando: Comando, ativo: str, intervalo: float = 0.2) -> Iterator[str]:
        """Faz polling contínuo e gera cada mensagem recebida."""
        while True:
            yield from self.requisitar(comando, ativo)
            time.sleep(intervalo)
