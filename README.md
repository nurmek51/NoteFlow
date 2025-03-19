Вот дополненный и доработанный `README.md` с учетом Swagger-документации и улучшенной структурой.  

---

## 📌 **NoteFlow — Server-side Documentation**

### 📖 **Project Description**
**NoteFlow** is a platform for sharing educational materials at SDU University. It allows users to upload, search, filter, rate, and discuss study materials across various subjects. The platform also features **a chat system** for communication between users.

This documentation covers **backend setup, API documentation, database management, and WebSocket chat configuration**.

---

## 🚀 **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/nurmek51/NoteFlow.git
cd NoteFlow
```

### **2️⃣ Create and Activate a Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Database**
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

### **5️⃣ Configure Redis (for WebSockets & Caching)**
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

### **6️⃣ Apply Migrations**
```bash
python manage.py migrate
```

### **7️⃣ Create a Superuser**
```bash
python manage.py createsuperuser
```

### **8️⃣ Start the Development Server**
```bash
python manage.py runserver
```
- The server will be available at: **`http://127.0.0.1:8000/`**
- Admin Panel: **`http://127.0.0.1:8000/admin/`**

---

## 📡 **API Documentation (Swagger)**
The backend includes **automatically generated API documentation** using **Swagger UI**.

### **📌 How to Access the API Docs**
After starting the server, visit:
- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Redoc UI**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

**To generate API documentation manually**, run:
```bash
python manage.py spectacular --color --file schema.yml
```

---

## 💬 **Chat System (WebSockets)**
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

## 📚 **Database Management**
To make and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔑 **Authentication**
The project uses **JWT authentication** with `Simple JWT`.

### **Endpoints**
- **Obtain Token:** `POST /api/token/`
- **Refresh Token:** `POST /api/token/refresh/`
- **User Registration:** `POST /api/register/`
- **User Profile:** `GET /api/user/detail/{id}/`

To authenticate API requests, include the token:
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## 📌 **Project API Overview**
### **🔹 Study Groups**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/groups/` | List all study groups |
| `POST` | `/api/groups/` | Create a new study group |
| `GET`  | `/api/groups/{id}/` | Retrieve study group details |
| `PUT`  | `/api/groups/{id}/` | Update a study group |
| `PATCH` | `/api/groups/{id}/` | Partially update a study group |
| `DELETE` | `/api/groups/{id}/` | Delete a study group |
| `GET`  | `/api/groups/{id}/chat_link/` | Get WebSocket Chat Link |
| `POST` | `/api/groups/{id}/join/` | Join a Study Group |
| `POST` | `/api/groups/{id}/leave/` | Leave a Study Group |
| `GET`  | `/api/groups/my_groups/` | List groups user is part of |

### **🔹 Educational Materials**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/api/material/` | List all materials |
| `POST` | `/api/material/` | Upload new material |
| `GET`  | `/api/material/{id}/` | Get material details |
| `PUT`  | `/api/material/{id}/` | Update material |
| `DELETE` | `/api/material/{id}/` | Delete material |
| `POST` | `/api/material/upload/` | Upload a file |

### **🔹 Users & Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/register/` | Register a new user |
| `POST` | `/api/token/` | Obtain JWT token |
| `POST` | `/api/token/refresh/` | Refresh JWT token |
| `GET`  | `/api/user/detail/{id}/` | Get user details |
| `PUT`  | `/api/user/detail/{id}/` | Update user profile |
| `DELETE` | `/api/user/detail/{id}/` | Delete user profile |

---

## 📜 **Conclusion**
**NoteFlow** is a powerful and flexible platform for managing educational materials and facilitating communication among SDU University students. By following this guide, you can successfully deploy, configure, and extend the backend to suit your needs.

🔥 Happy coding! 🚀
