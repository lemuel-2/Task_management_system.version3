# Task Management System v3

A Python-based task management system with a web interface built with HTML and CSS.

## Project Overview

This is a task management application that allows users to create, track, and manage tasks efficiently. The project is built with:
- **Backend**: Python
- **Frontend**: HTML & CSS
- **Architecture**: Web-based application

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python** 3.7 or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- A web browser (for accessing the interface)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/lemuel-2/Task_management_system.version3.git
cd Task_management_system.version3
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv .venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install common dependencies:

```bash
pip install flask  # or Django, FastAPI depending on your setup
```

## Running the Application

### Start the Server

```bash
# If using Django
python manage.py runserver

The application will typically be available at: **http://localhost:5000** or **http://127.0.0.1:5000**

### Access the Web Interface

1. Open your web browser
2. Navigate to `http://localhost:5000` (or the URL shown in your terminal)
3. You should see the task management interface

## Features

- ✅ Create new tasks
- ✅ View all tasks
- ✅ Update task status
- ✅ Delete tasks
- ✅ Responsive web interface

## Project Structure

```
Task_management_system.version3/
├── README.md
├── app.py (or main application file)
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
├── templates/
│   └── index.html
│   └── tasks.html
└── (other application files)
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change the port
python app.py --port 8000
```

**Module Not Found Error**
```bash
# Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

**Permission Denied (macOS/Linux)**
```bash
chmod +x app.py
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue on the GitHub repository.

---

**Happy Task Managing! 🚀**
