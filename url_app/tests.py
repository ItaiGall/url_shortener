import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .url_shortener import shorten_url


class UrlViewSetTest(TestCase):
    #Test for CREATE/POST
    def setUp(self):
        data = json.dumps({
            "full_url": "https://www.weather.com"
        })
        client = APIClient()
        response = client.post('/create', data=data, content_type='application/json')
        #save short_url for other tests
        self.short_url = f"http://localhost:8000/s/{response.data['short_url']}"
        self.full_url = response.data['full_url']
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check to see if the url was created
        self.assertEqual(response.data['full_url'], 'https://www.weather.com')
        # Check to see if the url was created
        self.assertTrue(response.data['short_url'])
        # Check that short_url is a string
        self.assertEqual(type(response.data['short_url']), str)
        # Check that short_url has a length of 8
        self.assertEqual(len(response.data['short_url']), 8)

    #test successful redirect of short_url call
    def test_short_url_redirect_successful(self):
        client = APIClient()
        response = client.get(self.short_url)
        #Check if redirect was successful (status 302) - from django documentation
        self.assertRedirects(response,
                             self.full_url,
                             status_code=302,
                             target_status_code=200,
                             msg_prefix="",
                             fetch_redirect_response=False)

    #As for my understanding, a test "for non-existing short url"
    #means to test that if the wrong short_url has been provided for redirection
    #a 404 status should be returned.
    def test_if_non_existent_short_url(self):
        client = APIClient()
        while True:
            new_url = shorten_url()
            if new_url != self.short_url:
                break
        new_url = f"http://localhost:8000/s/{new_url}"
        response = client.get(new_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #check if duplicate url input returns the existing value
    def test_prevent_duplicate_full_url(self):
        data = json.dumps({
            "full_url": self.full_url
        })
        client = APIClient()
        response = client.post('/create', data=data, content_type='application/json')
        #response comes in a complex datastructure, required trial and error
        new_short_url = list(response.data[0].items())[2][1]
        self.assertEqual(new_short_url, self.short_url[-8:])



