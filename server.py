import threading
import socket
import json
import traceback
import bpy

class BlenderMCPServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.server_thread = None

    def start(self):
        if self.running:
            print("Server is already running")
            return
        self.running = True
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()
            print(f"BlenderMCP server started on {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to start server: {str(e)}")
            self.stop()

    def stop(self):
        self.running = False
        if self.socket:
            try: self.socket.close()
            except: pass
            self.socket = None
        if self.server_thread:
            try:
                if self.server_thread.is_alive():
                    self.server_thread.join(timeout=1.0)
            except: pass
            self.server_thread = None
        print("BlenderMCP server stopped")

    def _server_loop(self):
        self.socket.settimeout(1.0)
        while self.running:
            try:
                try:
                    client, address = self.socket.accept()
                    threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()
                except socket.timeout:
                    continue
            except Exception as e:
                print(f"Error in server loop: {str(e)}")
                if not self.running:
                    break

    def _handle_client(self, client):
        client.settimeout(None)
        buffer = b''
        try:
            while self.running:
                try:
                    data = client.recv(8192)
                    if not data: break
                    buffer += data
                    try:
                        command = json.loads(buffer.decode('utf-8'))
                        buffer = b''
                        def execute_wrapper():
                            try:
                                from .handlers import dispatcher
                                response = dispatcher.handle_command(command)
                                client.sendall(json.dumps(response).encode('utf-8'))
                            except Exception as e:
                                traceback.print_exc()
                                error_response = {"status": "error", "message": str(e)}
                                try: client.sendall(json.dumps(error_response).encode('utf-8'))
                                except: pass
                        bpy.app.timers.register(execute_wrapper, first_interval=0.0)
                    except json.JSONDecodeError:
                        pass
                except Exception as e:
                    print(f"Error receiving data: {str(e)}")
                    break
        finally:
            try: client.close()
            except: pass

def register_server():
    bpy.types.Scene.blendermcp_server = BlenderMCPServer(port=bpy.context.scene.blendermcp_port)
    bpy.types.Scene.blendermcp_server.start()
    bpy.context.scene.blendermcp_server_running = True

def unregister_server():
    if hasattr(bpy.types.Scene, 'blendermcp_server'):
        bpy.types.Scene.blendermcp_server.stop()
        del bpy.types.Scene.blendermcp_server
    bpy.context.scene.blendermcp_server_running = False
