# Wireguard example setup
A simple wireguard setup with a server and two clients

This is just a reference for myself in case I need to setup wireguard again.

# Key generation
To generate the keys for the server and the clients, use the following command:
```bash
wg genkey | tee privatekey | wg pubkey > publickey

# Or in two steps:
wg genkey > privatekey
wg pubkey < privatekey > publickey
```
This generates a privatekey and a publickey file.
Every peer should have its own `privatekey` and `publickey` file - so every peer should run this command.
The `privatekey` file should be kept secret and only the `publickey` should be shared
with the server or the client respectively.


# Creating the wireguard tunnel
`wg-quick` is a simple script for easily bringing up a WireGuard interface.
```bash
Server:
wg-quick up ~/wg/server.conf

Client A:
wg-quick up ~/wg/client_a.conf

Client B:
wg-quick up ~/wg/client_b.conf


Note: The filename determines the tunnel interface name.
```

Use 
`sudo wg status` to see the status of the wireguard interfaces.
