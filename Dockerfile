# Use the official Python image as the base image
#FROM conda/miniconda3
#FROM --platform=linux/amd64 continuumio/anaconda3
FROM continuumio/anaconda3

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc g++ libgmp-dev libmpfr-dev libmpc-dev

ENV HNSWLIB_NO_NATIVE=1

# Copy the conda environment specification file (environment.yml) to the container
COPY environment.yml .
COPY requirements.txt .

# Create a Conda environment and activate it
RUN conda env create --verbose -f environment.yml
#RUN conda install pytorch::pytorch -c pytorch 
#RUN pip install -r requirements.txt
RUN echo "source activate dmiaqa" > ~/.bashrc
ENV PATH /opt/conda/envs/dmiaqa/bin:$PATH
RUN /bin/bash -c "source ~/.bashrc"

# Install additional requirements using pip
#COPY requirements.txt .
RUN /bin/bash -c "source activate dmiaqa && pip install -r requirements.txt"

# Copy the Flask server code to the container
COPY . .

# Set the Flask app environment variable
ENV FLASK_APP=app.py

# Expose the port on which the Flask server will run (replace 5000 with the appropriate port number)
EXPOSE 5000

# Start the Flask server
CMD ["python", "app.py"]

# Start the Flask server using Waitress
#CMD ["waitress-serve", "--call", "app:create_app"]
