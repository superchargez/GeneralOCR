# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Install Tesseract OCR
# RUN apt-get update && apt-get install -y tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr && pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8855

# Run main.py when the container launches
CMD streamlit run main.py --server.port 8855

# docker run --name sprout_ocr -p 8501:8855 -v C:\Users\jawad\Downloads\projects\ocr\codefiles\images:/app/images ptcl_sprout_ocr