FROM python:3.11-slim

# Dependências base + SSH server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Diretório da app
WORKDIR /app

# Aumentar limites de sessões SSH
RUN echo '\
MaxSessions 20\n\
MaxStartups 20:30:100\
' >> /etc/ssh/sshd_config

# Copia código e requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia scripts todos
COPY . .

RUN mkdir -p /users_homes
COPY users.txt /users.txt
COPY login-mainpy.sh /usr/local/bin/login-mainpy.sh
RUN chmod +x /usr/local/bin/login-mainpy.sh
RUN set -eux; \
    while IFS=: read -r user pass; do \
        useradd -m -d /users_homes/$user $user; \
        echo "$user:$pass" | chpasswd; \
        usermod -s /usr/local/bin/login-mainpy.sh $user; \
    done < /users.txt

# Script de login personalizado
COPY login-mainpy.sh /usr/local/bin/login-mainpy.sh
RUN chmod +x /usr/local/bin/login-mainpy.sh

# Usa o script como shell para todos os users
RUN set -eux; \
    while IFS=: read -r user pass; do \
        usermod -s /usr/local/bin/login-mainpy.sh $user; \
    done < /users.txt
RUN set -eux; \
    while IFS=: read -r user pass; do \
        usermod -s /usr/local/bin/login-mainpy.sh $user; \
    done < /users.txt




# Config SSH
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's@/home@/users_homes@g' /etc/ssh/sshd_config

EXPOSE 22 8080

# Entrypoint script para levantar sshd + flask
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
