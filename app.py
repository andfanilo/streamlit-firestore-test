import os
import json
import firebase_admin
from firebase_admin import firestore
import secrets_beta
import streamlit as st

PATH_TO_FIRESTORE_KEY = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

# Write firestore key from env to file if it doesn't exist on S4A container / locally
try:
    with open(PATH_TO_FIRESTORE_KEY, "x") as f:
        json.dump(json.loads(os.environ["FIREBASE_KEY"]), f)
except FileExistsError:
    pass

# Authenticate to Firestore through GOOGLE_APPLICATION_CREDENTIALS env var
if not firebase_admin._apps:
    firebase_admin.initialize_app()

app = firebase_admin.get_app()
db = firestore.client(app)

# Streamlit widgets to let a user create a new post
with st.sidebar:
    st.subheader("Create a new post")
    title = st.text_input("Post title")
    url = st.text_input("Post url")
    password = st.text_input("Password for submission authorization", type="password")
    submit = st.button("Submit new post")

    # Once the user has submitted, upload it to the database
    if title and url and submit:
        if password==os.environ["SUBMIT_PASSWORD"]:
            doc_ref = db.collection("posts").document(title)
            doc_ref.set({"title": title, "url": url})
        else:
            st.warning("Wrong password, can't authorize submit")

# And then render each post, using some light Markdown
st.title("Hello Firestore :fire:")
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
    post = doc.to_dict()
    title = post["title"]
    url = post["url"]

    st.subheader(f"{title}")
    st.write(f":link: [{url}]({url})")
