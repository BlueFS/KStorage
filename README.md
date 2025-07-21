# KStorage: A Lightweight Cloud Service for File Storage
## Video Demo:  <https://youtu.be/lmXLGJ10f38>
## Description
### Basics:
KStorage is my CS50x final project -- a very early prototype of a simple file storage cloud service. As of V1.0.0, it features the following:
- [x] Account creation
- [x] User login
- [x] Display name on profile page
- [x] Edit name, email, and password
- [x] Upload, download, and delete files
- [x] Store files in server based on userid
- [x] Retrieve files based on userid
- [x] Password encryption

Planned features:
- [ ] Confirm delete with prompt
- [ ] Two Factor Authentication (2FA)
- [ ] Email and password resetting via email
- [ ] Google Sign-On (OAuth)
- [ ] Light/Dark Mode -- Currently a light gray color is used -- A toggle is planned
- [ ] Refactor routes to be cleaner -- Make things more consolidated into one blueprint

It utilizes the following to run:

### Bulma:
[Bulma](bulma.io) is used for CSS formatting, but it is occasionally overwritten to make things fit better. It is used for hero banners, buttons, navbars, and more. While it does have some limitations for this project, the known issues have been fixed to have a flawless experience for the current version.

### Font Awesome:
[Font Awesome](fontawesome.com) provides certain icons for .zip, .pdf, etc when uploading a file and its image cannot be displayed.

## Bugs
### Current:
None

### Fixed:
- [x] Profile page's table caused rendering issues with the background color being cut off halfway horizontally.
- [x] Message that file was uploaded despite file not being stored.
- [x] Retrieval was impossible due to a type in the following route:
` @main.route('/downloaded/<int:file_id>')`
- [x] Image showing outside the upload box
- [x] Uploaded file's name drags outside of the container
- [x] Uploaded file's name cuts off inside the container and is uneven
- [x] Uploaded file's name doesn't show up
- [x] File could not be attached to uploader
- [x] Email could not be changed due to incorrect checking of the form items in the following route:
`@auth.route('/email_change', methods=['POST'])`

## Quick Disclaimer:
This may become an opensource project for file storage with no size limit <ins>**if feasible**.</ins>
This is originally just a project for Harvard's CS50x and should not be taken as an actual upcoming website.

## Tech Stack
- Python (Flask)
- JavaScript
- HTML, Jinja
- CSS (Bulma included)
- SQLite (Through SQLAlchemy)

## Install Instructions
1. Clone the repository
2. Cd into project/flask_auth_app/project using:\
`cd project/flask_auth_app/project`
3. Download dependencies using:\
`pip install -r requirements.txt`
4. Cd back into project/flask_auth_app using:\
`cd ..`
5. Run the following command: \
`source auth/bin/activate`
6. Export flask app and set debug mode to 1 using:\
`export FLASK_APP=project`\
`export FLASK_DEBUG=1`
7. Run flask using:\
`flask run`
