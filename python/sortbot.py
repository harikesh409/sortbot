import requests
import json
import random
import re
import sys

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
    answer = input("Enter sorted list of Comma Seperated Values \n")
    if type(answer[0]) == str:
        answer = re.sub(r'\s*,\s*',',',answer)
        answer = json.dumps(answer.split(','))
    sorted_json = '{"solution":'+answer+'}'
    # print(sorted_json)
    verify = requests.post(url=qsn_endpoint, json=json.loads(sorted_json))
    result = verify.json()
    if result['result'] == "finished":
        print("🏆 "*20)
        print("You did it! You completed the challenge in " +
          question['elapsedTime']+" milliseconds.\n")
        print("See your certificate at "+endpoint+question['certificate'])
        print("\nThank you for playing.")
        print("👋  Bye bye.")
        sys.exit(0)
    if result['result'] == "success":
        print("You're right! "+result['message'] +
              " Let's see... here's the next questions\n")
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
get_question(response_json['nextSet'])