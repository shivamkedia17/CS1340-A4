# CS1340-A3

## Socket Programming

**Usage**: Python version >= 3.10 required.

0. Make sure you are in `A3/`
1. For the *server-side* run:
    ```bash
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 server.py
    ```
2. For *each client*, open another terminal, and run:
    ```bash
    python3 client.py
    ```

Note:
+ Type `greet` to show Menu
+ Type `close` to disconnect client
+ Type `Ctrl-c` for graceful server shutdown.
+ You can simultaneously open upto 4 others before connections are refused.
+ The server is single-threaded, which means only 1 connection will be actively served. The rest have to wait.
+ If you try to re-run the server immediately after shutting it down, you may get:
    ```
        OSError: Address already in use.
    ```
    This is because `SO_REUSEADDR` has been set to `False`.
