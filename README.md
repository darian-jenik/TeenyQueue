# TeenyQueue

ref: RnM

(if you know you know)

---

Basically a simple http based queue.

---

### Authentication

You can add authentication to individual messages (or all of them).

Authentication is uuid4 based.  This solves a few other issues and stops people putting in basic passwords.

---

### Targeted Messages

You can send messages to specific subscriber named modules.  
This is good if you want to send a message and makes sure a particular module (or all of them) gets it.

---

### Timed Messages

You *could* use it almost as a job scheduler.

Warning, the timezone thing is borked a bit.  You may need to adjust.

Also the timezones don't work in the tests.  It's on the list to fix one day maybe.

---

### Pagination

The endpoints /list and /list_all have optional pagination parameters.

e.g.

    page_size
    page_number

    http://localhost:8000/list?page_size=5&page_number=2

Defaults are 

    page_size = 1000
    page_number = 1

You can set default_page_size in config.yaml

---

### db_setup

Look in there for the schema and account setups.

---

### /docs url on the api

Set debug to True in the config.yaml and they will appear.

---

config.yaml has some configuration variables

---

#### TODO:

- Proper authentication
- Webhooks
- Containerize it.

---

Built in python 3.12 but should work anywhere

Logs by default go to ./main.log  You can change that in config.yaml

