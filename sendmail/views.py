from sendmail import app,mail
from flask_mail import Message
from flask import request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


st = logging.StreamHandler()
st.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s :: %(message)s")
st.setFormatter(formatter)
logger.addHandler(st)
from jinja2 import Template



@app.route('/')
def index():
    return Template("<link rel='shortcut icon' href='/static/img/favicon.png' >" +
                    "<pre>curl --data 'subject=&lt;subject&gt;&body=&lt;body&gt;" +
                    "&recipients=&lt;recipient[@synchrotron.org.au]&gt;[,one][,two][,etc...]' " +
                    "hostAddress:Port/sendmail/</pre>").render()

@app.route('/sendmail/', methods=['POST'])
def post_the_mail():
    # required to send message
    # subject<string>, body<string>, recipients<list>
    subject_string = str(request.form.get('subject'))
    body_string = str(request.form.get('body'))
    tmp_list = str(request.form.get('recipients')).split(',')
    from_string = str(request.form.get('from'))
    if not from_string:
        from_string = 'email_robot'

    recipient_list = []
    for recipient in tmp_list:
        r = recipient
        if '@' not in recipient:
            r = r + '@synchrotron.org.au'
        recipient_list.append(r)

    logger.info("%s, %s, %s" % (subject_string, body_string, tmp_list))

    with mail.connect() as con:
        logger.info('Sending Email Message to the following users: ')
        for user in recipient_list:
            logger.info(user)
            msg = Message(subject=subject_string,
                          sender=from_string + '@synchrotron.org.au',
                          html=body_string,
                          recipients=[user])
            con.send(msg)

    logger.info("Email Sent, you don't have anymore messages!")
    return "Done! "
