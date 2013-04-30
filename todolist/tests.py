from models import LABEL_MAX_LEN

from django.test import TestCase
from django.core.urlresolvers import reverse

import json
import random

class TodolistTest(TestCase):
    urls = 'todolist.urls'
    fixtures = ['test.json']

    def setUp(self):
        self.getlisturl = reverse('getlist')
        self.addurl = reverse('additem')
        self.delurl = reverse('delitem')
        self.modurl = reverse('moditem')
        self.label = hex(random.randint(0x10000000, 0xffffffff))

    def login(self):
        self.client.login(username='admin', password='admin')

    def test_list_for_unauthenticated_user(self):
        response = self.client.get(self.getlisturl)
        d = json.loads(response.content)
        self.assertIn('error', d)
        self.assertIsNotNone(d['error'])
        self.assertNotIn('items', d)

    def test_list_for_authenticated_user(self):
        self.login()
        response = self.client.get(self.getlisturl)
        d = json.loads(response.content)
        self.assertIn('error', d)
        self.assertIsNone(d['error'])
        self.assertIn('items', d)
        self.assertIsInstance(d['items'], list)
        for item in d['items']:
            self.assertIn('id', item)
            self.assertIn('label', item)
            self.assertIn('priority', item)

    def get_items(self):
        response = self.client.get(self.getlisturl)
        d = json.loads(response.content)
        return d['items']

    def add_item(self, label, priority=None):
        data = {'label': label}
        if priority is not None:
            data['priority'] = priority
        response = self.client.post(self.addurl, data)
        return json.loads(response.content)

    def test_add_item(self):
        self.login()

        d = self.add_item(self.label)
        self.assertIn('error', d)
        self.assertIsNone(d['error'])
        self.assertIn('id', d)

        for item in self.get_items():
            if item['label'] == self.label:
                break
        else:
            raise KeyError('{} not found in todolist'.format(self.label))

    def test_del_item(self):
        self.login()
        id = self.add_item(self.label)['id']

        response = self.client.post(self.delurl, {'id': id})
        d = json.loads(response.content)
        self.assertIn('error', d)
        self.assertIsNone(d['error'])

        for item in self.get_items():
            self.assertNotEqual(item['id'], id)

    def test_modify_item(self):
        self.login()
        id = self.add_item(self.label)['id']
        newlabel = 'My new label'
        newpriority = 0
        self.assertTrue(any(self.label == item['label'] and id == item['id']
                            for item in self.get_items()))

        response = self.client.post(self.modurl,
                               {'id': id, 'label': newlabel,
                                'priority': newpriority})
        d = json.loads(response.content)
        self.assertIsNone(d['error'])

        for item in self.get_items():
            if item['id'] == id:
                self.assertEqual(item['label'], newlabel)
                self.assertEqual(item['priority'], newpriority)
                break
        else:
            raise KeyError('Modified label not found')

    def test_add_long_label(self):
        self.login()
        s = ('This is a long label that goes on and on '
             'and on and on and it is definitely more than '
             '255 characters, I mean it just goes on and on '
             'and on and on, it just doesn\'t seem to stop '
             'no ending in sight, more and more, and when will '
             'it end, i mean, c\'mon, it\'s gotta end sometime, '
             'I can\'t keep typing forever')
        d = self.add_item(s)
        self.assertIsNone(d['error'])

        for item in self.get_items():
            if item['id'] == d['id']:
                self.assertEqual(item['label'], s[:LABEL_MAX_LEN])
                break
        else:
            raise KeyError('Long label not added')

    def test_add_invalid_priority(self):
        self.login()
        d = self.add_item(self.label, 'chocolate')
        self.assertIsNotNone(d['error'])
