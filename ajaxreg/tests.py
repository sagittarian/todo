from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail

import json

class RegTest(TestCase):
    urls = 'ajaxreg.urls'
    fixtures = ['test.json']


    def setUp(self):
        self.infourl = reverse('ajaxreg_info')
        self.registerurl = reverse('ajaxreg_register')
        self.loginurl = reverse('ajaxreg_login')
        self.logouturl = reverse('ajaxreg_logout')
        self.pwchangeurl = reverse('ajaxreg_password_change')
        self.pwreseturl = reverse('ajaxreg_password_reset')
        self.uname = 'Reinhardt'
        self.email = 'reinhardt@example.com'
        self.pw = 'jazz123'


    def get_logged_in_username(self):
        response = self.client.get(self.infourl)
        d = json.loads(response.content)
        self.assertIsNone(d['error'])
        return d['username']


    def test_info_anonymous(self):
        uname = self.get_logged_in_username()
        self.assertIsNone(uname)


    def test_info_authenticated(self):
        self.client.login(username='admin', password='admin')
        uname = self.get_logged_in_username()
        self.assertEqual(uname, 'admin')


    def test_register(self):
        response = self.client.post(
            self.registerurl,
            {'username': self.uname, 'email': self.email, 'password': self.pw})
        d = json.loads(response.content)
        self.assertEqual(d['username'], self.uname)
        self.assertIsNone(d['error'])
        self.assertEqual(self.uname, self.get_logged_in_username())


    def test_login(self):
        uname = 'admin'
        response = self.client.post(
            self.loginurl, {'username': uname, 'password': 'admin'})
        d = json.loads(response.content)
        self.assertIsNone(d['error'])
        self.assertEqual(d['username'], uname)
        self.assertEqual(uname, self.get_logged_in_username())


    def test_login_bad_pw(self):
        uname = 'admin'
        response = self.client.post(
            self.loginurl, {'username': uname, 'password': 'something'})
        d = json.loads(response.content)
        self.assertIsNotNone(d['error'])
        self.assertIsNone(d['username'])
        self.assertIsNone(self.get_logged_in_username())


    def test_logout(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.logouturl)
        d = json.loads(response.content)
        self.assertIsNone(d['error'])


    def test_password_change(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.pwchangeurl, {'password': self.pw})
        d = json.loads(response.content)
        self.assertIsNone(d['error'])
        self.client.logout()
        self.assertIsNone(self.get_logged_in_username())
        response = self.client.post(
            self.loginurl, {'username': 'admin', 'password': self.pw})
        d = json.loads(response.content)
        self.assertIsNone(d['error'])
        self.assertEqual(d['username'], 'admin')
        self.assertEqual('admin', self.get_logged_in_username())


    def test_password_reset(self):
        response = self.client.post(self.pwreseturl, {'username': 'admin'})
        d = json.loads(response.content)
        self.assertIsNotNone(d['status'])
        self.assertIsNone(d['error'])
        self.assertEqual(len(mail.outbox), 1)

