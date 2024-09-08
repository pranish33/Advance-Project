#import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from frontend.models import Doctor,Appointment
from django.urls import reverse
from django.test import LiveServerTestCase, TestCase, Client
import requests
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime, timedelta


""" 
    Testing UI using Selenium 
    Given: We will be giving the parameters same as in browser 
    When: Correct Credentials used in same as UI
    Then: User can log in and see the successfully
"""
class SeleniumUITestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.browser.implicitly_wait(10)  # Wait up to 10 seconds for elements to be available
        self.server_url = 'http://localhost:8000' 

    def tearDown(self):
        self.browser.quit()
    
    # check the index is loaded correctly or not
    def test_homepage(self):
        self.browser.get(f'{self.server_url}/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('What Does Pink Eye Look Like?', self.browser.page_source)

    # check the home page is loaded correctly or not for patient
    def test_patienthome(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('patient1@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('patient1', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/home/')
        self.assertIn('Patient Home', self.browser.title)
        self.assertIn('Healthy Tips', self.browser.page_source)

    # check the about us page
    def test_aboutpage(self):
        self.browser.get(f'{self.server_url}/about/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('The main motive', self.browser.page_source)

    # check the login using valid username and password
    def test_login_valid(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('patient1@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('patient1', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.assertIn('Patient Home', self.browser.title)
        self.assertIn('Healthy Tips', self.browser.page_source)

    # check the login using invalid username and password
    def test_login_invalid(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('invalid@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('password', Keys.RETURN)
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('Invalid credentials.', self.browser.page_source)
    
    # check the chatroom page popup
    def test_chatroom_view(self):
        self.browser.get(f'{self.server_url}/chatroom/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('Personal Health Assistant!', self.browser.page_source)
    
    # check the View Doctor page from admin perspective
    def test_adminviewDoctor(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('tjiten123@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('zeyrox1@', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/adminviewDoctor/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('ALL DOCTORS', self.browser.page_source)

    # check the View appointment from admin perspective
    def test_adminviewAppointment(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('tjiten123@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('zeyrox1@', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/adminviewAppointment/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('PREVIOUS APPIONTMENTS', self.browser.page_source)

    # check the View profile page from patient perspective
    def test_profile(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('patient1@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('patient1', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/profile/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('Phone Number', self.browser.page_source)

    # check the View appointment page from patient perspective
    def test_view_appointments_patient(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('patient1@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('patient1', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/viewappointments/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('APPOINTMENTS', self.browser.page_source)

    # check the View appointment page from doctor perspective
    def test_view_appointments_doctor(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('alhan@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('alhan', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/viewappointments/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('YOU HAVE APPOINTMENTS WITH:', self.browser.page_source)

    # check the View health record page from patient perspective
    def test_view_health_records_patient(self):
        self.browser.get(f'{self.server_url}/login/')
        self.browser.find_element(By.NAME, 'email').send_keys('patient1@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('patient1', Keys.RETURN)
        WebDriverWait(self.browser, 10).until(EC.url_changes(f'{self.server_url}/login/'))
        self.browser.get(f'{self.server_url}/viewhealthrecords/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('HEALTH RECORDS', self.browser.page_source)

    # check the contact page
    def test_contactus(self):
        self.browser.get(f'{self.server_url}/contact/')
        self.assertIn('HealthCare', self.browser.title)
        self.assertIn('ll never share your email with anyone else.', self.browser.page_source)

    # checking the available time slot returned on api 
    def test_get_available_time_slots(self):
        date = '2024-09-12'
        doctor_email = 'baburam@gmail.com'
        url = f'{self.server_url}/get-available-time-slots/?date={date}&doctor_email={doctor_email}'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_slots = ['10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30']
        self.assertEqual(response_data['timeSlots'], expected_slots)


""" 
    Functional Testing of views methods
    Given: We will be giving the parameters required for the methods
    When: Correct paramters provided
    Then: User can get the correct template and peform tasks 
"""
class FunctionalTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create groups
        self.patient_group = Group.objects.create(name='Patient')
        self.doctor_group = Group.objects.create(name='Doctor')
        self.admin_group = Group.objects.create(name='Admin')

        # Create users
        self.patient_user = User.objects.create_user(username='patient@gmail.com', password='password', email='patient@gmail.com', first_name='Patient')
        self.patient_group.user_set.add(self.patient_user)

        self.doctor_user = User.objects.create_user(username='doctor@gmail.com', password='password', email='doctor@gmail.com', first_name='Doctor')
        self.doctor_group.user_set.add(self.doctor_user)

        self.admin_user = User.objects.create_user(username='admin@gmail.com', password='password', email='admin@gmail.com', first_name='Admin', is_staff=True)
        self.admin_group.user_set.add(self.admin_user)

    def test_homepage(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_patienthome(self):
        self.client.login(username='patient@gmail.com', password='password')
        response = self.client.get(reverse('patienthome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patienthome.html')

    def test_aboutpage(self):
        response = self.client.get(reverse('aboutpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_loginpage_valid(self):
        response = self.client.post(reverse('loginpage'), {
            'email': 'patient@gmail.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patienthome'))

    def test_loginpage_invalid(self):
        response = self.client.post(reverse('loginpage'), {
            'email': 'invalid@gmail.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginpage'))

    def test_createaccountpage(self):
        response = self.client.post(reverse('createaccountpage'), {
            'name': 'New Patient',
            'email': 'newpatient@gmail.com',
            'password': 'password',
            'repeatpassword': 'password',
            'gender': 'Male',
            'phonenumber': '1234567890',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginpage'))

    def test_chatroom_view(self):
        url = reverse('chatroom')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatroom.html')
        self.assertContains(response, "Chatroom")

    def test_adminaddDoctor(self):
        self.client.login(username='admin@gmail.com', password='password')
        response = self.client.post(reverse('adminaddDoctor'), {
            'name': 'Dr. Smith',
            'email': 'drsmith@gmail.com',
            'password': 'password',
            'repeatpasssword': 'password',
            'gender': 'Male',
            'phonenumber': '1234567890',
            'address': '123 Street',
            'licenseNo': 'ABC123',
            'specialization': 'Cardiology',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminviewDoctor'))

    def test_adminviewDoctor(self):
        self.client.login(username='admin@gmail.com', password='password')
        response = self.client.get(reverse('adminviewDoctor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminviewDoctors.html')

    def test_admin_delete_doctor(self):
        doctor = Doctor.objects.create(name='Dr. Smith', email='drsmith@gmail.com', gender='Male', phonenumber='1234567890', address='123 Street', licenseNo='ABC123', specialization='Cardiology')
        user = User.objects.create_user(username='drsmith@gmail.com', email='drsmith@gmail.com', password='password')
        self.client.login(username='admin@gmail.com', password='password')
        response = self.client.get(reverse('admin_delete_doctor', args=[doctor.id, doctor.email]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminviewDoctor'))

    def test_patient_delete_appointment(self):
        appointment = Appointment.objects.create(doctorname='Dr. Smith', doctoremail='drsmith@gmail.com', patientname='Patient', patientemail='patient@gmail.com', appointmentdate=timezone.now().date(), appointment_time='10:00', symptoms='Cough', status=True)
        self.client.login(username='patient@gmail.com', password='password')
        response = self.client.get(reverse('patient_delete_appointment', args=[appointment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('viewappointments'))

    def test_adminviewAppointment(self):
        self.client.login(username='admin@gmail.com', password='password')
        response = self.client.get(reverse('adminviewAppointment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminviewappointments.html')

    def test_profile(self):
        self.client.login(username='patient@gmail.com', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pateintprofile.html')

    def test_make_appointments(self):
        self.client.login(username='patient@gmail.com', password='password')
        response = self.client.post(reverse('makeappointments'), {
            'doctoremail': 'drsmith@gmail.com',
            'doctorname': 'Dr. Smith',
            'patientname': 'Patient',
            'patientemail': 'patient@gmail.com',
            'appointmentdate': timezone.now().date(),
            'timeslot': '10:00',
            'symptoms': 'Cough',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('makeappointments'))

    def test_view_appointments_patient(self):
        self.client.login(username='patient@gmail.com', password='password')
        response = self.client.get(reverse('viewappointments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patientviewappointments.html')

    def test_view_appointments_doctor(self):
        self.client.login(username='doctor@gmail.com', password='password')
        response = self.client.get(reverse('viewappointments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctorviewappointment.html')

    def test_view_health_records_patient(self):
        self.client.login(username='patient@gmail.com', password='password')
        response = self.client.get(reverse('viewhealthrecords'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pateintviewrecord.html')

    def test_view_health_records_doctor(self):
        self.client.login(username='doctor@gmail.com', password='password')
        response = self.client.get(reverse('viewhealthrecords'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctorviewappointment.html')

    def test_contactus(self):
        response = self.client.post(reverse('contactus'), {
            'contactname': 'John Doe',
            'contactphonenumber': '1234567890',
            'contactemail': 'johndoe@gmail.com',
            'message': 'This is a test message.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactus.html')

""" 
    Functional Testing of get_available_time_slots API
    Given: We will be giving the parameters required for the methods
    When: Correct paramters provided
    Then: User can get the JSON response or not
"""
class FunctionalTestForGetAvailableSlot(TestCase):
    def setUp(self):
        # Set up the test client
        self.client = Client()
        
        # Create test data
        self.date = timezone.now().date() + timedelta(days=1)
        self.doctor_email = 'alhan@gmail.com'
        self.booked_times = ['10:00', '11:00']

        # Create appointments for the doctor
        for time_slot in self.booked_times:
            Appointment.objects.create(
                doctorname='Alhan',
                doctoremail=self.doctor_email,
                patientname='Patient Test',
                patientemail='patient@gmail.com',
                appointmentdate=self.date,
                appointment_time=datetime.strptime(time_slot, '%H:%M').time(),
                symptoms='Test Symptoms',
                status=True,
                prescription=''
            )

    # Check the method to get the JSON response
    def test_get_available_time_slots(self):
        url = reverse('get_available_time_slots')
        response = self.client.get(url, {'date': self.date, 'doctor_email': self.doctor_email})
        self.assertEqual(response['Content-Type'], 'application/json')
        response_data = response.json()
        expected_slots = ['10:30', '11:30', '12:00', '12:30', '13:00', '13:30']
        self.assertEqual(response_data['timeSlots'], expected_slots)

    def tearDown(self):
        # Clean up any data
        Appointment.objects.all().delete()