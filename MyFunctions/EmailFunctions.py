# Descrição
"""
Funções referentes a comunicação com Email.
"""

# Email Function:
import os, ssl, smtplib
from email.message import EmailMessage
from typing import Optional
from typing import cast

# Aquisitando API KEY
from dotenv import load_dotenv
load_dotenv()  # Carrega as variáveis do .env
email = os.getenv("email")
app_key = os.getenv("app_key")

def SendEmail(subject:str, to_who:str, message:str, user: Optional[str] = email, senha: Optional[str] = app_key, html = None):

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = user
        msg["To"]   = to_who

        if html:
            msg.add_alternative(message, subtype="html")
        else:
            msg.set_content(message)

        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls(context=context)            # ativa TLS 1.2+
            user_str = cast(str, user)
            senha_str = cast(str, senha)
            smtp.login(user_str, senha_str)      # usa App Password
            smtp.send_message(msg)
