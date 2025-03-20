##  **NoteFlow **

###  **Project Description**
**NoteFlow** is a platform for sharing educational materials at SDU University. It allows users to upload, search, filter, rate, and discuss study materials across various subjects. The platform also features **a chat system** for communication between users.
Key Features:
 
    Material Uploading: Users can upload educational materials, which are linked to their accounts.
    
    Tagging System: Uploaded materials can be tagged with predefined tags to improve searchability.
        
    Chat/Group Chat: Users can have conversations because of websocket technology

    Private: Users can authenticate only by mail -> @sdu.edu.kz, so its only for SDU University students 
---

## **Installation & Setup**
### **1️) Clone the Repository**
```bash
git clone https://github.com/nurmek51/NoteFlow.git
cd NoteFlow
```

### **2) Create and Activate a Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### **3) Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️)Configure Database**
- By default, the project uses **SQLite**.
- To switch to **PostgreSQL**, update `DATABASES` in `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'note_flow_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### **5️) Configure Redis (for WebSockets & Caching)**
- Install **Redis** (if not installed):
```bash
sudo apt install redis
```
- Ensure Redis is running:
```bash
redis-server
```
- Update `config/settings.py`:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### **6) Apply Migrations**
```bash
python manage.py migrate
```

### **7️) Add data to .env**
But you can not upload materials, because locally you dont registered to aws s3
```bash
SECRET_KEY=secret_key_you_know
DEBUG=True
ALLOWED_HOSTS="localhost,127.0.0.1"


DATABASE_URL="postgres://username:password@localhost:5432/dbName"

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Redis 
REDIS_URL=redis://localhost:6379

#email for sending mails when register and reset password
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # original
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'email address'
EMAIL_HOST_PASSWORD = 'address password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### **8️)Start the Development Server**
```bash
python manage.py runserver
```
- The server will be available at: **`http://127.0.0.1:8000/`**
- Admin Panel: **`http://127.0.0.1:8000/admin/`**

---

##  **API Documentation (Swagger)**
The backend includes **automatically generated API documentation** using **Swagger UI**.

### **How to Access the API Docs**
After starting the server, visit:
- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Redoc UI**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

**To generate API documentation manually**, run:
```bash
python manage.py spectacular --color --file schema.yml
```

---

##  **Chat System (WebSockets)**
The **chats** app allows real-time messaging using **Django Channels** and **Redis**.

### **How it Works**
1. **Users join a study group** → `/api/groups/{id}/join/`
2. **They receive a WebSocket URL** → `/api/groups/{id}/chat_link/`
3. **Connect to WebSocket**
```javascript
const socket = new WebSocket("wss://yourdomain.com/ws/group/{group_id}/?token=your_jwt_token");
```
4. **Send & receive messages in real-time!**

### **Redis WebSocket Setup**
- Install `channels_redis`:
```bash
pip install channels_redis
```
- Ensure `config/asgi.py` is configured correctly:
```python
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.chats.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(apps.chats.routing.websocket_urlpatterns),
})
```

---

## **Required migrations!!!**
To make and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **Authentication**
The project uses **JWT authentication** with `Simple JWT`.

### **Endpoints**
- **Obtain Token:** `POST /api/token/` -> just login
- **Refresh Token:** `POST /api/token/refresh/` -> automatically handles to refresh the token
- **User Registration:** `POST /api/register/`
- **Own Profile:** `GET /api/user/detail/{id}/`

To authenticate API requests, include the token:
```http
Authorization: *Bearer* YOUR_ACCESS_TOKEN
```

