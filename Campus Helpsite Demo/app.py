from ast import Name
from ctypes import _NamedFuncPointer
from os import error
from CampusSite.views import app

if __name__ == "__main__":
    app.run(debug=True, port= 5000)