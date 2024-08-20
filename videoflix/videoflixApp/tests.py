from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
#from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserFilmEvaluation, Video

User = get_user_model()

class LoginViewTests(APITestCase):

    def setUp(self):
        # Erstellt einen Benutzer, der für den Test verwendet wird.
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.user.is_verified = True  # Angenommen, das Feld `is_verified` existiert.
        self.user.save()
        self.url = '/login/'  # Setze die richtige URL für den Login-Endpunkt

    def test_login_success(self):
        """
        Testet einen erfolgreichen Login-Versuch.
        """
        data = {'username':'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['user_id'], self.user.pk)

    def test_login_failed_due_to_unverified_account(self):
        """
        Testet einen fehlgeschlagenen Login-Versuch, weil das Konto nicht verifiziert ist.
        """
        # Markiere das Konto als nicht verifiziert
        self.user.is_verified = False
        self.user.save()
        data = {'username':'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(self.url, data, format='json')
        #self.assertEqual(response.status_code, status.status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(response.data['status'])
        self.assertEqual(response.data['status'], 'Account not yet verified')

    def test_login_failed_due_to_invalid_credentials(self):
        """
        Testet einen fehlgeschlagenen Login-Versuch aufgrund ungültiger Anmeldedaten.
        """
        data = {'username':'testuser@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'error')

    def test_login_failed_due_to_missing_fields(self):
        """
        Testet einen fehlgeschlagenen Login-Versuch aufgrund fehlender Felder.
        """
        data = {'username': 'testuser'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('detail', response.data)


class RegisterViewTests(APITestCase):
     
    
    def setUp(self):
        self.url = reverse('auth_register')  # Setze die richtige URL für den Registrierung-Endpunkt
    
    def test_register_success(self):
        """
        Testet eine erfolgreiche Registrierung eines neuen Benutzers.
        """
        data = {
            'username': 'newuser',
            'password': 'Testpass123!',
            'password2': 'Testpass123!',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_data']['username'], data['username'])
        self.assertIn('access_token', response.data)
        
        # Überprüfe, ob der Benutzer in der Datenbank gespeichert wurde
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(user.email, data['email'])

    def test_register_password_mismatch(self):
        """
        Testet die Registrierung, wenn die Passwörter nicht übereinstimmen.
        """
        data = {
            'username': 'newuser',
            'password': 'Testpass123!',
            'password2': 'Wrongpass123!',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "Password fields didn't match.")

    def test_register_duplicate_email(self):
        """
        Testet die Registrierung mit einer E-Mail, die bereits existiert.
        """
        # Erstelle einen existierenden Benutzer
        User.objects.create_user(username='existinguser', password='Testpass123!', email='existinguser@example.com')
        
        data = {
            'username': 'newuser',
            'password': 'Testpass123!',
            'password2': 'Testpass123!',
            'email': 'existinguser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "This field must be unique.")

    def test_register_missing_fields(self):
        """
        Testet die Registrierung mit fehlenden Feldern.
        """
        data = {
            'username': 'newuser'
            # Fehlende Felder wie password, password2 und email
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)
        
class VideoEvaluationTests(APITestCase):

    def setUp(self):
        # Benutzer erstellen und authentifizieren
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Beispiel-Video erstellen
        self.video = Video.objects.create(title='Test Video')
        
        # URLs festlegen
        self.url = reverse('video-evaluation')  # Stelle sicher, dass der URL-Namen korrekt ist
    
    def test_get_evaluations(self):
        """
        Testet das Abrufen aller Bewertungen des aktuellen Benutzers.
        """
        # Beispielhafte Bewertung erstellen
        UserFilmEvaluation.objects.create(user=self.user, video=self.video, evaluation=5)
        
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Es sollte eine Bewertung zurückgegeben werden
    
    def test_post_evaluation(self):
        """
        Testet das Erstellen einer neuen Bewertung für ein Video.
        """
        data = {'filmId': self.video.id, 'eval': 4}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Es sollte eine Bewertung zurückgegeben werden
        
        # Überprüfen, ob die Bewertung korrekt gespeichert wurde
        evaluation = UserFilmEvaluation.objects.get(user=self.user, video=self.video)
        self.assertEqual(evaluation.evaluation, 4)

    def test_post_evaluation_video_not_found(self):
        """
        Testet das Erstellen einer Bewertung für ein nicht existierendes Video.
        """
        data = {'filmId': 999, 'eval': 2}  # Ungültige Video-ID
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('status', response.data)
    
    def test_put_evaluation(self):
        """
        Testet das Aktualisieren einer bestehenden Bewertung.
        """
        # Beispielhafte Bewertung erstellen
        UserFilmEvaluation.objects.create(user=self.user, video=self.video, evaluation=3)
        
        # Bewertung aktualisieren
        data = {'filmId': self.video.id, 'eval': 5}
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Überprüfen, ob die Bewertung aktualisiert wurde
        evaluation = UserFilmEvaluation.objects.get(user=self.user, video=self.video)
        self.assertEqual(evaluation.evaluation, 5)
    
    def test_put_evaluation_not_found(self):
        """
        Testet das Aktualisieren einer nicht existierenden Bewertung.
        """
        data = {'filmId': self.video.id, 'eval': 2}  # Keine vorhandene Bewertung
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
        print(response.data)    
        self.assertIn('status', response.data)       

        