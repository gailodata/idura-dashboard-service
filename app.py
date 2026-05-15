import streamlit as st
import jwt
import uuid
import datetime
import streamlit.components.v1 as components

# Set page to wide mode for the big screen
st.set_page_config(layout="wide")

# 1. Pull secrets from Streamlit's "Secrets" manager (we set this up in Step 4)
CLIENT_ID = st.secrets["TABLEAU_CLIENT_ID"]
SECRET_ID = st.secrets["TABLEAU_SECRET_ID"]
SECRET_VALUE = st.secrets["TABLEAU_SECRET_VALUE"]
USER_EMAIL = st.secrets["TABLEAU_USER_EMAIL"]

# 2. Generate the Token
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

# 3. The HTML for the big screen
# Note the JS refresh script at the bottom to keep it "infinite"
html_code = f"""
<script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
<tableau-viz 
    id="tab-viz" 
    src="https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"
    token="{token}" 
    toolbar="hidden" 
    device="desktop" 
    style="width:100vw; height:95vh;">
</tableau-viz>
<script>
    setTimeout(function(){{ window.location.reload(); }}, 1800000); 
</script>
"""

# 4. Display it
components.html(html_code, height=1000)