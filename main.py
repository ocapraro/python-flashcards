'''
A python module that is a flashcard app.

@author Oscar Capraro
'''
import random
import cv2
import json

FLASHCARDS = []
with open('art.json') as json_file:
  FLASHCARDS = json.load(json_file)

def update_database():
  '''
  Updates the json file.
  '''
  with open('art.json', 'w') as f:
    json.dump(FLASHCARDS, f)

def test_card(card)->int:
  '''
  A function that tests a flashcard.

  Args:
  card: the flashcard object.

  Returns:
  bool: the user's score.
  '''
  img = cv2.imread("Images/"+card["path"], cv2.IMREAD_ANYCOLOR)
  score = 0
  questions = 0

  cv2.imshow("Flashcard", img)
  cv2.waitKey(1)
  for key,value in card.items():
    if not (key == "path" or key == "score" or key == "streak"):
      answer = input(f"What's the {key}: ")
      questions+=1
      if answer.lower() == value.lower():
        score+=1
        print("Correct!")
      else:
        print(f"Incorrect, the correct answer is {value}.")
  
  cv2.destroyAllWindows() # destroy all windows
  return (score, questions)

def main():
  def run_game():
    global FLASHCARDS
    random.shuffle(FLASHCARDS)
    FLASHCARDS = sorted(FLASHCARDS, key=lambda k: k['score']) 
    score = 0
    out_of = 0
    for ii,i in enumerate(FLASHCARDS):
      result = test_card(i)
      if result[0]==result[1]:
        i["streak"] = (i["streak"]+1) if "streak" in i else 1
      else:
        i["streak"] = 0
      i["score"]+=result[0]+i["streak"]
      score+= result[0]
      out_of+= result[1]
      if ii>=9:
        break
    update_database()
    print(f"Your score is {score}/{out_of}")
    if input("Would you like to try again? ").lower() == "y":
      run_game()
  run_game()
  
main()