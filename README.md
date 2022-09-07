# End_to_End_ML_Project
***This is my first complete end to end machine learning project.***

## Software & Account Requirements

1. [Github Account](https://github.com)
2. [Heroku Account](https://dashboard.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [Git CLI](https://git-scm.com/downloads)

Creating conda environment
```
conda create -p venv python==3.7 -y
```

Activating the virtual environment
```
conda activate venv/
```

```
pip intsall -r requirements.txt
```

To Add Files to git
``` 
git add .
```
OR
``` 
git add <file_name>
```

> Note: To ignore files or folders from git we can write names of file/folder in  .gitignore file

To check the git status
```
git status
```

To check all the version maintained by git
```
git log
```

To create version/commit all changes by git
```
git commit -m message
```

To send version/changes to github
```
git push origin main
```

To check  remote url
```
git remote -v
```

To Setup CI/CD Pipeline in heroku we need 3 information:
1. HEROKU_EMAIL = avr13405@gmail.com
2. HEROKU_API_KEY = c83e1bf6-628b-49d0-8f9a-0bb7dce7555e
3. HEROKU_APP_NAME = ml-regression-app-avr

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tag_name>
```
> Note: The image name must be lowercase

To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 <image_id>
```

To check running containers in docker
```
docker ps
```

To Stop Docker Container
```
docker stop <container_id>
```