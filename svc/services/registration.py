import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread, Event

from svc.models.registration import RegistrationData
from svc.utilities.file_utils import save_hub_info


class _RegistrationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/register':
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))

            data = RegistrationData.from_dict(body)
            save_hub_info(data)
            self.server.registration_complete.set()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def wait_for_registration(port, timeout=None):
    server = HTTPServer(('', port), _RegistrationHandler)
    server.registration_complete = Event()

    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    server.registration_complete.wait(timeout=timeout)

    server.shutdown()
    server_thread.join()
