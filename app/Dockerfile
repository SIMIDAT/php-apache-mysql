FROM python:2.7.15
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD python DescargaACCUWEATHER.py & python DescargaTIEMPO.py & python DescargaOPENWEATHERMAP.py & python DescargaAEMET.py

