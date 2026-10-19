# CENG413 HW-1: Containerized Flask App

1. Clone: `git clone https://github.com/isk-burakkilic/Ceng413-HW1.git && cd Ceng413-HW1`
2. Build (also runs the unit tests): `docker build -t ceng413-hw1:1.0 .`
3. Run (settings from env vars `APP_GREETING`, `APP_NAME`, `APP_VERSION`): `docker run -d --name hw1 -p 8000:8000 -e APP_GREETING=Merhaba -v hw1data:/data ceng413-hw1:1.0`
4. Call it (Windows PowerShell: `curl.exe`): `curl http://localhost:8000/health`, `/info`, `/greet?name=Ada`, `/visit`
5. Stop and remove: `docker rm -f hw1`
