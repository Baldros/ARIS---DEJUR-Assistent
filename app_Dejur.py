# Descrição
"""
Construção do app DEJUR.
"""

# Dependencias:
from MyAgents.Agents import IA_DEJUR
from agno.team import TeamRunResponse
import streamlit as st
import json
import os
import base64

# -------------------- Helpers de persistência --------------------  # NEW
STORAGE_PATH = "chats.json"

def load_storage() -> dict:
    if os.path.exists(STORAGE_PATH):
        try:
            with open(STORAGE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    else:
        data = {}

    # Migração: se o arquivo antigo era { "1": {...}, "2": {...} }  # NEW
    # empacotamos em um bucket "_legacy"
    if data and all(isinstance(v, dict) and "title" in v for v in data.values()):
        data = {"_legacy": data}
    return data

def save_storage(storage: dict) -> None:
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)

def ensure_user_bucket(storage: dict, user_id: str) -> None:
    storage.setdefault(user_id, {})
    # Se não houver conversas, cria "Conversa 1"
    if not storage[user_id]:
        storage[user_id]["1"] = {"title": "Conversa 1", "messages": []}

def next_chat_id_for(storage: dict, user_id: str) -> str:
    keys = [int(k) for k in storage[user_id].keys() if k.isdigit()]
    return str(max(keys) + 1) if keys else "1"

# -------------------- Inicialização de estado --------------------
st.set_page_config(
    page_title="ARIS - DEJUR assistent",
    page_icon="🤖",
    layout="wide",      # layout wide
    initial_sidebar_state="auto", 
    menu_items=None,
)

if "storage" not in st.session_state:  # NEW
    st.session_state.storage = load_storage()

if "user_id" not in st.session_state:  # NEW
    st.session_state.user_id = None

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None



# --------------------- Melhorias da Pagina --------------------------
path_image = 'logo_mgeb_transparente.png'
#st.logo(path_image, size="large")

