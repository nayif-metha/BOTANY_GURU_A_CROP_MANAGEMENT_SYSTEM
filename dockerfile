# Use the official Miniconda3 image as the base image
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Install Mamba
RUN conda install -n base -c conda-forge mamba

# Copy the requirements file into the container
COPY requirements.txt .

# Create a conda environment and install the required packages using Mamba
RUN mamba create -n myenv python=3.6 && \
    mamba install -n myenv --file requirements.txt --quiet && \
    conda clean -afy

# Activate the conda environment
RUN echo "source activate myenv" > ~/.bashrc
ENV PATH /opt/conda/envs/myenv/bin:$PATH

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["bash", "-c", "source activate myenv && python manage.py runserver 0.0.0.0:8000"]RUN conda install -n myenv --file requirements.txt --quiet
