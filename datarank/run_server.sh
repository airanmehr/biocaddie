/etc/init.d/nginx start
cd /home/arya/workspace/biocaddie/datarank
uwsgi --socket /tmp/test.sock --wsgi-file web/wsgi.py --chmod-socket=666 &