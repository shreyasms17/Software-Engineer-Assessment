
## EVIL GENIUSES SOFTWARE ENGINEER INTERN ASSESSMENT

The current directory contains a setup.sh file, which contains the necessary python3 packages that need to be installed prior to executing the Python scripts.

The folder structure in this repo looks like this:
#### Folder Structure:
| Name | Files |
|--|--|
|.|Q3_design.txt, README.md, setup.sh, SWE Intern Assessment.pdf|
| code/ | process_game_state.py, question_2.py, main.py |
| data/|game_state_frame_data.parquet|
|map/|de_overpass_radar.jpeg|
|output/| results.txt, result.png |


###  Which file refers to which question in the assessment? 
| Question | File | Description |
| -- |--|--|
|Question 1|code/process_game_state.py|Contains the ProcessGameState class|
|Question 2| code/question_2.py |Contains functions for each subquestion in Question 2|
| Question 1 & 2|code/main.py|Creates an object of ProcessGameState class & executes functions in code/question_2.py|
| Question 3 | Q3_design.txt | A design for the problem in Question 3 |


### Steps to follow: 
```
    sh setup.sh
    python3 code/main.py > output/results.txt
```