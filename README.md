# 🛰️ SQUAD-COMMS | Emergency SMS Dispatcher

A high-fidelity, full-stack communication dashboard built for rapid alert broadcasting. This project demonstrates a production-ready workflow for API integration, secure authentication, and local data persistence.

![Dashboard Preview](https://via.placeholder.com/800x450.png?text=Squad-Comms+Interface+Preview) 
*(Tip: Replace this link with a real screenshot of your new UI!)*

## 🚀 Strategic Features
* **Dual-Mode Engine**: Features a "Demo Mode" that simulates API handshakes and database logging when Twilio credentials are not provided—ensuring 100% uptime for portfolio reviewers.
* **Secure Dispatch**: Implementation of PIN-based authorization to prevent unauthorized broadcast triggers.
* **Live Persistence**: Integrated SQLite backend to maintain a verifiable audit trail of all outgoing transmissions.
* **Cyberpunk UI**: A high-performance interface built with Tailwind CSS, featuring glassmorphism and real-time system status indicators.

## 🛠️ Tech Stack
* **Backend**: Python, FastAPI
* **Database**: SQLite3
* **API**: Twilio SMS (REST API)
* **Frontend**: Tailwind CSS, JavaScript (Async/Fetch)
* **Deployment**: Hugging Face Spaces / Docker

## 📖 How It Works
1. **Authentication**: The system requires a 4-digit PIN (`1234` by default) to unlock the dispatch command.
2. **Database Logging**: Every message is immediately timestamped and committed to `crew.db`.
3. **API Logic**: 
   - If `TWILIO_ACCOUNT_SID` is detected in environment variables, the system executes a real SMS broadcast.
   - If variables are missing, the system enters **Demo Mode**, simulating network latency and providing a successful UI response for testing purposes.

## 🛠️ Installation & Setup
To run this locally or on your own server:
1. Clone the repo.
2. Set your environment variables: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_NUMBER`, `ADMIN_PIN`.
3. Run `uvicorn main:app --reload`.
