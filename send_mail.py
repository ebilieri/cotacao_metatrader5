import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

class EnviaEmail:
    
    
    def envia_email(self, ticker_item: str, valor_projetado: str, valor_atual: str, operacao: str) -> None:
        senha = os.environ.get("senha_email")
        email_from = os.environ.get("email")
        now = datetime.today().isoformat()
        
        msg = EmailMessage()
        msg['Subject'] = f"{ticker_item} -> {valor_atual} -> Alerta de {operacao} Python Ticker B3"
        msg['From'] = email_from
        msg['To'] = os.environ.get("list_mail_to")
        msg.set_content(f'''
        
        {operacao} 
        
        Valor Invest projetado {valor_projetado}
        
        O ativo {ticker_item} chegou no preço de {operacao} {valor_atual}

        --------------------------------------------------

        Data/Hora: {now}
        ''')

        # Send mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
            smtp.login(email_from, senha)
            smtp.send_message(msg)


    def envia_email(self, lista_ativos: [], operacao: str) -> None:
        senha = os.environ.get("senha_email")
        email_from = os.environ.get("email")
        now = datetime.today().isoformat()

        msg = EmailMessage()
        msg['Subject'] = f"--> Alerta de {operacao} Python Ticker B3 <--"
        msg['From'] = email_from
        msg['To'] = os.environ.get("list_mail_to")

        mensagem = ""
        for row in lista_ativos:
        
            mensagem += f'''   {operacao} ---->>> {row["ticker"]} <<<-----\n'''
                
            mensagem += f'''   Valor Invest projetado -->> R$ {row["valor_projetado"]} <<-- \n'''
                
            mensagem += f'''   O ativo {row["ticker"]} chegou no preço de {operacao} -->> R$ {row["valor_atual"]} <<-- \n'''

            mensagem += f'''   Data/Hora: {now} \n'''

            mensagem += f'''   -------------------------------------------------- \n'''

            mensagem += '\n\n'

        msg.set_content(f''' {mensagem} ''')

        # Send mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
            smtp.login(email_from, senha)
            smtp.send_message(msg)
    