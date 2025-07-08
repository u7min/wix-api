# Wix Blog Scraper & API Service 📝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📚 Overview

This project retrieves blog post lists using the **Wix API**, scrapes each post into **Markdown**, stores them in **MongoDB**, and serves them through a **FastAPI REST API**.

⚠️ Ensure compliance with Wix API Terms of Service. Excessive requests may lead to suspension or legal issues. This project is not affiliated with or endorsed by Wix.com.

---

## 🚀 Features

* Fetch blog posts via **Wix API**
* Scrape full blog post content with **BeautifulSoup**
* Convert posts to **Markdown**
* Store converted posts in **MongoDB**
* Serve posts through **FastAPI** endpoints
* Interactive API docs with **Swagger** and **Redoc**

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/u7min/wix-api
   cd wix-api
   ```

2. **Create virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set environment variables**

   Create a `.env` file in the project root with the following keys:

   ```env
   MONGO_URI=your_mongodb_connection_string
   WIX_API_URL=your_wix_api_url
   WIX_API_TOKEN=your_wix_api_token
   WIX_API_SITE_ID=your_wix_site_id
   X_API_USER=your_x_api_user
   X_API_ADMN=your_x_api_admin
   BOODING_BASE_URL=your_blog_url
   ```

---

## ▶️ Usage

Start the development server:

```bash
uvicorn app.api.main:app --reload
```

---

## 📝 API Documentation

* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Contributing

Pull requests, issues, and feature suggestions are welcome.
Feel free to fork and improve this project.

---

## 📫 Contact

For any questions or inquiries, please email me at [bigclouds@gmail.com](mailto:bigclouds(at)gmail.com).

