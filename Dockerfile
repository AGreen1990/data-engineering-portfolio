#1. Lightweight version of python
FROM python:3.11-slim

#2 Create folder inside container to fold app
WORKDIR /app

#3 Copy ONLY requirements fole first
COPY requirements.txt .

#4 Install python libraries into container
RUN pip install --no-cache-dir -r requirements.txt

#5 Copy the rest of app files (main.py, templates, static)
COPY . .

#6 Expose the port so outside world can see the website
EXPOSE 8000

#7 exact terminal commands to turn on server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
