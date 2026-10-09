from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string


class KoraFrontendTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check(self):
        response = self.client.get(reverse('health_check'), HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_home_page_renders_successfully(self):
        response = self.client.get(reverse('home'), HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Kora')
        self.assertContains(response, 'Afrobeat')

    def test_search_page_empty_and_query(self):
        # Empty query
        response_empty = self.client.get(reverse('search'), HTTP_HOST='127.0.0.1')
        self.assertEqual(response_empty.status_code, 200)
        self.assertTemplateUsed(response_empty, 'search.html')
        self.assertContains(response_empty, 'Discover Global Soundscapes')

        # With query
        response_query = self.client.get(reverse('search') + '?q=Burna', HTTP_HOST='127.0.0.1')
        self.assertEqual(response_query.status_code, 200)
        self.assertContains(response_query, 'Search results for')

    def test_profile_page_fallback(self):
        response = self.client.get(reverse('profile', args=['unknown_id']), HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_login_and_signup_pages(self):
        login_resp = self.client.get(reverse('login'), HTTP_HOST='127.0.0.1')
        self.assertEqual(login_resp.status_code, 200)
        self.assertTemplateUsed(login_resp, 'login.html')
        self.assertContains(login_resp, 'Username')
        self.assertContains(login_resp, 'Password')

        signup_resp = self.client.get(reverse('signup'), HTTP_HOST='127.0.0.1')
        self.assertEqual(signup_resp.status_code, 200)
        self.assertTemplateUsed(signup_resp, 'signup.html')
        self.assertContains(signup_resp, 'Confirm Password')

    def test_music_template_renders(self):
        req = self.client.get('/', HTTP_HOST='127.0.0.1').wsgi_request
        html = render_to_string('music.html', {'request': req})
        self.assertIn('Now Playing', html)
        self.assertIn('African Lofi Experience', html)

    def test_music_player_route_and_audio_sources(self):
        response = self.client.get(reverse('music_player'), HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music.html')
        self.assertContains(response, 'African Lofi Experience')
        self.assertContains(response, 'global-audio')
        self.assertContains(response, 'african_lofi_experience.wav')

    def test_signup_with_avatar_preset_and_populate_on_login(self):
        # Signup with an avatar preset
        preset_url = "https://images.unsplash.com/photo-test-preset.jpg"
        response = self.client.post(reverse('signup'), {
            'username': 'afrobeattester',
            'email': 'tester@example.com',
            'password': 'password123',
            'repeat_password': 'password123',
            'avatar_preset': preset_url
        }, HTTP_HOST='127.0.0.1', follow=True)
        self.assertEqual(response.status_code, 200)

        # Check that user is logged in and avatar is populated in response
        self.assertContains(response, 'afrobeattester')
        self.assertContains(response, preset_url)

        # Logout and log back in to verify avatar is populated anytime they sign in
        self.client.logout()
        login_resp = self.client.post(reverse('login'), {
            'username': 'afrobeattester',
            'password': 'password123',
        }, HTTP_HOST='127.0.0.1', follow=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertContains(login_resp, preset_url)
        self.assertContains(login_resp, 'user-avatar-img')

    def test_signup_with_avatar_file_upload(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        avatar_file = SimpleUploadedFile("avatar.jpg", b"fake-image-bytes", content_type="image/jpeg")
        response = self.client.post(reverse('signup'), {
            'username': 'phototester',
            'email': 'photo@example.com',
            'password': 'password123',
            'repeat_password': 'password123',
            'avatar': avatar_file
        }, HTTP_HOST='127.0.0.1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'phototester')
        self.assertContains(response, 'user-avatar-img')

