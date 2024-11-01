# Finance 50 JavaScript | JSON and Idempotency web design
#### Video Demo: https://youtu.be/Q3MgnXcnT2M
#### Description:
I wrote the finance50 project to use Javascript in the front end and have the server reply with JSON data.
This is significantly different than the Finance50 pset for the following reasons:
1) We weren't taught how to write the client side in JavaScript or how to utilize JSON formatted data. Dr. Malan had a short demo on it's usefulness in his lecture where he was talking about displaying SQL data on a website. He didn't show any code for it, however I liked how fast and responsive it felt. So I spent a couple of weeks learning JavaScript and implementing it. I then learned that Check50 doesn't check JavaScript or JSON, so all my checks failed for the pset (415 error). After speaking with curiouskiwi, she okayed using this implementation for my final project so long as I added extra scope.
2) The client side is written in JavaScript rather than utilizing jinja to the extent required by the pset
3) Communications to and from the server utlizes serializing and deserializing JSON into actionable data for both the client and the server.
4) I made this server authoritative. This lead me down the Idempotency rabbit hole, after viewing Stripe's docs (https://docs.stripe.com/error-low-level#idempotency) I learned how to use Idempotency and uuidv4 hashkeys (code for generating the keys from user Broofa: https://stackoverflow.com/questions/105034/how-do-i-create-a-guid-uuid/2117523#2117523) to limit restrict client interactions to the server to one action at a time per hashkey. When the server is done working on the request, it makes a copy of the request to the audit SQL table and then clears the hashkey from the in-memory static dict.
5) I chose an in-memory static dict rather than using mutliple SQL calls to make the operation faster. The audit is in place so that if needed, someone with SQL access could compare the requests to the user's transaction data and if needed, retry the event.
6) Yahoo's API went down, using reddit (https://www.reddit.com/r/sheets/comments/1farvxr/comment/llxk7m9/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) I found the updated API link, so I made some edits to retrieve the data and convert it to JSON, I extended lookup() to also retrieve additional information such as the company name.
7) Added on the client side, confirmation of destructive actions to buy and sell POSTs, where the user clicks okay on a popup to continue the POST request. Additionally for sell and buy, I added a throttle to the JS function to send the POST request to prevent buying or sellng additional stocks which the user did not own. This was also rectified server-side when I implemented the server authoritative design.
8) Added mouse over tool tips for stock ticker symbols, which include the long name for the company and yesterday's closing price.
9) For the transactions history page, I created a dict to store new symbols I had to look up to reduce the number of hits to Yahoo's API and speed up the page when there was many transactions.
10) Using data from CS50 duck, added a download csv option to the history page.
11) Some updated formatting changes in style.css for formatting the page.



The idempotency plan required a few things:
1) checkQueue() function in helpers.py for all my server-side functions to call before a POST is done to the SQL db. It returns null when the user has a job in the queue and 1 if not. The user can only have 1 job in the queue at a time.
2) Created a new audit table in the sql database to log all the hashkey used, user_id, end_point reached, method, request, status_code, and timestamp to distinguish between different requests.
Used try: and except: for the affected functions to clear the user's line from the dictionary when the job is complete or when there's an error talking with the sql db.
logRequest() function in helpers.py logs the requests to the audit table.

Example Output:
+----+--------------------------------------+---------+-----------+--------+----------------------------------------+-------------+---------------------+
| id |                 key                  | user_id | end_point | method |                request                 | status_code |      timestamp      |
+----+--------------------------------------+---------+-----------+--------+----------------------------------------+-------------+---------------------+
| 3  | 9d4cf1f9-4504-4261-b855-861e97e332d1 | 9       | /buy      | POST   | {"symbol": "qs", "shares": "1"}        | 200         | 2024-09-07 22:46:00 |
| 4  | 9d4cf1f9-4504-4261-b855-861e97e332d1 | 9       | /buy      | POST   | {"symbol": "qs", "shares": "1"}        | 200         | 2024-09-07 22:46:02 |
| 5  | 02190250-8676-41cc-adb6-c5f89d683f01 | 9       | /buy      | POST   | {"symbol": "qs", "shares": "1"}        | 200         | 2024-09-07 22:53:19 |
| 6  | 02190250-8676-41cc-adb6-c5f89d683f01 | 9       | /buy      | POST   | {"symbol": "EA", "shares": "13"}       | 200         | 2024-09-07 23:04:48 |
| 7  | 02190250-8676-41cc-adb6-c5f89d683f01 | 9       | /buy      | POST   | {"symbol": "TSN", "shares": "2"}       | 200         | 2024-09-07 23:04:59 |
| 8  | 02190250-8676-41cc-adb6-c5f89d683f01 | 9       | /buy      | POST   | {"symbol": "TSN", "shares": "-1"}      | 400         | 2024-09-07 23:05:49 |
| 9  | 02190250-8676-41cc-adb6-c5f89d683f01 | 9       | /buy      | POST   | {"symbol": "TSN", "shares": "1000000"} | 400         | 2024-09-07 23:05:56 |
| 10 | 02190250-8676-41cc-adb6-c5f89d683f01 | 9       | /buy      | POST   | {"symbol": "TSN", "shares": ""}        | 400         | 2024-09-07 23:06:03 |
| 11 | cefa90c2-d1ec-495c-a7e1-05ac6a292f15 | 9       | /buy      | POST   | {"symbol": "qs", "shares": "1"}        | 200         | 2024-09-08 00:45:06 |
| 12 | ac6c1c82-2725-4d85-9a29-8f72ce3102b4 | 9       | /sell     | POST   | {"symbol": "TSN", "shares": "1"}       | 200         | 2024-09-08 01:53:55 |
| 13 | 78751643-591f-42cc-ac5d-a56245675d58 | 9       | /sell     | POST   | {"symbol": "ACT", "shares": "0"}       | 200         | 2024-09-08 02:00:32 |
| 14 | a1516779-7401-4645-b857-0e5494aefc91 | 9       | /sell     | POST   | {"symbol": "NFLX", "shares": "0"}      | 500         | 2024-09-08 02:03:10 |
| 15 | a1516779-7401-4645-b857-0e5494aefc91 | 9       | /sell     | POST   | {"symbol": "NFLX", "shares": "0"}      | 500         | 2024-09-08 02:04:50 |
| 16 | a1516779-7401-4645-b857-0e5494aefc91 | 9       | /sell     | POST   | {"symbol": "NFLX", "shares": "2"}      | 412         | 2024-09-08 02:14:03 |
| 17 | a1516779-7401-4645-b857-0e5494aefc91 | 9       | /sell     | POST   | {"symbol": "EA", "shares": "10"}       | 200         | 2024-09-08 02:14:19 |

3) When the job is done on the server, clearKeyEntry() function in helpers.py is used to clear the job and the user can make a new request with the same hashkey.
