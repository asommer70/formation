from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os

User = get_user_model()


def inbox_notification(input):
    subject = 'New {} created'.format(input.form.name)
    from_email = 'formation@thehoick.com'
    to = input.route_holder.email

    if not input.route_sender:
        sender = input.user.username
    else:
        sender = input.route_sender.username

    text_content = "A {} has been sent to you by {}. \n\nClick here to open: {}\n\n".format(
        input.form.name,
        sender,
        'https://formation.thehoick.com/inbox/' + str(input.id)
    )

    # Read the email template.
    # email_template = open(os.path.join(settings.BASE_DIR, 'supply_request/templates/email/new_supply_request.html'), 'r')
    # email_templatemodeslpf.seek(0)
    # html_content = email_template.read()

    # html_content = html_content.replace('[USERNAME]', manager.email)
    # html_content = html_content.replace('[CREATED_AT]', supply_request.created_at.strftime('%m/%d/%Y %I:%M:%S'))
    # html_content = html_content.replace('[ID]', str(supply_request.id))

    html_content = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en" style="background:#ffffff!important">
      <head>
        <title>Formation Notification</title>
      </head>
      <body>
        <p>Hello {},</p>
        <p><br/></p>
        <p>"A {} has been sent to you by {}.</p>
        <p><br/></p>
        <p>Click here to open: {}</p>
        <p><br/></p>
        <p>Thanks, and have a great day!</p>
      </body>
    </html>
'''.format(
      input.route_holder.username,
      input.form.name,
      sender,
      'https://formation.thehoick.com/inbox/' + str(input.id)
    )

    # email_template.close()

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def route_notification(input):
    print('input.route_holder:', input.route_holder)
    if input.status == 'archived':
        holder = 'archived'
    else:
        holder = input.route_holder.username
        
    subject = 'Form {} was sent to {}'.format(
        input.form.name,
        holder
    )
    from_email = 'formation@thehoick.com'
    to = input.user.email

    text_content = "Form {} created at {} was sent to {}. \n\nClick here to open: {}\n\n".format(
        input.form.name,
        input.created_at,
        holder,
        'https://formation.thehoick.com/inbox/' + str(input.id)
    )

    html_content = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en" style="background:#ffffff!important">
      <head>
        <title>Formation Notification</title>
      </head>
      <body>
        <p>Hello {},</p>
        <p><br/></p>
        <p>"Form {} created at {} was sent to {}.</p>
        <p><br/></p>
        <p>Click here to open: {}</p>
        <p><br/></p>
        <p>Thanks, and have a great day!</p>
      </body>
    </html>
'''.format(
      input.user.username,
      input.form.name,
      input.created_at,
      holder,
      'https://formation.thehoick.com/inbox/' + str(input.id)
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

