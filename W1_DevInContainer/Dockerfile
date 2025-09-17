# Using slim python image
FROM python:3.9-slim

# Setting workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt  . 
RUN pip3 install -r requirements.txt

# Create Uploaded_Files directory
RUN mkdir Uploaded_Files

# Commented => Code will come from volume
# Copy project files
# COPY streamlit_routine_app.py .
# COPY create_table.py . 
# COPY common_modules/postgres_conn.py ./common_modules/postgres_conn.py


EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "streamlit_routine_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Run create_table.py first, then Streamlit
CMD ["sh", "-c", "python create_table.py && streamlit run streamlit_routine_app.py --server.port=8501 --server.address=0.0.0.0"]
