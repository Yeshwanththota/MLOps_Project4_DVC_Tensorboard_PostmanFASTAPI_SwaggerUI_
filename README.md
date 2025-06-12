![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-945DD6?style=for-the-badge&logo=dvc&logoColor=white)
![TensorBoard](https://img.shields.io/badge/TensorBoard-FFA000?style=for-the-badge&logo=tensorflow&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Swagger UI](https://img.shields.io/badge/Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

** Go to MLops_project4 folder for outputs**

Highlights:
1.	Use of pytorch.
2.	Use of tensorboard (not better than mlflow and comet-ml but tensorboard is fast) for experiment tracking.
3.	Custom training pipeline using DVC. (The adv is it skips the steps which are unchanged and just run the changes but python runs all everytime)
4.	API using FASTAPI and POSTMAN.
   
Project Worflow

6.	Projectsetup, Kaggle notebook, data_ingestion, data_preprocessing, model_arc,model_training. Code them.

7.	For model tracking, we use tensorboard. For this we make little code changes in model_training and run the command tensorboard --logdir=tensorboard_logs/ in venv. This will give you a URL and go to that to see the tensorboard and experiment tracking.

8.	Next is Training pile using DVC
9.	Add dvc to requirements. Install setup again
10.	Then dvc init --no-scm
11.	We use –no-scm because we didn’t initialised the git yet.
12.	Now we create dvc.yaml in root for custom training pipeline.
13.	Now code this file.
14.	Now delete the models,raw in artifacts and delete the kagglehub in .cache.
15.	Now run dvc repro in venv. It will run the project as mentioned in dvc.yaml.
16.	Now if you run it again, it will skip the steps which are not changes. This is what special with dvc.
17.	Now create a .gitignore and add whatever you don’t want to push to git repo. Now create repo and push the code to github.

18.	Now create a bucket and link service account with some permissions as discussed in project 2.
19.	Now add dvc-gs to requirements and run. We are connecting the dvc to our bucket.
20.	Run in venv dvc remote add -d myremote gs://my_dvc_bucket11/
21.	Now in vevn set the credentials like you did before (SET google_credentials…) and run dvc push.
22.	This will push to the bucket.
23.	Now create main.py and code for FAST API and test in terminal using uvicorn.
24.	uvicorn main;app –reload
25.	now you see a url and go to it
26.	Now we test the api using 2 methods
27.	First is in url add /docs. Go to predict and try it out.
28.	Upload image and hit execute.
29.	Now another method is postman
30.	Download and install and create account.
31.	Now open the app and beside overview click + then select POST.
32.	Make sure the API  is running.
33.	Now add the url in the screen
34.	http://127.0.0.1:8000/predict/
35.	then select body-form-data-key is file-select file-upload file- SEND
36.	you will see the output
37.	Done
