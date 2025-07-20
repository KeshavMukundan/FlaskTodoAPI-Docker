# 1. Use a base image (official Python)
FROM python:3.10

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy all project files into the container
COPY . .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose Flask port
EXPOSE 3700

# 6. Command to run app
CMD ["sh", "-c", "sleep 15 && python todoAPI.py"]