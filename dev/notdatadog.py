# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import asyncore
import os
import socket
import sys


class AsyncoreSocketUDP2(asyncore.dispatcher):
    def __init__(self, host="127.0.0.1", port=8125, output=True):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Listening on udp {host}:{port}")
        self.bind((host, port))
        self.output = output

    def handle_connect(self):
        print("Server Started...")

    def handle_read(self):
        data = self.recv(8 * 1024)
        if self.output:
            print(data)

    def handle_write(self):
        pass

    def writable(self):
        return False

class AsyncoreSocketUDP(asyncio.DatagramProtocol):
    def __init__(self, output):
        super().__init__()
        self.output = output

    def connection_made(self, transport):
        print("Server Started...")

    def datagram_received(self, data, addr):
        if self.output:
            print(data)
            
async def main(host, port, output):
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(lambda: AsyncoreSocketUDP(output), local_addr=(host, port))
    loop.run_until_complete(t) # Server starts listening
    loop.run_forever()

if __name__ == '__main__':
    try:
        host, port = sys.argv[1].split(":")
        port = int(port)
    except:
        print("Usage: python3 notdatadog.py <host>:<port>")
        sys.exit(1)
    output = os.environ.get("METRICS_OUTPUT", "").lower() == "true"
    asyncio.run(main(host, port, output))

    loop = asyncio.get_running_loop()
    transport, protoco = loop.create_datagram_endpoint(lambda: AsyncoreSocketUDP(output), local_addr=(host, port))
    loop.run_until_complete(t) # Server starts listening
    loop.run_forever()

# if __name__ == "__main__":

#     AsyncoreSocketUDP(
#         host,
#         port,
#         os.environ.get("METRICS_OUTPUT", "").lower() == "true",
#     )
#     asyncore.loop()
