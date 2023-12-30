import requests

tunnelUrl = input("Device URL : ")
# username = input("username")
# password = input("password")
username = "master"
password = "master123"

actionUrl = "{}/listening".format(tunnelUrl)
print(actionUrl)
resp = requests.post(
    actionUrl, 
    auth=(username, password),
    headers={"Content-Type": "application/json" , 
             "action" : "button press ? " ,
             })

print(resp)
