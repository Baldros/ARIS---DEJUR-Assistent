# Descrição:
"""
Arquivo contendo os agentes, a principio aglomerará todos os agentes aqui,
a título de velocidade, mas no futuro podemos modularizar em arquivos diferentes
como fazemos as funções e ferramentas.
"""

# Dependencias para setar ambiente correto
import os
import sys
this_dir = os.path.dirname(os.path.abspath(__file__))        # .../V1/MyAgents
parent_dir = os.path.abspath(os.path.join(this_dir, os.pardir))
sys.path.insert(0, parent_dir)  # agora `V1` está no sys.path

# Dependencias para a construção do agente
from agno.agent import Agent
from agno.team import Team

# Modelo core do sistema
from agno.models.openai import OpenAIChat

# Ferramentas
from MyTools.FileTools import * # Ferramentas para manipulação de arquivos
from MyTools.WebTools import * # Ferramentas para busca na internet
from MyTools.EmailTools import *
from MyTools.CLITools import *
from agno.tools.googlesearch import GoogleSearchTools # Ferramenta nativa para busca na internet (via texto apenas!)
from agno.tools.arxiv import ArxivTools # Arxiv para buscas especializadas


# Sistema de comportamento:
from SystemFiles.BehaviorSistem import (aristoteles_behavior, # Comportamento do Team Leader
                                        oraculo_behavior, # Comportamento do Agente de Pesquisa
                                        ptolomeu_behavior, # Comportamento do agente de tratamento de documentos
                                        hermes_behavior #  Comportamento do agente de mensageria
                                        ) 

# Structured Answer
from pydantic import BaseModel
from typing import Optional

# Aquisitando API KEY
from dotenv import load_dotenv
load_dotenv()  # Carrega as variáveis do .env
api_key = os.getenv("OPENAI_KEY")

# -------------------- Modelo de saída --------------------
class LegalOutput(BaseModel):
    analysis: str
    jurisprudence_links: Optional[list[str]]
    summary: Optional[str]


# Construção dos Agentes:
# ----------- Resposta Estruturada ------------------
class StructureAnswer(BaseModel):
    answer: str
    links: Optional[list[str]]
    tools: Optional[list[str]]

# ----------------- Agents ---------------------------
# Oraculo - A pesquisadora
Oraculo = Agent(
    name="Oráculo",
    role= "Você é o agente de busca na web",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    description = oraculo_behavior["description"],
    instructions = oraculo_behavior["instructions"],
    tools=[
        # Sistema de busca padrão:
        GoogleSearchTools(), ArxivTools(), 

        # Funções mais elaboradas para lidar com problemas complexos:
        search_site_content, search_content_in_complex_site,
        ],
)

# Ptolomeu - O bibliotecário
Ptolomeu = Agent(
    name="Ptolomeu",
    role = "Você é o agente que lida com arquivos.",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    description = ptolomeu_behavior["description"],
    instructions = ptolomeu_behavior["instructions"],
    tools=[

        ],
)

Hermes = Agent(
    name = "Hermes",
    role = "Você é responsável por enviar emails",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    description = hermes_behavior["description"],
    instructions = hermes_behavior["instructions"],
    tools=[
        # Envio de Email:
        Send_Email,   
        ],
    )

# ------------- Costrução do Team --------------------------------
# Aristoteles - Team Leader
IA_DEJUR = Team(
    name="Aris", 
    mode="coordinate",
    members=[Oraculo, Ptolomeu, Hermes],
    model= OpenAIChat(id="gpt-4o", api_key=api_key), # Platão
    description = aristoteles_behavior["description"],
    instructions = aristoteles_behavior["instructions"],
    response_model = LegalOutput,
    )