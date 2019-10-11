# Define the python environement
FROM python:3.7.3-stretch


# Create a folder at the root of the container et make it the working directory
RUN mkdir /company-search-engine-backeng
WORKDIR /company-search-engine-backeng


# Copy the requirement txt in the working directory and install all the dependencies
# We make this first to throw error there if there is an error while installing dependencies
COPY requirements.txt /company-search-engine-backeng/
RUN pip install -r requirements.txt


# copy all the files in the repos
COPY . /company-search-engine-backeng/

# Specify the port
EXPOSE $PORT

# Launch the application
CMD python app.py
