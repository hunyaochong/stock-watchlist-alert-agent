Sending single emails using the Mailgun API
Let's first look at the most simple way of using Mailgun API: sending a single email. You can use it for one-off cases, like sending a reminder or a follow-up email to your high-value customer. This will allow you to track the email delivery as well.

Copy and paste the code below into your main.py file after the imports and initialization:

python
1
```python
2
def send_single_email(to_address: str, subject: str, message: str):
3
    try:
4
        api_key = os.getenv("MAILGUN_API_KEY")  # get API-Key from the `.env` file
5
​
6
        resp = requests.post(MAILGUN_API_URL, auth=("api", api_key),
7
                             data={"from": FROM_EMAIL_ADDRESS,
8
                                   "to": to_address, "subject": subject, "text": message})
9
        if resp.status_code == 200:  # success
10
            logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
11
        else:  # error
12
            logging.error(f"Could not send the email, reason: {resp.text}")
13
​
14
    except Exception as ex:
15
        logging.exception(f"Mailgun error: {ex}")
16
​
17
if __name__ == "__main__":
18
    send_single_email("Manish <manish@exanple.com>", "Single email test", "Testing Mailgun API for a single email")
19
```
This send_single_email(...) function takes three arguments: to_address, subject, and message. to_address is for a single email address, and the other two are for the email's subject and content.

The code reads the Mailgun API key from the .env file and uses it to make an API call to the specified API_URL. This API key acts as a unique identifier, allowing Mailgun to authenticate the API call and verify who is using its services.

You must use your unique API key to ensure proper authentication. The from email address used in this API call must also be associated with your valid domain or Mailgun's sandbox domain. If it doesn't, the call will fail with an error message.

The data parameters are sent via HTTP POST method to the API endpoint with the requests.post(...) call.

When the API call is successful, your email will be queued for delivery, and the API will return an HTTP-200 (OK) status. In case of an error, the API will return an error message with an appropriate HTTP status code. Both cases are appropriately logged by this code snippet.

Best practices
It's also important to keep some best practices in mind when you send emails programmatically.

Error handling
When your script uses a third-party API like Mailgun to send emails, you must handle potential errors related to network or API failures and API responses indicating errors to ensure your script works smoothly, can detect issues like invalid API keys or URLs, and knows when emails aren't sent by the Mailgun API. Without error handling, your script might fail silently, resulting in undelivered emails.

The code snippets above all provide for handling errors that might occur. Firstly, they check the response status code (resp.status_code). If it's not successful (HTTP 200), they log the error message so you can debug the issue.

Both the send_single_email(...) and send_batch_emails(...) functions also use a try-except block to ensure any exceptions are caught and logged correctly.

Email deliverability
Email deliverability means ensuring your emails land in the recipient's inbox, not their spam folder. You need a good sender reputation to achieve high deliverability. When we’re talking about building programmatic sending, there are a couple specific things we can look at to improve your email deliverability including authentication, and optimizing emails to be responsive. We’re talking about each below.

Authenticate your email
Use SPF, DKIM, and DMARC to validate your identity as a sender. Only send emails to verified subscribers who have opted in to receive them and regularly remove inactive subscribers and those who mark your emails as spam.

DMARC is becoming an industry requirements. Learn more about why, and what this authentication standard does in our post on the DMARC perspective. 

Responsive emails
Most users access content on various devices like mobile phones, iPads, and tablets, and they expect your emails to be visually appealing and easy to read across different screens.

This requires that you use responsive design techniques, such as fluid layouts, CSS media queries, and optimized images. You should also test your emails on various devices, email clients, and screen sizes to verify that they display correctly.

Responsive design is particularly important if your emails contain a lot of HTML content with images or if you're using email templates. Mailgun's predefined templates are responsive by default.

Here's the basic code you need. Plug in your API info from above and modify the from address, to address, and other content to give Mailgun a good old test drive.
import os
import requests
def send_simple_message():
  	return requests.post(
  		"https://api.mailgun.net/v3/sandbox125c63e39e4d41d5b65183834fe94aea.mailgun.org/messages",
  		auth=("api", os.getenv('API_KEY', 'API_KEY')),
  		data={"from": "Mailgun Sandbox <postmaster@sandbox125c63e39e4d41d5b65183834fe94aea.mailgun.org>",
			"to": "Hun Yao Chong <hunyaochong@gmail.com>",
  			"subject": "Hello Hun Yao Chong",
  			"text": "Congratulations Hun Yao Chong, you just sent an email with Mailgun! You are truly awesome!"})