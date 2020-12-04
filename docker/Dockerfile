FROM nginx:1.9.4 as web_server
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d /etc/nginx/conf.d

FROM python:3.7.9 as py_deps
WORKDIR /root
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --user --no-cache-dir --default-timeout=100 -r requirements.txt
RUN rm requirements.txt

FROM python:3.7.9 as app_server
COPY --from=py_deps /root/.local /root/.local
WORKDIR /root/.local/lib/ndlm_leak_monitoring_app
COPY ./src .
ENV PATH=/root/.local/bin:$PATH
ENV APP_PROJECT=ndlm_leak_monitoring_app
EXPOSE 8000
CMD python -m app_server