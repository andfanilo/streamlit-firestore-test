import os
import json
import firebase_admin
from firebase_admin import firestore
import secrets_beta
import streamlit as st

PATH_TO_FIRESTORE_KEY = "firestore-key.json"

# Write firestore secret to file if it doesn't exist
# Then load secrets from file
try:
    with open(PATH_TO_FIRESTORE_KEY, "x") as f:
        json.dump(json.loads(os.environ["FIREBASE_KEY"]), f)
except FileExistsError:
    print("Firestore key file file already exists")

# Authenticate to Firestore through GOOGLE_APPLICATION_CREDENTIALS env var
if not firebase_admin._apps:
    firebase_admin.initialize_app()

app = firebase_admin.get_app()
db = firestore.client(app)

# Streamlit widgets to let a user create a new post
with st.sidebar:
    title = st.text_input("Post title")
    url = st.text_input("Post url")
    submit = st.button("Submit new post")

    # Once the user has submitted, upload it to the database
    if title and url and submit:
        doc_ref = db.collection("posts").document(title)
        doc_ref.set({"title": title, "url": url})

# And then render each post, using some light Markdown
st.title("Hello Firestore :fire:")
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
    post = doc.to_dict()
    title = post["title"]
    url = post["url"]

    st.subheader(f"{title}")
    st.write(f":link: [{url}]({url})")
