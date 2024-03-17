python3.12 -m venv .venv
source ./.venv/bin/activate
pip install pip-tools
bash ./scripts/sync_pip.sh
