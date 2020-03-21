from index import app as DASH_APP

app = DASH_APP.server

if __name__ == "__main__":
    app.run()