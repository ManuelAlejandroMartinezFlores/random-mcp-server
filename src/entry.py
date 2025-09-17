# File: src/entry.py - Simplified Cloudflare Workers Version
from workers import Response
import json
import random

async def on_fetch(request, env):
    """Simplified MCP server for random number generation"""
    
    # Handle CORS
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Content-Type": "application/json"
    }
    
    if request.method == "OPTIONS":
        return Response("", headers=cors_headers)
    
    try:
        if request.method == "GET":
            # Health check
            result = {
                "status": "healthy",
                "server": "Random Number MCP Server",
                "version": "1.0.0"
            }
            return Response(json.dumps(result), headers=cors_headers)
        
        if request.method == "POST":
            # Parse JSON request
            request_text = await request.text()
            data = json.loads(request_text)
            
            method = data.get("method", "")
            request_id = data.get("id", 1)
            
            if method == "initialize":
                # MCP Initialize
                result = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "random-number-server",
                            "version": "1.0.0"
                        }
                    }
                }
                return Response(json.dumps(result), headers=cors_headers)
            
            elif method == "tools/list" or method == "notifications/initialized":
                # List available tools
                tools = [
                    {
                        "name": "random_int",
                        "description": "Generate random integer between min and max (inclusive)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "min": {"type": "integer", "default": 1},
                                "max": {"type": "integer", "default": 100}
                            }
                        }
                    },
                    {
                        "name": "random_float", 
                        "description": "Generate random float between min and max",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "min": {"type": "number", "default": 0.0},
                                "max": {"type": "number", "default": 1.0},
                                "precision": {"type": "integer", "default": 2}
                            }
                        }
                    },
                    {
                        "name": "random_choice",
                        "description": "Pick random item(s) from a list",
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "choices": {"type": "array", "items": {"type": "string"}},
                                "count": {"type": "integer", "default": 1}
                            },
                            "required": ["choices"]
                        }
                    }
                ]
                
                result = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools}
                }
                return Response(json.dumps(result), headers=cors_headers)
            
            elif method == "tools/call":
                # Execute tool
                params = data.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                try:
                    if tool_name == "random_int":
                        min_val = arguments.get("min", 1)
                        max_val = arguments.get("max", 100)
                        result_val = random.randint(min_val, max_val)
                        text_result = f"Random integer between {min_val} and {max_val}: {result_val}"
                    
                    elif tool_name == "random_float":
                        min_val = float(arguments.get("min", 0.0))
                        max_val = float(arguments.get("max", 1.0))
                        precision = int(arguments.get("precision", 2))
                        result_val = round(random.uniform(min_val, max_val), precision)
                        text_result = f"Random float between {min_val} and {max_val}: {result_val}"
                    
                    elif tool_name == "random_choice":
                        choices = arguments.get("choices", [])
                        count = int(arguments.get("count", 1))
                        
                        if not choices:
                            raise ValueError("Choices cannot be empty")
                        
                        if count == 1:
                            result_val = random.choice(choices)
                            text_result = f"Random choice: {result_val}"
                        else:
                            if count > len(choices):
                                count = len(choices)
                            result_val = random.sample(choices, count)
                            text_result = f"Random choices: {', '.join(result_val)}"
                    
                    else:
                        raise ValueError(f"Unknown tool: {tool_name}")
                    
                    result = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": text_result}]
                        }
                    }
                    return Response(json.dumps(result), headers=cors_headers)
                
                except Exception as e:
                    error_result = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32000,
                            "message": f"Tool execution failed: {str(e)}"
                        }
                    }
                    return Response(json.dumps(error_result), status=400, headers=cors_headers)
            
            else:
                # Unknown method
                error_result = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                return Response(json.dumps(error_result), status=400, headers=cors_headers)
        
        # Method not allowed
        error_result = {"error": f"Method {request.method} not allowed"}
        return Response(json.dumps(error_result), status=405, headers=cors_headers)
    
    except json.JSONDecodeError as e:
        error_result = {"error": f"Invalid JSON: {str(e)}"}
        return Response(json.dumps(error_result), status=400, headers=cors_headers)
    
    except Exception as e:
        error_result = {"error": f"Server error: {str(e)}"}
        return Response(json.dumps(error_result), status=500, headers=cors_headers)