sudo ﻿ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/hello.py /etc/gunicorn.d/hello.py
sudo /etc/init.d/nginx restart


