"""Cliente Python para o servidor RTD do Tryd."""

from .client import TrydClient
from .protocol import Comando
from .times_trades import Negocio, parse_negocios

__all__ = ["TrydClient", "Comando", "Negocio", "parse_negocios"]
__version__ = "0.2.0"
