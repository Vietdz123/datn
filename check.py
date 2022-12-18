import json

def add_json(key: str, value: str, responce: str) :
    json_responce = json.loads(responce)
    json_responce[key] = value
    return json.dumps(json_responce)
    
    
if __name__ == '__main__':
  rs = add_json("3", "true", "{}")
  rs2 = add_json("5", "false", rs)
  rs3= add_json("15", "reue", rs2)
  print(rs)
  print(rs3)
  
  
  fruit_json = {"apple" : 1, "orange" : 2}
  key = "banana"
  value = 3

  fruit_json[key] = value

  print(fruit_json)