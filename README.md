git clone https://github.com/olezhaku/ServerSturm.git
cd ServerSturm
sudo apt install python3-venv
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd src
python install.py

uvicorn core.asgi:application --host 0.0.0.0 --port 8000
