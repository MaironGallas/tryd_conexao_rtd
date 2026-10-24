import socket
import threading

from tryd_rtd import Comando, TrydClient, parse_negocios
from tryd_rtd.protocol import montar_requisicao


def test_requisicao():
    assert montar_requisicao(Comando.NEGOCIO_COMPLETO, " winz26 ") == b"NEGS$S|WINZ26#"


def test_parse_um_negocio():
    msg = "NEGS$S|101|10:00:01.123|128.450|5|3|72|Comprador#"
    [n] = parse_negocios(msg)
    assert (n.id, n.preco, n.qtde, n.agressor) == ("101", "128.450", "5", "Comprador")


def test_parse_varios_negocios():
    msg = "NEGS$S|1@2|10:00@10:01|10@11|1@2|3@4|5@6|Comprador@Vendedor"
    ns = parse_negocios(msg)
    assert [n.id for n in ns] == ["1", "2"]
    assert ns[1].agressor == "Vendedor"


def test_parse_invalido():
    assert parse_negocios("lixo") == []
    assert parse_negocios("NEGS$S|1@2|a|b|c|d|e|f") == []  # contagem desigual


def test_cliente_remonta_mensagem_fragmentada():
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def servir():
        conn, _ = srv.accept()
        conn.recv(1024)
        conn.sendall(b"NEGS$S|1|10:00|10|1|3|5|Comp")
        conn.sendall(b"rador#NEGS$S|2|10:01|11|2|3|5|Vend")
        conn.recv(1024)
        conn.sendall(b"edor#")
        conn.close()

    threading.Thread(target=servir, daemon=True).start()
    with TrydClient("127.0.0.1", port) as cli:
        a = cli.requisitar(Comando.NEGOCIO_COMPLETO, "WINZ26")
        b = cli.requisitar(Comando.NEGOCIO_COMPLETO, "WINZ26")
    srv.close()
    assert [parse_negocios(m)[0].agressor for m in a + b] == ["Comprador", "Vendedor"]
