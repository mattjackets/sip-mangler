# sip-mangler
Minimalistic UDP proxy with SIP header injection

# Usage

## Configureation
Set the target IP/port as well as the header you wish to inject.  Currently, the proxy only injects headers into SIP INVITE messages.

```
# Remote (SIP) server ip/port
TARGET_SIP_IP = "172.16.0.0"  # Replace with actual SIP server IP
TARGET_SIP_PORT = 5060

# Header to be inserted into INVITE message
X_FOO_HEADER = "X-Foo: custom-value"
```

## Running
Once configured, execute sip-mang.py.  Once running, configure your soft phone to point to 127.0.0.1 port 5060 (UDP) rather than the actual SIP server/proxy.  If successful, you should see activity from sip-mang.py and your softphone should register successfully.
