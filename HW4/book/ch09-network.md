# 第九章：網路程式設計

## 9.1 網路分層模型

網路通訊使用分層模型來組織協定。最常見的是 TCP/IP 四層模型：

```
應用層 (Application)     HTTP, FTP, SMTP, DNS
傳輸層 (Transport)       TCP, UDP
網路層 (Internet)        IP, ICMP
連結層 (Link)            Ethernet, WiFi
```

### 封裝過程

```
應用程式資料
  ↓ [應用層標頭]
傳輸層區段
  ↓ [傳輸層標頭]
網路層封包
  ↓ [網路層標頭]
連結層訊框
  ↓ [連結層標頭]
實體層位元串流
```

## 9.2 Socket 程式設計

Socket（插座）是網路通訊的端點抽象。作業系統透過 Socket API 讓應用程式進行網路通訊。

### TCP 客戶端

```python
import socket

# 建立 Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 連接到伺服器
s.connect(("example.com", 80))

# 發送 HTTP 請求
s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

# 接收回應
data = s.recv(4096)
print(data.decode())

# 關閉連線
s.close()
```

### TCP 伺服器

```python
import socket

# 建立 Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 綁定位址與埠號
server.bind(("0.0.0.0", 8080))

# 開始監聽
server.listen(5)

while True:
    # 接受連線
    client, addr = server.accept()
    print(f"Client connected: {addr}")

    # 接收資料
    data = client.recv(1024)
    print(f"Received: {data.decode()}")

    # 發送回應
    response = b"HTTP/1.1 200 OK\r\n\r\nHello, World!"
    client.send(response)

    # 關閉連線
    client.close()
```

## 9.3 HTTP 協定

HTTP（HyperText Transfer Protocol）是網際網路上最廣泛使用的協定。

### HTTP 請求

```http
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
Connection: close
```

### HTTP 回應

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 125

<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>
```

### 簡易 Web Server 實作

```python
def handle_request(client_socket):
    request = client_socket.recv(4096).decode()
    # 解析請求行
    lines = request.split('\r\n')
    method, path, version = lines[0].split(' ')

    if path == '/':
        body = "<html><body><h1>EasyLang Web Server</h1></body></html>"
    else:
        body = "<html><body><h1>404 Not Found</h1></body></html>"

    response = f"HTTP/1.1 200 OK\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += body

    client_socket.send(response.encode())
    client_socket.close()
```

## 9.4 TCP vs UDP

| 特性 | TCP | UDP |
|------|-----|-----|
| 連線 | 連線導向 | 無連線 |
| 可靠性 | 保證送達 | 不保證 |
| 順序 | 保證順序 | 不保證 |
| 流量控制 | 有 | 無 |
| 速度 | 較慢 | 較快 |
| 用途 | HTTP, FTP, SSH | DNS, 串流, 遊戲 |

## 9.5 簡易 TCP/IP 堆疊

在系統程式課程中，我們可以實作一個簡化的 TCP/IP 堆疊來理解網路協定的運作原理。

### 網路層（IP）

```python
class IPPacket:
    def __init__(self):
        self.version = 4
        self.header_length = 20
        self.total_length = 0
        self.ttl = 64
        self.protocol = 6  # TCP
        self.src_addr = 0
        self.dst_addr = 0
        self.payload = b''

    def pack(self):
        header = struct.pack('!BBHHHBBH4s4s',
            (self.version << 4) | (self.header_length >> 2),
            0, self.total_length, 0, 0,
            self.ttl, self.protocol, 0,
            self.src_addr, self.dst_addr)
        # 計算校驗和
        checksum = self.calculate_checksum(header)
        header = header[:10] + struct.pack('!H', checksum) + header[12:]
        return header + self.payload
```

### 傳輸層（TCP）

```python
class TCPSegment:
    def __init__(self):
        self.src_port = 0
        self.dst_port = 0
        self.seq_num = 0
        self.ack_num = 0
        self.data_offset = 20
        self.flags = 0  # SYN, ACK, FIN, etc.
        self.window_size = 65535
        self.payload = b''

    def pack(self):
        header = struct.pack('!HHIIBBHHH',
            self.src_port, self.dst_port,
            self.seq_num, self.ack_num,
            (self.data_offset >> 2) << 4, self.flags,
            self.window_size, 0, 0)
        return header + self.payload
```

## 9.6 從 Socket 到 Web Server

```
Socket API
    ↓
TCP/UDP 傳輸層
    ↓
IP 網路層
    ↓
Ethernet 連結層
    ↓
實體層

應用程式 ─ socket ─ 作業系統核心 ─ 網路卡 ─ 網路
```

## 練習題

1. 請用 Python 實作一個支援靜態檔案的 HTTP 伺服器
2. 請實作一個簡易的 TCP Client/Server 聊天程式
3. 請使用 Wireshark 觀察 HTTP 請求回應的封包結構

## 本章重點

- TCP/IP 四層模型：應用層、傳輸層、網路層、連結層
- Socket 是網路通訊的端點抽象，提供檔案描述子風格的 API
- TCP 提供可靠、有序的連線服務；UDP 提供快速、無連線服務
- HTTP 是基於 TCP 的應用層協定，使用請求/回應模式
- 實作簡易 TCP/IP 堆疊能深入理解網路協定的運作原理
