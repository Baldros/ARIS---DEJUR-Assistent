# Dependencias
from agno.tools import tool
from typing import Optional
from EmailFunctions import *

# Aquisitando email do administrador
adm_email = st.secrets["master_email"]

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description="""
    Enviar notificações por e-mail ao responsável pelo sistema em casos de:
    - falha ou problema insuperável na execução de uma tarefa;
    - solicitação do usuário, demandando algo;
    - feedback do usuário;
    - Caso haja a ferramenta, mas ela não esteja configurada para aquele propósito.

    Parâmetros:
      subject (str): assunto do e-mail. Deve ser o resumo do assunto em uma frase bem curta.
      message (str): corpo da mensagem; pode ser HTML se html=True. Contextualize sobre o problema no corpo da mensagem.
      html (bool, opcional): se True, envia como HTML; caso contrário, como texto simples.

    Retorno:
      str: "Email enviado com sucesso." em caso de êxito; "Erro: <detalhes>" em caso de falha.

    Uso esperado pelo agente:
    - Ferramenta utilizada automaticamente pelo agente supervisor (ex: Platão) ao detectar incapacidade de concluir a tarefa.
    - O agente deve interpretar a string de retorno:
        • Se inicia com "Email enviado com sucesso", considera a ferramenta executada com êxito.
        • Se inicia com "Erro:", deve acionar fluxo de fallback (retry, log, notificar o usuário).
    - Não gera múltiplas chamadas repetidas; usar apenas uma vez por incidente.

    Limitações:
    - Destinatário fixo como administrador (adm_email); o agente não deve tentar alterar este valor.
    - Não cabe ao agente métier interpretar ou formatar e-mails — apenas acionar esta ferramenta quando pertinente.

    Exemplo de instruction para Platão:
      "Quando não houver agente capaz de cumprir a tarefa automaticamente, use esta ferramenta Send_Email(...) para notificar o responsável e interprete o retorno para decidir o próximo passo."
    """
)
def Send_Email(subject:str, message:str, html: Optional[bool] = None):
    """
    📧 Ferramenta de envio de e-mail para notificação ao implementador responsável.

    Parâmetros:
        subject (str): Assunto da mensagem.
        message (str): Corpo da mensagem (texto ou HTML conforme flag).
        html (Optional[bool]): Se True, envia como HTML. Se False ou None, envia como plain text.

    Comportamento:
    - Sempre envia para o e‑mail do administrador (“mestre da implementação”).
    - Retorna string informando sucesso ou mensagem de erro detalhada.

    Regras para Agente Agno:
    - Esta ferramenta é chamada automaticamente pelo agente supervisor (ex: Platon) em caso de problema/falha.
    - O agente deve interpretar a saída para decidir se a entrega foi bem-sucedida:
        • “Email enviado com sucesso.” → boletim de sucesso;
        • “Erro: …” → capturar e reagir com outro fluxo (ex: fallback, retry).
    - Não apresentar saídas adicionais ou logs internos no retorno — apenas o texto mencionado.

    Exemplos de uso em instructions de agente:
      • “Use Send_Email(...) se a tarefa não puder ser completada automaticamente.”
      • “Após chamada de Send_Email, verifique o resultado e informe ao usuário adequadamente.”

    Internamente:
    - Utiliza `cast(str, adm_email)` para garantir compatibilidade com tipagem.
    - Captura exceções e retorna mensagem com o texto do erro.

    Retorno:
        str: Mensagem de status (“Email enviado...” ou “Erro: ...”)
    """
    try:
        adm_email_str = cast(str, adm_email)
        SendEmail(subject=subject, to_who=adm_email_str,message=message, html=html)
        return "Email enviado com sucesso."
    except Exception as e:

        return f"Erro: {e}"



