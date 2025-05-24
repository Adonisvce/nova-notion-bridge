
from flask import Flask
from notion_client import Client as NotionClient
from logic_engine.plugin_registry import plugin_registry
from logic_engine.plugins.builtin.echo_plugin import EchoPlugin

app = Flask(__name__)
notion = NotionClient(auth="your-secret-notion-token")

@app.route("/test-oauth-route")
def test_oauth():
    return "OAuth route test success!"

plugin_registry.register("echo", EchoPlugin())

@app.route("/")
def index():
    return "Nova OS is running!"
