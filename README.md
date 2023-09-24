# image-downloader

This is a program to download the images of products from Amazon and Flipkart with names.

## USE CASE

1. If you wish to have all the pics of the products for any reason.

## Installation for Linux Users

### Step 1

If you are a Linux user just dive into the project dir.  
Now you have to execute the below commands.

`
chmod +x install.sh
./install.sh
`

### Step 2 Loading the guns before shooting

Write all the product name and their URL in the Products.txt.  
The format is:  

```
Product Name, URL of product  
Product Name1, URL of product1  
Product Name2, URL of product2  
Product Name3, URL of product3  
```

### Steps 3 Shooting the Load

Now you just need to run the `run.sh` file.  
To run the software.
Just execute the below command in the shell.  

`./run.sh`  

## Installation and Working for Windows Users

### Step 0

Check and install python.  

### Step 1

Write all the product name and their URL in the Products.txt.  
The format is:  
```
Product Name, URL of product  
Product Name1, URL of product1  
Product Name2, URL of product2  
Product Name3, URL of product3  
```

### Step 2

***Create a Python virtual environment (not necessary but recommended).***  

Steps to create a virtual environment in Python:  

```python -m venv env```

### Step 3

Activate the virtual environment.  
***Ignore If ignored Step 2***  

#### For Command Prompt

```env\Scripts\activate.bat```

#### For PowerShell

```env\Scripts\Activate.ps1```

### Step 4

Dive into the folder/directory in shell/terminal.  
Install the requirements.txt using the below command.  

```pip install -r requirements.txt```

### Step 5

Run the imagedownloader.py using the below command.  

```python imagedownloader.py```

### Step 6

***Ignore if ignored Step 2 and Step 3***  

Deactivate the virtual environment.  

````deactivate```
