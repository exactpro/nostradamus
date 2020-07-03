FROM rasa/rasa:1.10.3-full

WORKDIR /app

COPY ./actions/requirements.txt ./

USER root

RUN pip install -r requirements.txt

COPY ./actions /app/actions
COPY ./chatbot-entrypoint.sh /app/

USER 1001

ENTRYPOINT ["bash", "chatbot-entrypoint.sh"]
