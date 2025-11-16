# Life in the UK quizzer

## Usage

`python3 -m Quizzer`

The program has 2 modes of operation. You can either click `Check` as you go or you can go through all questions and then click `Finish`. Once you click `Finish`, the test gets retroactively evaluated and then you get a list of all right/ wrong questions.

You can still navigate the test using Next/ Previous.

## Adding new questions

### Adding JSON questions

There are 2 python programs available : 

- `PickleToJson` which takes a pickle file and creates the equivalent JSON representation
- `JsonToPickle` which takes a json file and creates the equivalent pickle file.
  
You can run it on the current set of questions (`QuestionsWithCorrectChoice.pkl`) and add your own!

### Adding text questions

If you want to add your own questions, you can use the following format:

<<<
--- (wrong)|(guessed)|(any other tag) 
<blank line> 
QUESTION 
<blank line> 
CHOICE 1 
CHOICE 2 
... 
CHOICE N 
<blank line> 
PERSONAL COMMENT
```
OFFICIAL EXPLANATION (may be multiple lines) (optional)
``` 
>>>

For example

<<<
--- Guessed
 
Which British sportsman won five consecutive gold medals at the Olympic Games in the rowing category?

    Sir Chris Hoy
    Christopher Dean
    Bradley Wiggins
    Sir Steve Redgrave

I always forget that it's Redgrave 
>>>