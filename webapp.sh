#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" >> tempdir/Dockerfile

echo "RUN pip install flask" >> tempdir/Dockerfile
echo "RUN pip install flask_bootstrap" >> tempdir/Dockerfile
echo "RUN pip install flask_wtf" >> tempdir/Dockerfile
echo "RUN pip install flask_sqlalchemy" >> tempdir/Dockerfile
echo "RUN pip install flask_login" >> tempdir/Dockerfile
echo "RUN pip install email_validator" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  app.py /home/myapp/" >> tempdir/Dockerfile
echo "COPY  database.db /home/myapp/" >> tempdir/Dockerfile

echo "EXPOSE 5000" >> tempdir/Dockerfile

echo "CMD python3 /home/myapp/app.py" >> tempdir/Dockerfile

cd tempdir

docker build -t webapp .

docker run -t -d -p 5000:5000 --name webrunning webapp

docker ps -a