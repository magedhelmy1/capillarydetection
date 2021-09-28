try:
    print("Trying import production.py settings...")
    from .production import *
except ImportError:
    print("Trying import development.py settings...")
    from .settings import *