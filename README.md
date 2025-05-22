### Microserviço de gerenciamento de clientes - Tech Challenge Fase 4

# Serviço para cuidar dos clientes cadastrados

This project is a backend application designed to manage orders and facilitate efficient customer service as the business expands. Using **FastAPI** with a **hexagonal architecture**, the application allows customers to place and track orders and allows administrators to manage products, customers, and orders. It’s built as a monolithic application with a **PostgreSQL** database, containerized for easy deployment using **Docker** and **Docker Compose**.

## Overview

This service streamlines the customer management by:

- Allowing customers to sign up.
- Enabling admins to manage customers.

## Features

- **Customer Functionality**:
  - Place orders for a main item, side, drink, and dessert.
- **Admin Functionality**:
  - Manage customers.
  - Add, edit, and remove products.
  - Monitor all ongoing orders.

## Architecture

This project follows a **hexagonal architecture** (also known as ports and adapters), with a clear separation of concerns:

- **Core**: Contains domain models and interfaces.
- **Application**: Contains use cases for business logic.
- **Adapters**: Handles API and database interaction.

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/gabrielmatosms/tc-customers-service.git
   cd tc-customers-service
   ```

2. **Install Docker and Docker Compose** if you haven’t already:

   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)

3. **Build and run the application** using Docker Compose:

   ```bash
   docker-compose up --build -d
   ```

## API Endpoints

(Local) The FastAPI Swagger UI is available at: [http://localhost:8009/docs](http://localhost:8009/docs)


## Videos Explanations Links

Part 1 - [https://www.youtube.com/watch?v=B26AEoMjJgU](https://www.youtube.com/watch?v=B26AEoMjJgU) (Architecture representation) - Fase 1

Part 2 - [https://www.youtube.com/watch?v=ZrnqsGbtpDw](https://www.youtube.com/watch?v=B26AEoMjJgU) (API use) - Fase 2

Part 3 - [https://youtu.be/DgDAjOqwkTc](https://youtu.be/DgDAjOqwkTc) (API use) - Fase 3

## Workflow Representations

Video explicando a arquitetura dos microserviços - [https://www.youtube.com/watch?v=lWntA32xC7I](https://www.youtube.com/watch?v=lWntA32xC7I) - Fase 4

** Acesse o [miro](https://miro.com/app/board/uXjVIy2LsaY=/)
![Diagram de Micro-Servicos](https://github.com/user-attachments/assets/0ea2dc40-3047-4001-88b7-61858c7c9bc9)

