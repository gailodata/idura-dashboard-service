import streamlit as st
import jwt
import uuid
import datetime
import streamlit.components.v1 as components

# 1. Setup the Page (Wide mode for big screens)
st.set_page_config(layout="wide", page_title="Idura Dashboard")

# 2. Get your Secrets from the Streamlit "Vault"
# We will set these up in the Streamlit Cloud Dashboard next
CLIENT_ID = st.secrets["TABLEAU_CLIENT_ID"]
SECRET_ID = st.secrets["TABLEAU_SECRET_ID"]
SECRET_VALUE = st.secrets["TABLEAU_SECRET_VALUE"]
USER_EMAIL = st.secrets["TABLEAU_USER_EMAIL"]

# 3. Function to generate the Security Token
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

# 4. Create the Dashboard HTML
token = make_token()

html_code = f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:black;">
    <script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
    
    <tableau-viz
      id="tab-viz"
      src="https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"
      token="{token}"
      toolbar="hidden"
      device="desktop" 
      hide-tabs
      style="width:100vw; height:98vh;">
    </tableau-viz>

    <script>
        // Auto-refresh every 30 mins to get a fresh token
        setTimeout(function(){{ window.location.reload(); }}, 1800000); 
    </script>
</body>
</html>
"""

# 5. Render the dashboard
components.html(html_code, height=1000)