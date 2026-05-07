from importlib import import_module

app = import_module('app.main').app

for r in app.routes:
    print(r.path, list(r.methods))