# Converte para base64
with open(path_image, "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()

col1, col2 = st.columns([1, 15])

with col1:
    st.image(path_image, width=100)

with col2:
    st.markdown(
        f'''
        <div style="
            background-color:#D24334;
            width:100%;
            height:80px;
            padding:0 20px;
            display:flex;
            align-items:center;
            justify-content:flex-start;
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        ">
            <h1 style="
                color:white;
                font-size:28px;
                margin:0;
                font-weight:600;
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            ">
                ARIS - IA DEJUR
            </h1>
        </div>
        ''',
        unsafe_allow_html=True
    )
# -------------------- Gate de Identificador --------------------  # NEW
if not st.session_state.user_id:
    st.title("DEJUR — Identificador")
    user_input = st.text_input("Digite seu identificador de conversas (livre, ex.: email, apelido, etc.)")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Entrar"):
            if user_input.strip():
                st.session_state.user_id = user_input.strip()
                ensure_user_bucket(st.session_state.storage, st.session_state.user_id)
                # Define chat ativo inicial
                first_id = next(iter(st.session_state.storage[st.session_state.user_id].keys()))
                st.session_state.active_chat_id = first_id
                save_storage(st.session_state.storage)
                st.rerun()
            else:
                st.info("Informe um identificador válido.")
    st.stop()

# A partir daqui, temos user_id definido e um bucket garantido.
user_id = st.session_state.user_id  # NEW
ensure_user_bucket(st.session_state.storage, user_id)  # NEW

# Para manter seu código, criamos um "alias" que aponta só para as conversas do usuário atual
st.session_state.chats = st.session_state.storage[user_id]  # NEW

def new_chat(default_title: str | None = None) -> str:
    """Cria uma nova conversa **no bucket do user atual** e retorna o chat_id."""
    next_id = next_chat_id_for(st.session_state.storage, user_id)  # NEW
    st.session_state.chats[next_id] = {
        "title": default_title or f"Conversa {next_id}",
        "messages": [],
    }
    st.session_state.active_chat_id = next_id
    save_storage(st.session_state.storage)  # NEW
    return next_id

# Se por algum motivo não houver conversas (já tratado), reforça
if not st.session_state.chats:
    new_chat()

# -------------------- Sidebar: Seleção de Conversa --------------------
with st.sidebar:
    st.markdown("### 🗨️ Conversas")
    chat_ids = list(st.session_state.chats.keys())

    if st.session_state.active_chat_id not in chat_ids:
        st.session_state.active_chat_id = chat_ids[0] if chat_ids else None

    selected_id = st.selectbox(
        "Selecione a conversa:",
        options=chat_ids,
        index=chat_ids.index(st.session_state.active_chat_id) if st.session_state.active_chat_id in chat_ids else 0,
        format_func=lambda cid: st.session_state.chats[cid]["title"],
    )
    st.session_state.active_chat_id = selected_id

    # -------------------- Ações Rápidas --------------------
    st.markdown("### ⚙️ Ações Rápidas")
    if st.button("➕ Nova conversa", use_container_width=True):
        new_chat()
        st.rerun()  # Para o UI refletir a nova conversa

    if st.button("🔄 Trocar identificador", use_container_width=True):
        st.session_state.user_id = None
        st.session_state.active_chat_id = None
        st.rerun()

    # -------------------- Renomear Conversa --------------------
    st.markdown("### ✏️ Renomear Conversa")
    current_title = st.session_state.chats[selected_id]["title"]
    new_title = st.text_input("Título da conversa", value=current_title, key=f"title_{st.session_state.user_id}_{selected_id}")
    if new_title != current_title:
        st.session_state.chats[selected_id]["title"] = new_title
        save_storage(st.session_state.storage)




# -------------------- Área principal: render e input --------------------
chat = st.session_state.chats[selected_id]
st.header(chat["title"])
history = chat["messages"]

# Render do histórico
for turn in history:
    st.chat_message("user").markdown(turn["user"])
    if "model" in turn:
        st.chat_message("assistant").markdown(turn["model"])
        links = turn.get("links") or []
        if links:
            with st.expander("Jurisprudências citadas"):
                for link in links:
                    st.write(f"- {link}")

# --- Composição da mensagem (texto + anexos) ---
with st.form("compose"):
    user_prompt = st.text_area("Pergunta legal:", height=100, placeholder="Digite sua pergunta...")
    uploaded_files = st.file_uploader(
        "Anexos (PDF, DOCX, TXT, MD)",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        key="uploader_compose"
    )
    include_files = st.checkbox("Incluir anexos nesta mensagem", value=bool(uploaded_files))
    submitted = st.form_submit_button("Enviar")

def extract_text_from_bytes(name: str, mime: str | None, data: bytes) -> str:
    from io import BytesIO
    from pathlib import Path
    ext = Path(name).suffix.lower()

    # TXT / MD / CSV / LOG
    if ext in (".txt", ".md", ".csv", ".log"):
        for enc in ("utf-8", "latin-1"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
        return data.decode(errors="ignore")

    # PDF
    if ext == ".pdf" or (mime and "pdf" in mime):
        from pypdf import PdfReader  # pip install pypdf
        text = []
        reader = PdfReader(BytesIO(data))
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)

    # DOCX
    if ext == ".docx" or (mime and "officedocument.wordprocessingml.document" in mime):
        from docx import Document  # pip install python-docx
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError(f"Formato não suportado: {ext} (mime: {mime})")

def build_attachments_block(files, per_doc_chars=15000, total_chars=45000):
    """Extrai texto dos anexos e retorna um bloco consolidado com cortes de segurança."""
    blocks, total = [], 0
    for f in files:
        raw = f.getvalue()
        txt = extract_text_from_bytes(f.name, f.type, raw)
        txt = txt.strip()
        if not txt:
            continue
        # corta por doc
        txt = txt[:per_doc_chars]
        # respeita teto total
        space_left = total_chars - total
        if space_left <= 0:
            break
        txt = txt[:space_left]
        total += len(txt)
        blocks.append(f"### Anexo: {f.name}\n{txt}")
    if not blocks:
        return ""
    return "\n\n".join(blocks)

if submitted and user_prompt.strip():
    # 1) Renderiza a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(user_prompt)
        if include_files and uploaded_files:
            st.caption(f"{len(uploaded_files)} anexo(s) incluído(s)")

    # 2) Adiciona ao histórico
    entry = {"user": user_prompt}
    if include_files and uploaded_files:
        entry["files"] = [f.name for f in uploaded_files]  # metadados p/ auditoria
    history.append(entry)

    # 3) Monta o contexto (histórico prévio)
    full_context = "\n".join(
        f"User: {t['user']}\n Assistant: {t.get('model','')}".strip()
        for t in history
    )

    # 3.1) Anexa o conteúdo textual dos arquivos desta mensagem (se marcado)
    attachments_text = ""
    if include_files and uploaded_files:
        attachments_text = build_attachments_block(uploaded_files)

    # 3.2) Prompt final enviado ao agente
    prompt_to_agent = full_context
    if attachments_text:
        prompt_to_agent += "\n\n---\n# Documentos enviados nesta mensagem\n" + attachments_text

    # 4) Placeholder p/ resposta
    assistant_box = st.chat_message("assistant")

    # 5) Chamada ao modelo
    with assistant_box:
        with st.spinner("Analisando legislação e buscando jurisprudência…"):
            run_response: TeamRunResponse = IA_DEJUR.run(
                prompt_to_agent, stream=False, show_full_reasoning=False
            )
            resp = run_response.content  # instancia de LegalOutput

        # 6) Mostra resposta
        st.markdown(resp.analysis)
        if getattr(resp, "jurisprudence_links", None):
            st.write("### Jurisprudências citadas")
            for link in resp.jurisprudence_links:
                st.write(f"- {link}")

    # 7) Atualiza histórico
    history[-1]["model"] = resp.analysis
    if getattr(resp, "jurisprudence_links", None):
        history[-1]["links"] = resp.jurisprudence_links

    # 8) Persiste
    st.session_state.chats[selected_id]["messages"] = history
    with open("chats.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.storage, f, ensure_ascii=False, indent=2)

    # 9) Limpa uploader para próxima mensagem (trocando a key)
    if "uploader_seed" not in st.session_state:
        st.session_state.uploader_seed = 0
    st.session_state.uploader_seed += 1
    st.rerun()





