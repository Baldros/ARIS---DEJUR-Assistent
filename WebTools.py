from agno.tools import tool
from WebFunctions import *

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description="Caso haja link na mensagem, essa ferramenta ajuda a ter acesso ao conteúdo do link"
)
def search_site_content(url:str) -> str:
    """
    Given the link or URL of the page, this tool performs
    scraping and extracts the content  of the provided page
    in Markdown, supplying it as context to the model.
    """

    md_content = search_site_content_logic(url)

    return md_content

@tool(
    show_result=False,
    stop_after_tool_call=False,
    description="""
    Caso a ferramenta search_site_content não retorne um bom resultado,
    essa ferramenta pode ajudar. Criada para lidar com sites mais complexos, 
    essa ferramenta lida com sites que sejam protegidos por serviços como os
    da CloudFlare, que demandam um navegador que rode JS.
    """
)
def search_content_in_complex_site(url:str) -> str:
    """
    A tool designed to handle more complex websites,
    protected by services like CloudFlare,
    which require a browser that runs JS.
    """
    md_content = search_content_in_complex_site_logic(url)
    

    return md_content
