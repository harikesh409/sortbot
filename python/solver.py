import requests
import json
import sys

endpoint = "https://api.noopschallenge.com"


def print_sep():
    print("="*100)


def get_answer(question, level):
    vowels = 'aeiou'
    if level == 4:
        return sorted(question, reverse=True, key=len)
    elif level == 5:
        return sorted(question, key=lambda word: sum(ch in vowels for ch in word))
    elif level == 6:
        return sorted(question, key=lambda word: sum(ch not in vowels for ch in word))
    elif level == 7:
        return sorted(question, key=lambda word: len(word.split(' ')))
    return sorted(question)


def solve_question(questionURL, level):
    print(f"Set URL: {questionURL}")
    print(f"Stage: {level}")
    question = get_json(questionURL)
    print(f"Question: {question['message']}")
    print(str(question['question'])[1:-1].replace("'", ''))
    answer = get_answer(question['question'], level)
    print(f"Answer: ", end="")
    print(str(answer)[1:-1].replace("'", ''))
    print_sep()
    result = post_json(questionURL, {"solution": answer})
    if result['result'] == "finished":
        print("🏆 "*20)
        print(result['message'])
        print(f"Certificate: {endpoint+result['certificate']}")
        print("🤖 "*20)
        sys.exit(0)
    elif result['result'] == "success":
        return result['nextSet']
    else:
        print("Error: ")
        print(result)


def get_json(url):
    try:
        request = requests.get(endpoint+url)
        return request.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def post_json(url, body):
    try:
        response = requests.post(url=endpoint+url, json=body)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def main():
    print("Starting Exam")
    print_sep()
    start = post_json("/sortbot/exam/start", {"login": "harikesh409"})
    print(start['message'])
    questionURL = start['nextSet']
    print_sep()
    level = 1
    # print(json.dumps(question,indent=4))
    while questionURL:
        questionURL = solve_question(questionURL, level)
        level += 1


if __name__ == '__main__':
    main()
