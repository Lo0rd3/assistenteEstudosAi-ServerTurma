FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask-socketio eventlet pexpect
RUN apt-get update && apt-get install -y cron


COPY . .


RUN echo '#!/bin/bash\n' \
'chmod -R a+w /users_homes || true\n' \
'for folder in cheatsheets flashcards resumos quizzes; do\n' \
'  find /users_homes/*/${folder} -type f -mtime +2 -delete 2>/dev/null || true\n' \
'done' > /usr/local/bin/clean_old_files.sh && \
chmod +x /usr/local/bin/clean_old_files.sh


RUN echo '0 0 * * * root /usr/local/bin/clean_old_files.sh' > /etc/cron.d/clean_old_files && \
chmod 0644 /etc/cron.d/clean_old_files && \
crontab /etc/cron.d/clean_old_files




RUN mkdir -p /users_homes /app/templates


COPY users.txt /users.txt

RUN apt-get update && apt-get install -y sudo


COPY users.txt /users.txt
RUN set -eux; \
    while IFS=: read -r user pass; do \
        useradd -m -d /users_homes/$user $user; \
        echo "$user:$pass" | chpasswd; \
    done < /users.txt

RUN set -eux; \
    while IFS=: read -r user pass; do \
        mkdir -p /users_homes/$user/cheatsheets /users_homes/$user/flashcards /users_homes/$user/resumos /users_homes/$user/quizzes; \
        chown -R $user:$user /users_homes/$user; \
    done < /users.txt


RUN echo "ALL ALL=(ALL) NOPASSWD: /usr/bin/python3 /app/main.py" >> /etc/sudoers



RUN set -eux; \
    while IFS=: read -r user pass; do \
        mkdir -p /users_homes/$user/cheatsheets /users_homes/$user/flashcards /users_homes/$user/resumos /users_homes/$user/quizzes; \
    done < /users.txt


EXPOSE 8080 8081



CMD ["sh", "-c", "service cron start && python3 webterminal.py"]


