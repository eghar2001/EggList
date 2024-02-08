from eggList import create_app
from waitress import serve
app = create_app()

if __name__ == "__main__":
    serve(app,url_scheme = "https", port=8080)