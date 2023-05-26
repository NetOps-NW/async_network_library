
# Async Network Library

## SSH

```python
import asyncio;
from async_network_library import *;

async def main():
    device_details_dict = {
        "jdict":{},
        "rdict":{"host":"10.254.13.254", "known_hosts": None, "username": "adm1n", "password": "", "term_type": "xterm"}
        };
    
    async with async_ssh_library(device_details_dict) as ssh:
        print(await ssh.exec_specific_command("id:$:1"));

if "__main__" in __name__:
    asyncio.run(main());
```

## SCP

```python
import asyncssh;
from async_network_library import *;

async def main():
    device_details_dict = {
        "jdict":{},
        "rdict":{"host":"10.254.13.253", "known_hosts": None, "username": "root", "password": ""}
        };
    async with async_scp_library(device_details_dict) as scp:
        print(await scp.copy_path_from_server("/root", "/home/adm1n", recurse=True));

if "__main__" in __name__:
    asyncio.run(main());
```
