# WhatsEase - WhatsApp-like Chat Application with AI Bot

A real-time chat application inspired by WhatsApp, featuring user-to-user messaging and an AI chatbot integration.  
Backend is built with **FastAPI** and MongoDB, and the frontend is built with **React** (no UI frameworks).

---

## 📂 Project Structure
```
WhatsEase/
├── backend/      # FastAPI backend code
├── frontend/     # React frontend code
└── README.md
```

---

## 🚀 Backend Setup
1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate       # Mac/Linux
   venv\Scripts\activate          # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**  
   Create a `.env` file in `backend/`:
   ```
   MONGO_URI=mongodb://localhost:27017/whatsease
   JWT_SECRET=your-secret-key
   ```

5. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   - Backend API Docs: http://localhost:8000/docs

---

## 💻 Frontend Setup
1. **Navigate to frontend**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   - Frontend runs at http://localhost:3000

---

## 🔌 Connecting Frontend & Backend
- The backend URL should be set in the frontend API/WebSocket config file (e.g., `src/websocket.js` or API service file).
- Example:
  ```javascript
  const BACKEND_URL = "http://localhost:8000";
  ```

---

## ✨ Features
- User authentication (JWT)
- Real-time messaging with WebSockets
- AI bot integration
- Chat search/filter
- Activity logging
- Responsive and accessible UI

---

## 🛠 Requirements
- Python 3.9+
- Node.js 16+
- MongoDB (local or cloud)

---

## 🏃‍♂️ Running the Full App
1. Start **backend** (port 8000)
2. Start **frontend** (port 3000)
3. Access the UI in your browser: http://localhost:3000

---

## 📜 License
This project is for demonstration purposes as part of a development task.
