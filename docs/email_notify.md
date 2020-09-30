# Email Notification

`CloudTDMS` provides email notifications for Data Profiling reports. Generating a profiling report for a data-set
can be time consuming. You can let `CloudTDMS` notify you when the reports are generated. 

In order to register for email notifications, You need to provide SMTP server credentials in `config_default.yaml` file.

### SMTP Configuration
Following values are required to register for email notification:

1. **to :** Takes receiver email address as value, Receiver email is the one to which notification must be sent.
2. **from :** Takes sender email address as value, Sender email is the one which is used to send the email.
3. **smtp_host :** Takes SMTP Host address as value e.g `smtp.gmail.com`
4. **smtp_port :** Set your SMTP port here, such as 587, 465, 25, 2525
5. **smtp_ssl :** This is a boolean flag to specify If SSL connection is to be used for sending emails set this `True` 
                  if `smtp_port` is 465 else make it `False` for 587 etc.
6. **username :** Takes SMTP username or login id as value
7. **password :** Takes SMTP password as value
8. **subject :** Set the subject of the email by default its `Data Profiling`

### How to Use GMAIL as SMTP server

In order to use `GMAIL` as `SMTP` server, You need to first generate an `app-password` for your Gmail account.
An app password is a 16-digit passcode that gives a non-Google app or device permission to access your Google Account. App passwords can only be used with accounts that have 2-Step Verification turned on.


**Create and use app passwords**

>**Note :** If you use 2-Step-Verification and are seeing a 'password incorrect' error when trying to access your Google Account, an app password may solve the problem.

1. Go to your [Google Account](https://myaccount.google.com).
2. On the left navigation panel, choose Security.
3. On the 'Signing in to Google' panel, choose App passwords. If you don’t see this option:
   
   - 2-Step Verification is not set up for your account
   - 2-Step Verification is set up for security keys only
   - Your account is through work, school or other organisation
   - You’ve turned on Advanced Protection for your account
4. At the bottom, choose Select app and choose the app that you’re using.
5. Choose Select device and choose the device that you're using.
6. Choose Generate.
7. Follow the instructions to enter the app password. The app password is the 16-character code in the yellow bar on your device.
8. Choose Done.

For more details about Google App Password check out the following link [Google Support](https://support.google.com/mail/answer/185833)

Once you have generated `App-Password` for your Gmail Account, You can use following `config_default.yaml` values

```yaml
email:
  to: "<EMAIL-ADDRESS-TO-WHICH-NOTIFICATION-MUST-BE-SENT>" 
  from: "<YOUR-GMAIL-EMAIL-ADDRESS>"
  smtp_host: "smtp.gmail.com"
  smtp_port: 465
  smtp_ssl: True
  username: "<YOUR-GMAIL-EMAIL-ADDRESS>"
  password: "<GENERATE-APP-PASSWORD>"
  subject: "Data Profiling"
```

### Using Third Party SMTP server 
Many third party SMTP service providers are available such as [MailJet](https://mailjet.com), [SendPulse](https://sendpulse.com) etc
You can use any SMTP relay settings provided by the service provider to register for email notification. Here we shall
describe the `MailJet` process.

1. Register for an account on Mailjet website [MailJet](https://app.mailjet.com/signup?lang=en_US)
2. Login to your MailJet account
3. Click on **Transactional** in the top navigation bar, A drop down menu will appear
4. Select `SMTP` from the drop down menu list
5. You will have your `SMTP` relay setting available to you.

Use the MailJet settings to configure you `CloudTDMS` email notification.

>**Note :** You should use the same email address with which you login into mailjet account as `from` email_address in
>`config_default.yaml` file 

```yaml
email:
  to: "<EMAIL-ADDRESS-TO-WHICH-NOTIFICATION-MUST-BE-SENT>" 
  from: "<YOUR-MAILJET-EMAIL-ADDRESS-WITH-WHICH-YOU-LOGIN>"
  smtp_host: "<YOUR-MAILJET-SMTP-SERVER>"
  smtp_port: 465
  smtp_ssl: True
  username: "<YOUR-MAILJET-USERNAME>"
  password: "<YOUR-MAILJET-PASSWORD>"
  subject: "Data Profiling"
```
