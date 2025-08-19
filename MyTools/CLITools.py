# Dependencias para setar ambiente correto
import os
import sys
this_dir = os.path.dirname(os.path.abspath(__file__))        # .../V1/MyAgents
parent_dir = os.path.abspath(os.path.join(this_dir, os.pardir))
sys.path.insert(0, parent_dir)  # agora `V1` está no sys.path

from pathlib import Path
from agno.tools import tool
from MyFunctions.CLIFunctions import *

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description="Procura um diretório pelo nome dentro de outro, retornando o caminho ou mensagem de erro."
)
def find_directory(root_path: str, dir_name: str) -> str:
    """
    Wrapper como *tool* que converte argumentos JSON‑friendly em Path,
    chama a função original e devolve sempre uma str.
    """
    p = Path(root_path)
    result = find_directory_logic(p, dir_name)
    return str(result)

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description="Lista os arquivos e subdiretórios de um caminho informado."
)
def list_directory_contents(target_path: str) -> str:
    """
    Wrapper como *tool*: recebe uma string, converte em Path,
    chama a função original e devolve a saída formatada.
    """
    p = Path(target_path)
    result = list_directory_contents_logic(p)
    return result  # já é string

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description="""
    Função que dado um alvo, retorna todos os possíveis paths,
    cuja o qual esse alvo pode ser encontrado.

    Útil para quando o usuário der apenas um nome e precisar
    para aquisitar no sistema.
    """
)
def serch_for_full_path(target:str) -> str:
    """
    This function make a full search in the system,
    looking for the full path of the target
    """

    result = find_path_globally_logic(target)
    return result