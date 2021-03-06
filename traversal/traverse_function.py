import hashlib
import requests
import time
import sys
import json
from decouple import config
from visited_rooms import visited_rooms

if __name__ == '__main__':
    node = "https://lambda-treasure-hunt.herokuapp.com/api"
    headers = {"Authorization": config('API_KEY')}

    def moving_function(direction, room_id=None):
        if room_id is None:
            data = {"direction": direction}
            r = requests.post(url=node + "/adv/move",
                              json=data, headers=headers)
            try:
                result = r.json()
                print("cooldown", r.json()["cooldown"])
                time.sleep(r.json()["cooldown"])
                return result
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(r)

        else:
            data = {"direction": direction, "next_room_id": str(room_id)}
            r = requests.post(url=node + "/adv/move",
                              json=data, headers=headers)
            print("data", data)
            try:
                result = r.json()
                print("cooldown", r.json()["cooldown"])
                time.sleep(r.json()["cooldown"])
                return result
            except ValueError:
                print("Error:  Non-json response")
                print("next_room_id Response returned:")
                print(r)

    def pick_up_function(treasure):
        data = {"name": treasure}
        r = requests.post(url=node + "/adv/take", json=data, headers=headers)
        try:
            result = r.json()
            time.sleep(r.json()["cooldown"])
            return result
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)

    def get_player_status_function():
        r = requests.post(url=node + "/adv/status", headers=headers)
        try:
            result = r.json()
            time.sleep(r.json()["cooldown"])
            return result
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)

    r = requests.get(url=node + "/adv/init", headers=headers)
    try:
        starting_room = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
    cooldown = starting_room["cooldown"]
    print("cooldown ", cooldown)
    time.sleep(cooldown)

    player = get_player_status_function()
    print("player status", player)

    stack = []
    stack.append(starting_room)
    print("start", stack)
    while len(stack) > 0:
        if len(visited_rooms) == 500:
            print('You visited 500 rooms!')
            break
        room = stack.pop()

        if str(room["room_id"]) not in visited_rooms:
            print("stack", room["room_id"])
            print("room visited", len(visited_rooms))
            visited_rooms[str(room["room_id"])] = dict()

            for d in room["exits"]:
                visited_rooms[str(room["room_id"])][d] = "?"

        if "w" in visited_rooms[str(room["room_id"])] and visited_rooms[str(room["room_id"])]["w"] == "?":
            room_w_to = moving_function("w")

            stack.append(room_w_to)
            visited_rooms[str(room["room_id"])]["w"] = room_w_to["room_id"]
            if room_w_to["room_id"] not in visited_rooms:
                print("room visited", len(visited_rooms))

                visited_rooms[room_w_to["room_id"]] = dict()
                for d in room_w_to["exits"]:
                    visited_rooms[room_w_to["room_id"]][d] = "?"
                visited_rooms[room_w_to["room_id"]]["e"] = room["room_id"]
            else:
                visited_rooms[room_w_to["room_id"]]["e"] = room["room_id"]

        elif "e" in visited_rooms[str(room["room_id"])] and visited_rooms[str(room["room_id"])]["e"] == "?":
            room_e_to = moving_function("e")

            stack.append(room_e_to)
            visited_rooms[str(room["room_id"])]["e"] = room_e_to["room_id"]
            if room_e_to["room_id"] not in visited_rooms:
                print("room visited", len(visited_rooms))
                visited_rooms[room_e_to["room_id"]] = dict()
                for d in room_e_to["exits"]:
                    visited_rooms[room_e_to["room_id"]][d] = "?"
                visited_rooms[room_e_to["room_id"]]["w"] = room["room_id"]
            else:
                visited_rooms[room_e_to["room_id"]]["w"] = room["room_id"]

        elif "n" in visited_rooms[str(room["room_id"])] and visited_rooms[str(room["room_id"])]["n"] == "?":
            room_n_to = moving_function("n")

            stack.append(room_n_to)
            visited_rooms[str(room["room_id"])]["n"] = room_n_to["room_id"]
            if room_n_to["room_id"] not in visited_rooms:
                print("room visited", len(visited_rooms))
                visited_rooms[room_n_to["room_id"]] = dict()
                for d in room_n_to["exits"]:
                    visited_rooms[room_n_to["room_id"]][d] = "?"
                visited_rooms[room_n_to["room_id"]]["s"] = room["room_id"]
            else:
                visited_rooms[room_n_to["room_id"]]["s"] = room["room_id"]

        elif "s" in visited_rooms[str(room["room_id"])] and visited_rooms[str(room["room_id"])]["s"] == "?":
            room_s_to = moving_function("s")

            stack.append(room_s_to)
            visited_rooms[str(room["room_id"])]["s"] = room_s_to["room_id"]
            if room_s_to["room_id"] not in visited_rooms:
                print("room visited", len(visited_rooms))
                visited_rooms[room_s_to["room_id"]] = dict()
                for d in room_s_to["exits"]:
                    visited_rooms[room_s_to["room_id"]][d] = "?"
                visited_rooms[room_s_to["room_id"]]["n"] = room["room_id"]
            else:
                visited_rooms[room_s_to["room_id"]]["n"] = room["room_id"]

        else:
            queue = []
            paths = []
            for d in room["exits"]:
                paths.append([d])
                queue.append(visited_rooms[str(room["room_id"])][d])
            while len(queue) > 0:
                room_id = queue.pop(0)
                path = paths.pop(0)

                if ("s" in visited_rooms[str(room["room_id"])]) or ("n" in visited_rooms[str(room["room_id"])]) or ("w" in visited_rooms[str(room["room_id"])]) or ("e" in visited_rooms[str(room["room_id"])]):
                    print("queue", room_id)
                    queue.clear()
                    current_room = room
                    for p in path:
                        new_room = moving_function(
                            p, visited_rooms[str(current_room["room_id"])][p])
                        current_room = new_room

                    stack.append(current_room)
                else:
                    if "s" in visited_rooms[str(room["room_id"])]:
                        new_path = path.copy()
                        new_path.append("s")
                        paths.append(new_path)
                        queue.append(visited_rooms[str(room["room_id"])]["s"])
                    if "n" in visited_rooms[str(room["room_id"])]:
                        new_path = path.copy()
                        new_path.append("n")
                        paths.append(new_path)
                        queue.append(visited_rooms[str(room["room_id"])]["n"])
                    if "w" in visited_rooms[str(room["room_id"])]:
                        new_path = path.copy()
                        new_path.append("w")
                        paths.append(new_path)
                        queue.append(visited_rooms[str(room["room_id"])]["w"])
                    if "e" in visited_rooms[str(room["room_id"])]:
                        new_path = path.copy()
                        new_path.append("e")
                        paths.append(new_path)
                        queue.append(visited_rooms[str(room["room_id"])]["e"])
