import os
# import quart
from Quart_Authorization_Discord import DiscordOauth2Client
from quart import Quart, redirect, url_for, render_template


app = Quart(__name__)
# ipcClient = ipc.Server(secret_key="Swas")

app.secret_key = os.environ['SESSION']
app.config['DISCORD_CLIENT_ID'] = os.environ['CLIENT_ID']
app.config['DISCORD_CLIENT_SECRET'] = os.environ['CLIENT_SECRET']
app.config['SCOPES'] = ['identify', 'guilds', "email"]
app.config['DISCORD_REDIRECT_URI'] = os.environ['URI']
app.config['DISCORD_BOT_TOKEN'] = os.environ['BOT_TOKEN']

client = DiscordOauth2Client(app)


@app.route("/")
async def index():
    return await render_template("index.html", logged=client.is_logged())

@app.route("/login")
async def login():
    return await client.create_session()


@app.route("/logout")
async def logout():
    await client.logout()
    return redirect(url_for("index"))

@app.route("/callback")
async def callback():
    await client.callback()
    return redirect(url_for("dashboard"))




@app.route("/dashboard")
@client.is_logged_in
async def dashboard():
    User = await client.fetch_user()
    return await render_template("dashboard.html", user=User)



@app.errorhandler(401)
async def handle_unathorized(e):
    return redirect(url_for("login"))
    return {"code": 401, "error": str(e)}

@app.errorhandler(404)
async def handle_404(e):
    return await render_template("404-page.html")
    return {"code": 404, "error": str(e)}

