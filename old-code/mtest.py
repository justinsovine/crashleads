import mandrill
try:
    mandrill_client = mandrill.Mandrill('W9qNf7N2JPjLjjcjJM7QMQ')
    message = {
     'from_email': 'grabreports@smagno.com',
     'from_name': 'Grab Reports',
     'headers': {'Reply-To': 'grabreports@smagno.com'},
     'text': 'Hey, Justin. What\'s up?',
     'html': '<p>Hey, Justin. What\'s up?</p>',
     'to': [{'email': 'justinsovine@gmail.com',
             'name': 'Justin Sovine',
             'type': 'to'},
            {'email': 'jsovine@huc.edu',
             'name': 'Justin Sovine',
             'type': 'to'}],
     'subject': 'This is a test of the Mandrill system',
     'track_clicks': True,
     'track_opens': True,
     'url_strip_qs': None
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')

except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
    raise
