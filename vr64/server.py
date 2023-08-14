import asyncio
import websockets
import json

Clients = {}

async def handle_client(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            if "Reg1" in data:
                Clients[data["Reg1"]] = websocket
                print(f"{data['Reg1']} Connected")
            if "To1" in data and "Instance1" in data and "Value1" in data:
                if data["To1"] in Clients:
                    for client in Clients:
                        if client == data["To1"]:
                            response = {
                            'Instance1': data["Instance1"],
                            'Value1': data["Value1"],
                            }
                            response_json = json.dumps(response)
                            await Clients[client].send(response_json)
            else:
                response = {
                'Instance1': "Client Not Found",
                }
                response_json = json.dumps(response)
                await websocket.send(response_json)
        except json.JSONDecodeError:
            print("Invalid JSON format")
        except KeyError as e:
            print(f"Missing key in JSON: {e}")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
