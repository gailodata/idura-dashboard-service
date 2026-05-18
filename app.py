import streamlit as st
import jwt, uuid, datetime
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Idura Dashboard")

# Hide the Streamlit header/toolbar and kill all padding
st.markdown("""
    <style>
        #MainMenu, header, footer { display: none !important; }
        .block-container {
            padding: 0 !important;
            margin: 0 auto !important;
            display: flex !important;
            justify-content: center !important;
        }
        .stApp > div:first-child {
            margin-top: 0 !important;
        }
        /* Target the iframe Streamlit creates for components.html */
        iframe {
            display: block !important;
            margin: 0 auto !important;
        }
    </style>
""", unsafe_allow_html=True)

CLIENT_ID    = st.secrets["TABLEAU_CLIENT_ID"]
SECRET_ID    = st.secrets["TABLEAU_SECRET_ID"]
SECRET_VALUE = st.secrets["TABLEAU_SECRET_VALUE"]
USER_EMAIL   = st.secrets["TABLEAU_USER_EMAIL"]

DEVICE = "laptop15"

device_config = {
    "phone":    {"scale": 0.45, "height": 580},
    "ipad":     {"scale": 0.75, "height": 900},
    "laptop13": {"scale": 0.60, "height": 680},
    "laptop15": {"scale": 0.90, "height": 980},  # bumped up from 0.72
    "desktop":  {"scale": 1.00, "height": 980},
}
cfg = device_config[DEVICE]

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
  style="width:{round(100/cfg['scale'])}%; transform:scale({cfg['scale']}); transform-origin:top center; display:block; margin:0 auto;">
</tableau-viz>
<script>setTimeout(() => window.location.reload(), 480000);</script>
"""

components.html(html_code, height=cfg["height"], scrolling=False)