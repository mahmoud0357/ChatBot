import random
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from querymancer.agent import ask, create_history
from querymancer.config import Config
from querymancer.models import create_llm
from querymancer.tools import get_available_tools, with_sql_cursor

load_dotenv()

LOADING_MESSAGES = [
    "Consulting the ancient tomes of SQL wisdom...",
    "Casting query spells on your database...",
    "Summoning data from the digital realms...",
    "Deciphering your request into database runes...",
    "Brewing a potion of perfect query syntax...",
    "Channeling the power of database magic...",
    "Translating your words into the language of tables...",
    "Waving my SQL wand to fetch your results...",
    "Performing database divination...",
    "Aligning the database stars for optimal results...",
    "Consulting with the database spirits...",
    "Transforming natural language into database incantations...",
    "Peering into the crystal ball of your database...",
    "Opening a portal to your data dimension...",
    "Enchanting your request with SQL optimization...",
    "Invoking the ancient art of query completion...",
    "Reading between the tables to find your answer...",
    "Conjuring insights from your database depths...",
    "Weaving a tapestry of joins and filters...",
    "Preparing a feast of data for your consideration...",
]

@st.cache_resource(show_spinner=False)
def get_model() -> BaseChatModel:
    llm = create_llm(Config.MODEL)
    try:
        llm = llm.bind_tools(get_available_tools())
    except NotImplementedError:
        pass
    return llm

def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="ChatBot for SQLite",
    page_icon="🧙‍♂️",
    layout="centered",
    initial_sidebar_state="expanded",
)

load_css("assets/style.css")
st.markdown(
    """
    <style>
        .stChatMessage {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .stChatMessage.user {
            background-color: #e0f7fa;
            color: #006064;
        }
        .stChatMessage.ai {
            background-color: #e8f5e9;
            color: #1b5e20;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 10px;'>
        <h1 style='font-size: 3rem; margin-bottom: 0;'>🤖 ChatBot</h1>
        <p style='font-size: 1.2rem; color: #374151; margin-top: 0;'>Talk to your database using natural language</p>
        <div style='color:gray; font-size:14px; margin-top:-5px;'>
            Created by <b>EYouth Bootcamp - TEAM 20</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.write("# Database Information")
    st.write(f"**File:** {Config.Path.DATABASE_PATH.relative_to(Config.Path.APP_HOME)}")
    db_size = Config.Path.DATABASE_PATH.stat().st_size / (1024 * 1024)
    st.write(f"**Size:** {db_size:.2f} MB")

    with with_sql_cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        )
        tables = [row[0] for row in cursor.fetchall()]
        st.write("**Tables:**")
        for table in tables:
            cursor.execute(f"SELECT count(*) FROM {table};")
            count = cursor.fetchone()[0]
            with st.expander(f"📄 {table} ({count} rows)"):
                if count > 0:
                    limit = min(5, count)
                    cursor.execute(f"SELECT * FROM {table} LIMIT {limit};")
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df, use_container_width=True)

    if st.button("🔄 Reset Chat"):
        st.session_state.messages = create_history()
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = create_history()

for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        continue

    is_user = isinstance(message, HumanMessage)
    role = "user" if is_user else "ai"
    avatar = "🧙‍♂️" if is_user else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(
            f'<div class="stChatMessage {role}">{message.content}</div>',
            unsafe_allow_html=True
        )

if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user", avatar="🧙‍♂️"):
        st.session_state.messages.append(HumanMessage(prompt))
        st.markdown(
            f'<div class="stChatMessage user">{prompt}</div>',
            unsafe_allow_html=True
        )

    with st.chat_message("ai", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state="running")

        response = ask(prompt, st.session_state.messages, get_model())
        message_placeholder.markdown(
            f'<div class="stChatMessage ai">{response}</div>',
            unsafe_allow_html=True
        )
        st.session_state.messages.append(AIMessage(response))
