from flask import Blueprint, redirect
import os

oauth_bp = Blueprint("oauth", __name__, url_prefix="/oauth")

@oauth_bp.route("/start", methods=["GET"])
def start_oauth():
    client_id = os.getenv("NOTION_CLIENT_ID")
    redirect_uri = os.getenv("NOTION_REDIRECT_URI", "https://nova.novaaisecurity.com/oauth/callback")

    auth_url = (
        "https://api.notion.com/v1/oauth/authorize"
        f"?owner=user&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        "&response_type=code"
    )
    return redirect(auth_url)

