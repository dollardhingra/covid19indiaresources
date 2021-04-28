# Covid19 India Resources
This is a telegram bot for searching covid19 resources like oxygen cylinders, hospital 
beds, icu & ventilator beds, food and medicines on Twitter.

### Demo
![image](https://github.com/dollardhingra/covid19indiaresources/blob/master/about.gif)

### How to use this?
* Install Telegram on your device(available on android, ios, windows, mac). 
[Download from here](https://telegram.org/)

* After installing, search for the bot `Covid19 India Resources`, select the one with
the Indian national flag as the display picture

* click Start

* Select your city, select the resource you are searching for.

* You will get a twitter link which is basically a Twitter search for the resources
you are searching for. 


**The result should not have keywords like "requested, needed etc" 
to filter out the tweets requesting for the resources.**


### Contribution
Feel free to contribute and improve the code. 

**Steps to run:**
* create a python virtual environment for python 3.7
* install the requirements
    ```python
        pip install -r requirements.txt 
    ```
* Create a telegram bot and get your own API key for testing/running. [Steps here](https://core.telegram.org/bots#creating-a-new-bot)

* Export the token with the following command:
    ```
    export TELEGRAM_TOKEN=<API-TOKEN>
    ```

* run the following now:
    ```
    python main.py
    ```

**Steps for creating a PR:**
* create a new feature branch from master
* do the changes
* run black formatter
* run Pylama
* run unitests
* commit and push, and then create a PR.