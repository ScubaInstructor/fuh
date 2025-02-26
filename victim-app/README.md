# Minimal Victim App
This is a minimal Application to perform a Brute Force Attack against.

start this app with `docker-compose up` and navigate to (http://localhost:9999) to check its functionality

Hardcoded credentials are `admin:password123`.

You can attack its loginform with hydra and rockyou.txt using this command:
`hydra -l user -P rockyou.txt <IPADRESS> -s 9999 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials" -V`



See [rockyou website](https://github.com/dw0rsec/rockyou.txt) for informations about and download of rockyou.txt.

See [hydra website](https://www.kali.org/tools/hydra/) for more information on hydra.
