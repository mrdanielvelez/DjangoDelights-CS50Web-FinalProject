# Django Delights: Restaurant Manager — Harvard CS50 Web — Final Project

## Video Demo: https://youtu.be/ZDbdKcrhRsY

![YT Thumbnail](https://user-images.githubusercontent.com/85040841/138975266-5d8d1934-8ded-4596-9b94-2887eeb44c01.png)

## Distinctiveness and Complexity:
I made a restaurant manager using Django on the back-end and JavaScript on the front-end. The project uses a REST API in order to be a single-page web app. I focused on improving my front-end creative skills while creating this final project, as I believed that my CSS/SCSS needed to be improved after going over my previous projects for this course. More specifically, I wanted to become better at responsive design and advanced CSS. I decided to learn Figma and use it to design a mockup for the project. I chose a modern color scheme that reflected the theme of a lighthearted bakery. The app has four main features: 1. A "Menu" interface, which displays all of the restaurants menu items, containing an image and a "View Recipe" button. After clicking that button, the user gets shown the ingredient requirements for the recipe. 2. An "Inventory" interface, which contains all of the restaurant's ingredients and corresponds to individual recipes. 3. A "Purchases" interface, which displays all of the purchases that occured in the history of the restaurant, including the item name and the date and time of the purchase. 4. A "Finances" interface, which displays the profit, revenue, and expense information for the restaurant. The first three interfaces all have a form at the top of the display area which enables the user to add database entries for that specific interface. Lastly, this was also my final project for Codecademy's Django Skill Path, which I took simultaneously with CS50 Web, as I wanted to really understand the fundamentals of Django.

---

## What's contained in each file:
* views.py contains all of the project's views, including all of the various account views and API views
* models.py contains all of the project's models, which are "User", "Ingredient", "MenuItem", "RecipeRequirement", and "Purchase"
* admin.py registers all of the various models for the Django admin interface
* base.html is the base template for the app, it includes the project's logo and navigational items and imports my stylesheets i.e. Bootstrap, favicons, etc.
* app.html contains the app's center box and all of the SPA views, similar to project 3 "Mail"
* login.html contains the login template for the app
* register.html contains the register template for the app
* main.scss contains the main scss design file for the app which imports other helper files
* _variables.scss contains all of the variables used by main.scss
* _responsive.scss contains the mobile responsiveness stylesheet that is imported by scss
* _placeholders.scss contains scss placeholders used by main.scss
* _mixins.scss contains scss mixins used by main.scss
* main.css is the compiled version of main.scss
* main.js contains all of the API requests and dynamic features of the web app
* logo.png is the project's logo
* bottom_graphics.svg is the "wave" design on the bottom of the page
* the favicon_io folder contains all of the various favicon sizes and the webmanifest file for them
* requirements.txt contains all of the necessary Python packages in order to run the web application

---

## How to run the application:
1. Ensure that you have all of the necessary Python packages (see requirements.txt)
2. Navigate to the location of manage.py
3. Run "python manage.py runserver" in the terminal
