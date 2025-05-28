git clone https://github.com/olezhaku/ServerSturm.git
cd ServerSturm
chmod +x install.sh
./install.sh

uvicorn core.asgi:application --host 0.0.0.0 --port 8000
