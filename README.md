# mokachan

A simple HTTP tarpit server, modified from <https://nullprogram.com/blog/2019/03/22/>.

*Mo\~ka\~chan is very\~fast at send\~ing H\~T\~T\~P res\~ponse!*

## Usage

It accepts two environment variables:

- `HOST`: The address to bind to. Default: `127.0.0.1`
- `PORT`: The port to bind to. Default: `6571`

## Installation

### Systemd

Requires a Python 3 installation. No extra dependencies.

```sh
install -Dm644 mokachan.service /etc/systemd/system/mokachan.service
install -Dm755 mokachan.py /usr/local/bin/mokachan.py
systemctl daemon-reload
systemctl enable --now mokachan
```

You might need to adjust `IPAddressDeny` and `IPAddressAllow` in the service file.

### Docker

```sh
docker compose up -d
```
