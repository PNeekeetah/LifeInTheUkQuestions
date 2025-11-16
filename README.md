# Life in the UK quizzer

## Usage

### Quiz mode

`python3 -m Quizzer`

If the file `QuestionsWithCorrectChoice.pkl` exists, the program is started in quiz mode. 

The program has 2 modes of operation. You can either click `Check` as you go or you can go through all questions and then click `Finish`. Once you click `Finish`, the test gets retroactively evaluated and then you get a list of all right/ wrong questions.

You can still navigate the test using Next/ Previous.

### Setting the right answers mode

`python3 -m Quizzer`

If the file `QuestionsWithCorrectChoice.pkl` doesn't exist, the program is started in settings mode. It will parse the `UkTestUnsureQuestions.md` file (see `Adding text questions` for formatting). You get to set the correct answers via `Ticks`. Whenever you click `Next`, the answer gets saved.  That does imply that you can go back and correct any answers you've chosen (previous -> correct -> click next to save).

Once you've gone through all of the questions, you can exit the program. The next time you start it, it will get started in Quiz mode. 

## Adding new questions

### Adding JSON questions

There are 2 python programs available : 

- `PickleToJson` which takes a pickle file and creates the equivalent JSON representation
- `JsonToPickle` which takes a json file and creates the equivalent pickle file.
  
You can run it on the current set of questions (`QuestionsWithCorrectChoice.pkl`) and add your own!

This is the easiest way to add new questions in my opinion.

### Adding text questions

If you want to add your own questions, you can use the following format:

```
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
 \```
OFFICIAL EXPLANATION (may be multiple lines) (optional)
 \``` 
```

For example

```
--- Guessed
 
Which British sportsman won five consecutive gold medals at the Olympic Games in the rowing category?

    Sir Chris Hoy
    Christopher Dean
    Bradley Wiggins
    Sir Steve Redgrave

I always forget that it's Redgrave 

 \```
A comment
 \```

```

The `\` are there to prevent the code block from being ended and started again. 