import streamlit as st
import jwt
import uuid
import datetime
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Idura Dashboard")

# Remove default Streamlit padding so the viz fills the whole page
st.markdown("""
    <style>
        .stApp { overflow: hidden; }
        #root > div:first-child { height: 100vh; }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
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
<!DOCTYPE html>
<html style="margin:0; padding:0; width:100%; height:100%;">
<head>
    <script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: transparent;
        }}
        tableau-viz {{
            display: block;
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <tableau-viz
      id="tab-viz"
      src="https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"
      token="{token}"
      toolbar="hidden"
      device="default"
      hide-tabs>
    </tableau-viz>
    <script>
        // Resize the viz whenever the iframe itself resizes
        function resizeViz() {{
            const viz = document.getElementById('tab-viz');
            if (viz) {{
                viz.style.width  = window.innerWidth  + 'px';
                viz.style.height = window.innerHeight + 'px';
            }}
        }}
        window.addEventListener('resize', resizeViz);
        resizeViz();

        // Re-auth refresh every 30 mins
        setTimeout(() => window.location.reload(), 1800000);
    </script>
</body>
</html>
"""

# Use scrolling=False (correct param name) and a tall height as fallback
components.html(html_code, height=900, scrolling=False)