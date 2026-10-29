# ILIK-GECE-YAYIN zinciri: ucretsiz_3d.py --kuyruk bitince ilik_yayin.py (Gorev Zamanlayici 'ucretsiz3d-kuyruk' bunu calistirir)
import os, sys, subprocess
d = os.path.dirname(os.path.abspath(__file__)); env = dict(os.environ)
subprocess.run([sys.executable, os.path.join(d, 'ucretsiz_3d.py'), '--kuyruk'], env=env, timeout=6 * 3600)
subprocess.run([sys.executable, os.path.join(d, 'ilik_yayin.py')], env=env, timeout=3600)
