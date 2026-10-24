"""Mostra o Times & Trades de um ativo no console.

    python -m tryd_rtd WINZ26
    python -m tryd_rtd DOLZ26 --host 127.0.0.1 --port 12002 --intervalo 0.5
"""

import argparse
import sys

from .client import TrydClient
from .protocol import Comando
from .times_trades import formatar, parse_negocios


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tryd_rtd", description="Times & Trades em tempo real via RTD do Tryd.")
    p.add_argument("ativo", help="código do ativo, ex.: WINZ26, DOLZ26, PETR4")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=12002)
    p.add_argument("--intervalo", type=float, default=0.2, help="segundos entre requisições (padrão 0.2)")
    p.add_argument("--sem-cor", action="store_true", help="desliga as cores no console")
    args = p.parse_args(argv)

    if not args.sem_cor:
        import colorama

        colorama.just_fix_windows_console()

    try:
        with TrydClient(args.host, args.port) as cli:
            for msg in cli.assinar(Comando.NEGOCIO_COMPLETO, args.ativo, args.intervalo):
                for negocio in parse_negocios(msg):
                    print(formatar(negocio, cor=not args.sem_cor))
    except KeyboardInterrupt:
        return 0
    except OSError as ex:
        print(f"Não foi possível falar com o RTD em {args.host}:{args.port}: {ex}", file=sys.stderr)
        print("Confira se o Tryd está aberto e com o servidor RTD habilitado.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
