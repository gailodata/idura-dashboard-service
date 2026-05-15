import jwt, uuid, datetime
from flask import Flask, render_template_string
import os

app = Flask(__name__)

CLIENT_ID   = os.environ.get('TABLEAU_CLIENT_ID')
SECRET_ID   = os.environ.get('TABLEAU_SECRET_ID')
SECRET_VALUE = os.environ.get('TABLEAU_SECRET_VALUE')
USER_EMAIL  = os.environ.get('TABLEAU_USER_EMAIL')

def make_token():
    return jwt.encode(
        {
            "iss": CLIENT_ID,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=9),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": USER_EMAIL,
            "scp": ["tableau:views:embed"],
        },
        SECRET_VALUE,
        algorithm="HS256",
        headers={"kid": SECRET_ID, "iss": CLIENT_ID}
    )

@app.route("/")
def index():
    token = make_token()
    return render_template_string(PAGE, token=token)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* This makes the dashboard fill the entire browser screen */
        body, html { 
            margin: 0; 
            padding: 0; 
            height: 100%; 
            width: 100%;
            overflow: hidden; 
            background-color: #000; 
        }
        tableau-viz { 
            width: 100vw; 
            height: 100vh; 
        }
    </style>
</head>
<body>
    <script type="module" src="https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
    
    <tableau-viz
      id="tab-viz"
      src="https://dub01.online.tableau.com/t/ailo/views/MarComHowWereDoing/MarComHowWereDoing"
      token="{{ token }}"
      toolbar="hidden"
      device="desktop" 
      hide-tabs>
    </tableau-viz>

    <script>
        // Refresh the page every 60 minutes (3600000 ms)
        // This forces Python to generate a brand new security token
        setTimeout(function(){
           window.location.reload();
        }, 3600000); 
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=8080)