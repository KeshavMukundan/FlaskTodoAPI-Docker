# FlaskTodoAPI-Docker

A simple RESTful To-Do List API built with Flask, Flask-SQLAlchemy, and MySQL, designed to run efficiently using Docker and Docker Compose. This project provides user authentication and CRUD (Create, Read, Update, Delete) operations for managing personal tasks.

## Table of Contents

-   [Features](#features)
-   [Technologies Used](#technologies-used)
-   [Prerequisites](#prerequisites)
-   [Getting Started](#getting-started)



## Features

* **User Authentication:** Register and log in users.
* **JWT (JSON Web Token) based Authentication:** Secure access to protected routes.
* **To-Do Management:** Create, retrieve, update, and delete personal to-do items.
* **Pagination:** Retrieve to-do items with pagination support.
* **Containerized Environment:** Easy setup and deployment using Docker and Docker Compose.
* **MySQL Database:** Persistent data storage.

## Technologies Used

* **Backend:** Python 3.10, Flask
* **Database ORM:** Flask-SQLAlchemy
* **MySQL Connector:** PyMySQL
* **Authentication:** PyJWT, Werkzeug (for password hashing)
* **Database:** MySQL 8.0
* **Containerization:** Docker, Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

* **Docker Desktop** (includes Docker Engine and Docker Compose) or **Docker Engine** and **Docker Compose** installed separately.
    * [Install Docker](https://docs.docker.com/get-docker/)
* **Postman** or `curl` for testing the API endpoints.
    * [Download Postman](https://www.postman.com/downloads/)

## Getting Started

Follow these steps to get your FlaskTodoAPI-Docker project up and running.

### 1. Clone the Repository

```bash
git clone [https://github.com/KeshavMukundan/FlaskTodoAPI-Docker.git](https://github.com/KeshavMukundan/FlaskTodoAPI-Docker.git)
cd FlaskTodoAPI-Docker
