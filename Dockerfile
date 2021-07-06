FROM python:3-slim

WORKDIR /app

COPY requirements.txt ./
COPY MyFirstWebpage.py ./
COPY save_book_list.p ./
COPY save_book_names.p ./
COPY save_corr_mat.p ./

ADD ./templates/GetBookName.html templates/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python","MyFirstWebpage.py"]