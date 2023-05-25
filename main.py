from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import time

from send_mail import EnviaEmail

compra = "COMPRA"
venda = "VENDA"
# instanciar Email
email = EnviaEmail()

# iniciar Metatrader
mt5.initialize()

simbolos = mt5.symbols_get()
print(len(simbolos))

# for ticker in simbolos:
#     print(ticker.name)


# carregar ativos monitorados
df = pd.read_excel("ativos.xlsx")

while True:
    for row in df.iterrows():
        print(f"{row[1]['Ticker']} - Minima 6M {row[1]['Minima6']} - Maxima {row[1]['Maxima']}")

        # valores informados na planilha
        ticker = row[1]['Ticker']
        minima6m = row[1]['Minima6']
        maxima = row[1]['Maxima']

        # selecionar ativo
        mt5.symbol_select(ticker)
        # carregar dados do ticker
        tick_mt5 = mt5.symbol_info_tick(ticker)
        print(f"Fechamento: {tick_mt5.last}")
        print(f"Valor compra: {tick_mt5.ask}")
        print(f"Valor venda: {tick_mt5.bid}")
        print(f"{datetime.today().isoformat()}-----------------")

        if tick_mt5.bid > 0:
            # Minima === COMPRA
            if tick_mt5.bid <= minima6m:
                email.envia_email(ticker=ticker, valor_projetado=maxima, valor_atual=tick_mt5.bid, operacao=compra)

            # Maxima === VENDA
            if tick_mt5.bid >= maxima:
                email.envia_email(ticker=ticker, valor_projetado=maxima, valor_atual=tick_mt5.bid, operacao=venda)

    # pausa em segundos  
    print("=======================================================")  
    print("         ===================================")  
    print("                 ==================")  
    print("                         =      ")  
    time.sleep(5)





