import requests

def send_action(cred , action) :
    actionUrl = "{}/listening".format(cred["tunnelUrl"])
    print(actionUrl)
    resp = requests.post(
        actionUrl, 
        auth=(cred['username'], cred['password']),
        headers={"Content-Type": "application/json" , 
                "action" : action ,
                })
    # tunnelUrl = "https://af4e-103-240-162-120.ngrok-free.app"
    # resp = requests.get(
    #     "{}/actions".format(tunnelUrl), 
    #     auth=(cred['username'], cred['password']),
    #     headers={"Content-Type": "application/json" })
    resdata = resp.json()
    print(resdata["actions"])
