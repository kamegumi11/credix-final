import sys
import subprocess

subprocess.run([sys.executable, "datapipeline/application_features.py"])
subprocess.run([sys.executable, "datapipeline/bureau_features.py"])
subprocess.run([sys.executable, "datapipeline/generate_abt.py"])
subprocess.run([sys.executable, "model/train.py"])