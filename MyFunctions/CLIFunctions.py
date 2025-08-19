# Dependências
from pathlib import Path
from typing import Union
from tqdm import tqdm
import os

def find_directory_logic(root_path: Path, dir_name: str) -> Path | str:
    """
    Procura **recursivamente** por um diretório com nome `dir_name` a partir de `root_path`.
    Retorna o primeiro Path encontrado que for um diretório ou:
      • uma string “None path found” se nenhum encontrado,
      • ou uma string com mensagem de exceção em caso de erro.
    """
    try:
        found = list(root_path.rglob(dir_name))
        for p in found:
            if p.is_dir():
                return p
        return "None path found"
    except Exception as e:
        return f"Ocorreu um erro durante a busca: {e}"


def list_directory_contents_logic(target_path: Path) -> str:
    """
    Retorna uma string formatada com os conteúdos de `target_path`.
    Cada item do diretório:
      • “[DIR] nome_do_diretorio” se for diretório;
      • “  nome_do_arquivo” se for arquivo.
    Se o `target_path` não existir ou não for diretório, retorna mensagem de erro.
    """
    if not target_path or not target_path.exists() or not target_path.is_dir():
        return f"Error: The path provided is not a valid directory."

    output = []
    for item in sorted(target_path.iterdir()):
        prefix = "[DIR]" if item.is_dir() else "     "
        output.append(f"{prefix} {item.name}")
    return "\n".join(output)



def find_path_globally_logic(target_name: str) -> str:
    """
    Busca por um arquivo ou diretório com nome `target_name` em todos os discos acessíveis.
    
    Retorna uma lista de caminhos completos encontrados.
    """
    found_paths = []

    # Detecta sistemas de arquivos
    drives = []
    if os.name == "nt":  # Windows
        import string
        from ctypes import windll

        bitmask = windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                drives.append(f"{string.ascii_uppercase[i]}:\\")
    else:
        # Para Linux/macOS, varre apenas a raiz (/) e talvez /mnt
        drives = ["/", "/mnt"]

    print("Listando diretórios possíveis...")
    for drive in tqdm(drives, desc="Etapa drives"):
        try:
            for root, dirs, files in os.walk(drive, topdown=True, followlinks=False):
                # Busca em diretórios
                if target_name in dirs:
                    found_paths.append(str(Path(root) / target_name))

                # Busca em arquivos
                if target_name in files:
                    found_paths.append(str(Path(root) / target_name))
        except (PermissionError, OSError):
            continue  # Ignora pastas protegidas

    if len(found_paths) >= 1:
        return ", ".join(found_paths)

    elif len(found_paths) == 0:
        return "the search did not find any results"
    
    else:
        return "".join(found_paths)
