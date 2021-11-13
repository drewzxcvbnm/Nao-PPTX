import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="IP address for NAO", required=True)
parser.add_argument("--pr", help="Path of presentation (full path)", default="naoPPTX.pptx")
parser.add_argument("--no-inet", help="Disable use of external services", action='store_true')
ARGS = parser.parse_args()
