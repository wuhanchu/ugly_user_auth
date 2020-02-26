FROM frolvlad/alpine-python3


ENV API_SERVER_HOME=/opt/www

WORKDIR "$API_SERVER_HOME"

COPY "./requirements.txt" "./"

EXPOSE 5000



ARG INCLUDE_POSTGRESQL=false
ARG INCLUDE_UWSGI=false
RUN echo 'https://mirrors.aliyun.com/alpine/v3.9/main/' >/etc/apk/repositories && echo 'https://mirrors.aliyun.com/alpine/v3.9/community/' >>/etc/apk/repositories &&  \
    apk add --no-cache --virtual=.build_dependencies musl-dev  gcc python3-dev  py3-cffi libevent-dev linux-headers  openssl-dev libxslt libxslt-dev && \
    apk --no-cache add tzdata   libffi-dev yasm ffmpeg && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&  \
    echo "Asia/Shanghai" >/etc/timezone  &&  \
    cd /opt/www && \
    pip3 install  -i https://pypi.tuna.tsinghua.edu.cn/simple  -r ./requirements.txt   &&   \
    apk del .build_dependencies


COPY "./" "./"

CMD [ "python3", "./z_markgo.pyc"]