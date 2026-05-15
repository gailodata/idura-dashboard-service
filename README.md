# idura-dashboard-service

---

## Phase 1: The Tableau 

You need these 5 things from the Tableau Cloud interface to make the security handshake work.

1. **Site URI:** Log in and look at your URL. Grab the text after `/site/`.
2. **Connected App:** Go to **Settings > Connected Apps > New Connected App (Direct Trust)**.


3. **Client ID:** Copy this from the Connected App page.
4. **Secret ID & Value:** Click "Generate New Secret." **Copy the Secret Value immediately**
5. **Enable:** Click the "Actions" button and select **Enable**. (It won't work if it's still 'Disabled').

---

## Phase 2: Local Setup 


### 1. Create your folder

Create a folder on your desktop named `idura-dashboard`. Inside, create two files:

**File 1: `requirements.txt**` (Check the spelling!)

```text
streamlit
pyjwt

```

**File 2: `app.py**`

```python
import streamlit as st
import jwt
import uuid
import datetime
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
# For local testing, you can paste your strings here. 
# We will move these to "Secrets" in the next phase.
CLIENT_ID = "YOUR_CLIENT_ID"
SECRET_ID = "YOUR_SECRET_ID"
SECRET_VALUE = "YOUR_SECRET_VALUE"
USER_EMAIL = "your-email@company.com"

# TRANSFORM YOUR URL HERE:
# Before: https://dub01.online.tableau.com/#/site/ailo/views/MarComHowWereDoing/MarComHowWereDoing
# After:  https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing
DASHBOARD_URL = "https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"

# --- 2. THE SECURITY HANDSHAKE ---
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

# --- 3. THE FRONTEND ---
st.set_page_config(layout="wide", page_title="Idura Pulse")
st.title("📊 Idura Pulse") # This is the "Great Name" for the screen

token = make_token()

html_code = f"""
<script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
<tableau-viz 
    id="tab-viz" 
    src="{DASHBOARD_URL}"
    token="{token}" 
    toolbar="hidden" 
    device="desktop" 
    style="width:100vw; height:90vh;">
</tableau-viz>
<script>
    // Self-refresh every 30 mins to keep it infinite
    setTimeout(function(){{ window.location.reload(); }}, 1800000); 
</script>
"""

components.html(html_code, height=900)

```

### 2. Run it locally

Open your terminal in that folder and run:

1. `pip install streamlit pyjwt`
2. `streamlit run app.py`

---

## Phase 3: The Web

Once you see the dashboard working on `localhost`, it’s time to put it in the cloud so you can use it for the company.

### 1. GitHub (The Storage)

1. Create a **New Private Repository** on GitHub.
2. Upload `app.py` and `requirements.txt`.

### 2. Streamlit Cloud (The Host)

1. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub.
2. Deploy the repo you just made.
3. **Crucial Step:** Go to the app's **Settings > Secrets** and paste your IDs and Secrets there:
```toml
TABLEAU_CLIENT_ID = "..."
TABLEAU_SECRET_ID = "..."
TABLEAU_SECRET_VALUE = "..."
TABLEAU_USER_EMAIL = "..."

```


4. Update your `app.py` code to use `st.secrets["TABLEAU_CLIENT_ID"]` instead of hardcoded strings (this keeps the company's data safe!).

### 3. The Big Screen

1. Open the browser on the office TV.
2. Type in your new Streamlit URL (e.g., `https://idura-pulse.streamlit.app`).
3. **F11** for full screen.

