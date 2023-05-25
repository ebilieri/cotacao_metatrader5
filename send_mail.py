import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime

class EnviaEmail:
    
    load_dotenv()


    def envia_email(self, ticker: str, valor_projetado: str, valor_atual: str, operacao: str) -> None:
        senha = os.environ.get("senha_email")
        email_from = os.environ.get("email")
        now = datetime.today().isoformat()
        
        msg = EmailMessage()
        msg['Subject'] = f"{ticker} -> {valor_atual} -> Alerta de {operacao} Python Ticker B3"
        msg['From'] = email_from
        msg['To'] = os.environ.get("list_mail_to")
        msg.set_content(f'''
        
        {operacao} 
        
        Valor ultima Maxima Invest {valor_projetado}
        
        O ativo {ticker} chegou no preço de {operacao} {valor_atual}

        --------------------------------------------------

        Data/Hora: {now}
        ''')

        # Send mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
            smtp.login(email_from, senha)
            smtp.send_message(msg)