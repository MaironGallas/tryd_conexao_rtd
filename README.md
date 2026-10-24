# tryd_conexao_rtd

Cliente Python para o **servidor RTD do [Tryd](https://www.tryd.com.br/)**. Conecta por socket TCP à plataforma e mostra o **Times & Trades** de um ativo em tempo real no console, com o agressor colorido (verde = comprador, vermelho = vendedor).

```
      1021   10:31:02.512    128.455      5    308     72  Comprador
      1022   10:31:02.517    128.450      2     85    308  Vendedor
```

## Requisitos

- Python 3.9+
- Tryd aberto, com o **servidor RTD habilitado** (padrão: `127.0.0.1:12002`)

## Instalação

```bash
git clone https://github.com/MaironGallas/tryd_conexao_rtd.git
cd tryd_conexao_rtd
pip install -e .
```

## Uso

Na linha de comando:

```bash
python -m tryd_rtd WINZ26
python -m tryd_rtd DOLZ26 --intervalo 0.5
python -m tryd_rtd PETR4 --host 127.0.0.1 --port 12002 --sem-cor
```

Como biblioteca:

```python
from tryd_rtd import TrydClient, Comando, parse_negocios

with TrydClient("127.0.0.1", 12002) as cli:
    for msg in cli.assinar(Comando.NEGOCIO_COMPLETO, "WINZ26"):
        for n in parse_negocios(msg):
            print(n.hora, n.preco, n.qtde, n.agressor)
```

## Protocolo

| Comando | Código | Conteúdo |
|---|---|---|
| `COTACAO` | `COT$S\|` | Cotação |
| `AUTOMATIZADOR` | `AUT$S\|` | Automatizador |
| `LIVRO_DE_OFERTAS` | `LVL2$S\|` | Livro de ofertas |
| `NEGOCIO` | `NEG$S\|` | Último negócio |
| `NEGOCIO_COMPLETO` | `NEGS$S\|` | Times & Trades (usado pelo CLI) |
| `INTERVALO_GRAFICO` | `GRF$S\|` | Intervalo gráfico |

- A requisição é `<CÓDIGO><ATIVO>#`, por exemplo `NEGS$S|WINZ26#`.
- Na resposta, `|` separa campos, `@` separa vários registros dentro de um campo e `#` encerra a mensagem.
- No `NEGS`, os campos são: id, hora, preço, quantidade, corretora compradora, corretora vendedora e agressor.

O cliente guarda os bytes recebidos num buffer e só entrega mensagens completas, delimitadas por `#`. Assim, nenhum negócio se perde quando a resposta passa de 8 KB.

Apenas o parser de `NEGS` está implementado. Os demais comandos já podem ser enviados com `TrydClient.requisitar()`, mas devolvem a mensagem crua.

## Estrutura

```
tryd_rtd/
  protocol.py      # comandos e formato das mensagens
  client.py        # conexão TCP, buffer e polling
  times_trades.py  # parser e formatação do Times & Trades
  __main__.py      # CLI
tests/             # testes (pytest), incluindo um servidor RTD falso
```

## Testes

```bash
pip install -e ".[dev]"
pytest
```

## Licença

AGPL-3.0. Veja [LICENSE](LICENSE).
