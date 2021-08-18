from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get('/')

    # не работает
    @task
    def profile(self):
        self.client.get('/auth/edit/')

    @task
    def products(self):
        self.client.get("/products/")

    # не работает
    @task
    def login(self):
        self.client.post('/auth/login/', json={'username': 'admin', 'password': '123'})

    # не работает
    @task
    def logout(self):
        self.client.post('/auth/logout/', json={'username': 'admin', 'password': '123'})
