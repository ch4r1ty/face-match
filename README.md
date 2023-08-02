# face-match
## WHAT IS IT
Face-Match is a program aiming at face comparison



## TOOLS
[pandas](https://pandas.pydata.org/)

[face_recognition](https://github.com/ageitgey/face_recognition)




## FILE DESCRIPTION
~~**'main.py'**: Do not read it plz, it's completely shitty code!🤮🤮 It is where the coder first coded all the lines in one python file~~

~~**'app.py'**: Linked to 'main.py'🤮🤮~~

~~**'function.py'**: The coder packages functions in 'main.py' in one function😊😊~~

**'main.py'**: It is the most vital code in the project! Many little functions are decomposed from one single function in 'function.py'🥵🥵

**'app.py'**: Linked to 'test.py', not bad🥵🥵

**'parameter.py'**: Adjust the tolerance. The higher the tolerance(between 0 to 1), the simpler the system will recognize faces.





---

## UPDATE

### 07/31/2023

* To improve the efficiency of the program, by saving face-encodings in a new file: **'face_encodings.pkl'**, instead of getting all the know_face_encodings each time when posts a request.

  Before: 0.15s

  Now: 1.1920928955078125e-05

* To improve the efficiency again, create a Thread Pool in function.

* New a js file and a html file, allowing coders to submit images in browsers.


### 08/02/2023

* Instead of importing an image file, this version imports the binary files, improving efficiency of the program.
* Loading the Excel file in the first beginning, rather than in functions.
