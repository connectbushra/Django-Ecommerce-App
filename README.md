# Django-Ecommerce-AppEcommerce App using Django and MySql
##              Project Summary
This is an E-Commerce web application using Django and MySql ,The website displays products.User can register and login and also able to forget password by Email verification.The customer can search for products, customer can filter product by ‘category’ , ’Brands’, ‘colors’ and by different persons type. Customer can add product to cart ,all products will store in the cart bag. customer can Review for products and give star rating and also see reviews by other customers .Users can update the product, can increase or decrease quantity of product and can also remove products from the cart and check out from the shop.customers will fill the address form and then will do payment through stripe payment gateway.
How to setup and run the ProjectTo get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with  


    pip install virtualenvrun
the following command in the base directory of this project  

virtualenv envThat will create a new folder env in your project directory. Next activate it with this command on Terminal    
      
      source env/bin/active
Set up a virtual environment and install django and the libraries used in this project from the ```   requirements.txt    ```  file using:~ 

    pip install -r requirement.txt
command to collect static files into STATIC_ROOT:~  
      
      python manage.py collectstatic        

Now you can run the project with this command :~           
    
      python manage.py runserver
