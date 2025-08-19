# Dependencias para setar ambiente correto
import os
import sys
this_dir = os.path.dirname(os.path.abspath(__file__))        # .../V1/MyAgents
parent_dir = os.path.abspath(os.path.join(this_dir, os.pardir))
sys.path.insert(0, parent_dir)  # agora `V1` está no sys.path

from agno.tools import tool
from typing import Annotated
from MyFunctions.FileFunctions import *

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description=("""
    Função útil para salvar conteúdo de texto em um arquivo.
    
    Por vezes o usuário pode solucitar para o agente fazer uma
    pesquisa e salvar essa pesquisa em um arquivo. Essa
    função é pensada para ser usada exatamente nesse caso.
    """),
    
)
def save_file(
    text: Annotated[str, "Conteúdo do arquivo"],
    filename: Annotated[str, "Nome do arquivo (sem extensão)"],
    fmt: Annotated[str, "Formato: ‘md’, ‘pdf’ ou ‘docx’"] = "md",
    dir_path: Annotated[str, "Diretório de saída (opcional)"] = "",
) -> str:
    
    """
    Function to write a content in a file.
    """
    try:
        save_to_file_logic(text, filename, fmt, dir_path)
        return "Arquivo salvo com sucesso."
    except Exception as e:
        return f"Error: {e}"