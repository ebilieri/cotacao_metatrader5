from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import MetaTrader5 as mt5
import time
from datetime import datetime

from send_mail import EnviaEmail

load_dotenv()

compra = "COMPRA"
venda = "VENDA"
planilha_ativos = os.environ.get("planilha_ativos")
# instanciar Email
email = EnviaEmail()

# iniciar Metatrader
mt5.initialize()

simbolos = mt5.symbols_get()
print(len(simbolos))

# for ticker in simbolos:
#     print(ticker.name)


# carregar ativos monitorados
df = pd.read_excel(planilha_ativos)

while True:
    date_now = datetime.now()
    date_start = datetime(datetime.now().year,
                          datetime.now().month,
                          datetime.now().day,
                          9, 55, 0)
    date_end = datetime(datetime.now().year,
                          datetime.now().month,
                          datetime.now().day,
                          17, 30, 0)
    
    if date_now >= date_start and date_now <= date_end:
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

            if tick_mt5 is not None:
                print(f"Ultimo: {tick_mt5.last}")
                print(f"Valor compra: {tick_mt5.ask}")
                print(f"Valor venda: {tick_mt5.bid}")
                print(f"{datetime.today().isoformat()}-----------------")
                print("")

                if tick_mt5.last > 0:
                    # Minima === COMPRA
                    if tick_mt5.last <= minima6m:
                        email.envia_email(ticker=ticker, valor_projetado=minima6m, valor_atual=tick_mt5.bid, operacao=compra)

                    # Maxima === VENDA
                    if tick_mt5.last >= maxima:
                        email.envia_email(ticker=ticker, valor_projetado=maxima, valor_atual=tick_mt5.bid, operacao=venda)

    # pausa em segundos  
    print("=======================================================")  
    print(f"        ------{datetime.today().isoformat()}--------")
    print("         ===================================")  
    print("                 ==================")  
    print("                         =      ")  
    time.sleep(20)





