import streamlit as st
import jwt
import uuid
import datetime
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Idura Dashboard")

# Remove Streamlit's default top padding
st.markdown("""
    <style>
        .block-container { padding-top: 0 !important; }
    </style>
""", unsafe_allow_html=True)

CLIENT_ID = st.secrets["TABLEAU_CLIENT_ID"]
SECRET_ID = st.secrets["TABLEAU_SECRET_ID"]
SECRET_VALUE = st.secrets["TABLEAU_SECRET_VALUE"]
USER_EMAIL = st.secrets["TABLEAU_USER_EMAIL"]

def make_token():
    return jwt.encode(
        {
            "iss": CLIENT_ID,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": USER_EMAIL,
            "scp": ["tableau:views:embed"],
        },
        SECRET_VALUE,
        algorithm="HS256",
        headers={"kid": SECRET_ID, "iss": CLIENT_ID}
    )

token = make_token()

html_code = f"""
<script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
<tableau-viz
  src="https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"
  token="{token}"
  toolbar="hidden"
  device="desktop"
  hide-tabs
  style="width:100%; height:100vh;">
</tableau-viz>
<script>
    setTimeout(() => window.location.reload(), 1800000);
</script>
"""

components.html(html_code, height=1080, scrolling=False)