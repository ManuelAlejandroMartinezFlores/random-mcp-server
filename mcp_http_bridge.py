#!/usr/bin/env python3
import json
import sys
import requests

class MCPHTTPBridge:
    def __init__(self, url):
        self.url = url
        self.request_id = 1
        
    def run(self):
        """Main loop to read from stdin and write to stdout"""
        while True:
            try:
                # Read line from stdin
                line = sys.stdin.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                    
                # Parse the JSON-RPC request
                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    self.send_error(None, -32700, "Parse error")
                    continue
                
                # Forward to HTTP server
                self.forward_request(request)
                
            except Exception as e:
                self.send_error(None, -32603, f"Internal error: {str(e)}")
    
    def forward_request(self, request):
        """Forward the request to HTTP server and handle response"""
        try:
            response = requests.post(
                self.url,
                headers={"Content-Type": "application/json"},
                json=request,
                timeout=30
            )
            response.raise_for_status()
            
            # Write the response back to stdout
            print(response.text, flush=True)
            
        except requests.exceptions.RequestException as e:
            self.send_error(request.get('id'), -32000, f"HTTP error: {str(e)}")
        except Exception as e:
            self.send_error(request.get('id'), -32603, f"Unexpected error: {str(e)}")
    
    def send_error(self, request_id, code, message):
        """Send JSON-RPC error response"""
        error_response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python3 mcp_http_bridge.py <url>', file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    bridge = MCPHTTPBridge(url)
    bridge.run()