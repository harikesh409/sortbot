import requests
import json
import random

def get_question(nextSet):
    qsn_endpoint = endpoint + nextSet
    question = requests.get(url=qsn_endpoint)
    question_json = question.json()
    print(question_json['message'])
    print("Example solution: ")
    print(str(question_json['exampleSolution']
              ['solution'])[1:-1].replace("'", ''))
    print("="*100)
    print(str(question_json['question'])[1:-1].replace("'", ''))
    sorted = input("Enter sorted list of Comma Seperated Values \n")
    if type(sorted[0]) == str:
        sorted = json.dumps(sorted.split(','))
    sorted_json = '{"solution":'+sorted+'}'
    # print(sorted_json)
    verify = requests.post(url=qsn_endpoint, json=json.loads(sorted_json))
    result = verify.json()
    if result['result'] == "finished":
        return result
    if result['result'] == "success":
        print("You're right! "+result['message']+" Let's see... here's the next questions\n")
        # print(result['nextSet'])
        get_question(result['nextSet'])
    else:
        print("Sorry, that's not correct: "+result['message'])
        get_question(nextSet)


endpoint = "https://api.noopschallenge.com"
username = input("Enter you github username: ")
username_errors = [
    "Please enter a username",
    "C'mon, enter a username",
    "Hey, just the username please.",
    "All I'm asking for is a username here.",
    "OK but first your GitHub username."
]
while username == "":
    username = input(random.choice(username_errors)+"\n")
data = {'login': username}
response = requests.post(url=endpoint+"/sortbot/exam/start", json=data)
response_json = response.json()
print(response_json['message'])
question = get_question(response_json['nextSet'])
if(question['result'] == "finished"):
    print("You did it! You completed the challenge in " +
          question['elapsedTime']+" milliseconds.\n")
    print("See your certificate at "+question['certificate'])
    print("\nThank you for playing.")
