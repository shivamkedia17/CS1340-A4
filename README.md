# CS1340-A3

## Socket Programming

**Usage**:

0. Make sure you are in `A3/`
1. For the *server-side* run:
    ```bash
    source .venv/bin/activate
    python3 server.py
    ```
2. For *each client*, open another terminal, and run:
    ```bash
    python3 client.py
    ```

Note:
+ You can simultaneously open upto 4 others before connections are refused.
+ The server is single-threaded, which means only 1 connection will be actively served. The rest have to wait.