# oBey - Group 5
Group coursework for the Web Programming module.

- Alberto Morabito
- Lorenzo Sani
- Martynas Jankus

## Setup

1) Create the environment with the right version of Python<br>
`conda create --name AuctionApp python=3.6`

2) Activate the environment you just created<br>
`conda activate AuctionApp`

3) Clone the repo<br>
`cd` to your desired folder, then run:<br>
`git clone https://github.com/lorenzosani/auction-app.git`

4) cd inside the repo you just cloned and install dependencies:<br>
`pip install -r requirements.txt`<br>
Don't forget to update the requirements.txt and push that to git if you install new packages.<br>
You can do so by running `pip freeze` and copying over the added module(s) to said .txt file.

5) Create a development DB<br>
`python ./manage.py migrate`<br>

6) You should be good to go!<br>
`python ./manage.py runserver`, and you should see your dev server live on localhost:8000<br>


Remember that if on Windows, you will need to add python to your PATH.

## Advanced feature: password reset

To correctly send emails, you need to add a `.env` file in the same folder as your `settings.py`
The file should look like:
```
EMAIL_HOST_USER=your_account@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

Also, make sure to turn ON the gmail setting "Allow less secure apps" for the emails to be sent successfully.
