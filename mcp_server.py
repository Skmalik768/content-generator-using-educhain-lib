import asyncio
import json
import sys
import logging
from typing import Any, Dict
from educhain_content import generate_mcqs, generate_lesson_plan, generate_flashcards

# Set up logging to stderr (Claude requirement)
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

class MCPServer:
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if not isinstance(method, str):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "Invalid method field: must be a string"
                }
            }

        if request_id is None and method != "notifications/initialized":
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32600,
                    "message": "Missing request ID"
                }
            }

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "educhain-mcp-server", "version": "1.0.0"}
                    }
                }

            elif method == "notifications/initialized":
                logger.info("Received notifications/initialized")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": None
                }

            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "generate_mcqs",
                                "description": "Generate MCQs for a given topic",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "topic": {"type": "string"},
                                        "count": {"type": "integer", "default": 5},
                                        "difficulty": {"type": "string", "default": "Medium"}
                                    },
                                    "required": ["topic"]
                                }
                            },
                            {
                                "name": "generate_lesson_plan",
                                "description": "Generate a lesson plan for a subject",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "subject": {"type": "string"}
                                    },
                                    "required": ["subject"]
                                }
                            },
                            {
                                "name": "generate_flashcards",
                                "description": "Generate flashcards for a topic",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "topic": {"type": "string"},
                                        "count": {"type": "integer", "default": 5}
                                    },
                                    "required": ["topic"]
                                }
                            }
                        ]
                    }
                }

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name == "generate_mcqs":
                    topic = arguments.get("topic")
                    count = arguments.get("count", 5)
                    difficulty = arguments.get("difficulty", "Medium")
                    result = generate_mcqs(topic, count, difficulty)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                        }
                    }

                elif tool_name == "generate_lesson_plan":
                    subject = arguments.get("subject")
                    result = generate_lesson_plan(subject)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                        }
                    }

                elif tool_name == "generate_flashcards":
                    topic = arguments.get("topic")
                    count = arguments.get("count", 5)
                    result = generate_flashcards(topic, count)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                        }
                    }

                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown method: {method}"
                    }
                }

        except Exception as e:
            logger.error(f"Error: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run(self):
        logger.info("Starting EduChain MCP Server...")
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue

                request = json.loads(line)
                response = await self.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()

            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"}
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break

async def main():
    server = MCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
