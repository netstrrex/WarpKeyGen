# WarpKeyGen
A simple async license key generator for warp vpn!😎

# Dependencies⚙️
- Python 3.9+
- aiohttp (`pip install aiohttp`)

# How to use it🤔
```python
from aiohttp import ClientSession
from warp import WarpKeyGenerator

async def main():
    async with ClientSession() as session:
        key_gen = WarpKeyGenerator(session)
        print(await key_gen.generate_key())
```

# Result✅
<img src="https://sun9-west.userapi.com/sun9-13/s/v1/ig2/EiF_ZdIgDjrrj9CG3PYIuL6v4Wd7AIDMbk6C0J9N3dDcC_nJzsiYBcOYdQWuaB56lbPg5So6gsH7jLtaY9jq_7ur.jpg?size=1080x1870&quality=96&type=album" width="300">
