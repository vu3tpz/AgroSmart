# AgroSmart 🍃

Simple Machine Learning that implement in this Website.

AgroSmart is a web application developed using Python Django Framework. 

In AgroSmart you can find Soil nutrient details and you can also find the rainfall details. We also have crop recommentation system, it predict the crop that suitable for nutrient that you entered.

# Disclaimer ⚠️

**This website is Theoretical Model** so, don't use this website for Real-Time Farming Decision. This website shows how we can implement Machine learning into farming and how we can improve the agriculture using programming languages.

# Build with ⚒️

-> [**Python Django FrameWork**](https://www.djangoproject.com/) | **HTML** | **CSS** | **JavaScript** | [**Bootstrap**](https://getbootstrap.com/)

-> [**MongoDB**](https://www.mongodb.com/)

-> [**Numpy**](https://numpy.org/) | [**Pandas**](https://pandas.pydata.org/) | [**sklearn**](https://scikit-learn.org/)

# Modules 🔖

* **Admin**: This module is most important one, it manage Admin, Visitor, Officer, Seller and also manage product that add by seller. Without Admins approval Visitor, Officer, Seller can't access the website.

* **Visitor**: This module is the consumer module you can find Soil nutrient details and you can also find the rainfall details. We also have crop recommentation system,it predict the crop that suitable for nutrient that you entered. Also, request soil and fertilizer to agriculture officer though this website. In this website there is a Virtual Market, you can by organic product through this website. This product is added by seller module.

* **Officer**: This modules add soil nutrient details and also can add rainfall details to the website. This module is manage by agriculture officer, they can approve or reject soil and fertilizer request from the visitor.

* **Seller**: This module add products to Virtual market.

# How to run Locally 🖥️

1. Before the following steps make sure you have [git](https://git-scm.com/downloads) installed on your system.


2. Download and Install [Python](https://www.python.org/) required version.


3. Download and Install [MongoDb Community Server](https://www.mongodb.com/try/download/community) and [MongoDb Compass](https://www.mongodb.com/products/compass) on your system.


4. Read about [virtualenv](https://docs.python.org/3/tutorial/venv.html) in Python. Create a virtual environment for your project.


```
pip install virtualenv
```
```
virtualenv virtualenv_name
```


5. Activate the environment in cmd.


```
virtualenv_name\scripts\activate
```


6. Clone the GitHub project in your local directory with command `git clone https://github.com/vu3tpz/AgroSmart` or you can just download the code and unzip it. 


```
git clone https://github.com/vu3tpz/AgroSmart
```


7. Run the command in console `pip install -r requirements.txt`  go to that directory and run the above command. This command will install the necessary packages required to run the project.


```
pip install -r requirements.txt
```


8. Go the the directory where `manage.py` file is present. Run following commands in the cmd


```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py runserver
```


9. See your project is running on your local host `http://127.0.0.1:8000`


```
http://127.0.0.1:8000
```

# Demo Video 📽️

https://user-images.githubusercontent.com/101320198/168467893-e2d3f3f4-5c6a-45fc-b7c6-6c7029f52b04.mp4

https://user-images.githubusercontent.com/101320198/168467954-3cf718aa-7d3d-410a-8da8-1d49570232ee.mp4


# Screen Layout 🎟️

* **Index Page**

![Screenshot (26)](https://user-images.githubusercontent.com/101320198/168466313-8955eaa2-faea-45ec-8344-35ec8fef9e34.png)

* **Register Page**

![Screenshot (29)](https://user-images.githubusercontent.com/101320198/168466410-f7e2a6e1-53e0-4a89-ad2e-3bac8b704573.png)

* **Login Page**

![Screenshot (27)](https://user-images.githubusercontent.com/101320198/168466403-405a59c1-687c-4d0a-9210-cfbad4ecf392.png)
![Screenshot (28)](https://user-images.githubusercontent.com/101320198/168466408-d75f1610-ad3d-4390-92cd-aa14e68f7a6f.png)


* **Visitor Page for Find Details**


![Screenshot (30)](https://user-images.githubusercontent.com/101320198/168466412-3dc74a3f-9269-4e2a-bc20-21dd9d867488.png)
![Screenshot (31)](https://user-images.githubusercontent.com/101320198/168466415-5ac26cc5-0aae-48f9-a835-2035d7c6b3fb.png)

* **Visitor Virtual Market Page**

![Screenshot (32)](https://user-images.githubusercontent.com/101320198/168466416-a01102cb-ef8e-403d-b507-58e1c16b4000.png)


* **Admin Home Page**


![Screenshot (33)](https://user-images.githubusercontent.com/101320198/168466426-007a49b8-d27a-4a55-8e58-4cd5bbdeeb9b.png)

* **Admin Product View Page**

![Screenshot (36)](https://user-images.githubusercontent.com/101320198/168466454-ea24de14-d9c6-4b32-9980-960a959ef1f8.png)

* **Seller Page**


![Screenshot (35)](https://user-images.githubusercontent.com/101320198/168466442-40cfa1b2-e993-4ddd-9964-17484cfa6516.png)
![Screenshot (34)](https://user-images.githubusercontent.com/101320198/168466439-0266c086-6e84-41d3-a530-4ec0d5c0868a.png)

## The End..⚔️
