import streamlit as st
import jwt, uuid, datetime, time
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Idura Dashboard")

# Hide the Streamlit header/toolbar and force full width on the iframe
st.markdown("""
    <style>
        #MainMenu, header, footer { display: none !important; }
        .block-container {
            padding: 0 !important;
            margin: 0 auto !important;
            display: flex !important;
            justify-content: center !important;
            max-width: 100% !important;
        }
        .stApp > div:first-child {
            margin-top: 0 !important;
        }
        iframe {
            display: block !important;
            width: 100% !important;
            margin: 0 auto !important;
        }
    </style>
""", unsafe_allow_html=True)

CLIENT_ID    = st.secrets["TABLEAU_CLIENT_ID"]
SECRET_ID    = st.secrets["TABLEAU_SECRET_ID"]
SECRET_VALUE = st.secrets["TABLEAU_SECRET_VALUE"]
USER_EMAIL   = st.secrets["TABLEAU_USER_EMAIL"]

DEVICE = "1920x1080"  # Set the active device to your new config

device_config = {
    "phone":     {"scale": 0.45, "height": 580},
    "ipad":      {"scale": 0.75, "height": 900},
    "laptop13":  {"scale": 0.60, "height": 680},
    "laptop15":  {"scale": 0.72, "height": 820},
    "desktop":   {"scale": 0.67, "height": 950},
    "1920x1080": {"scale": 0.67, "height": 1080},  # New configuration for 1080p
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

# Generate a fresh token on every Streamlit re-run
token = make_token()

html_code = f"""
<script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
<div style="width: 100%; display: flex; justify-content: center; overflow: visible;">
    <div style="width: {round(100/cfg['scale'])}%; transform: scale({cfg['scale']}); transform-origin: top center;">
        <tableau-viz
          src="https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"
          token="{token}"
          toolbar="hidden"
          device="desktop"
          hide-tabs
          style="width: 100%;">
        </tableau-viz>
    </div>
</div>
"""

components.html(html_code, height=cfg["height"], scrolling=False)

# Sleep for 8 minutes, then trigger a proper Streamlit re-run.
# This ensures a fresh JWT is generated before the old one expires (10 min TTL).
time.sleep(480)
st.rerun()
