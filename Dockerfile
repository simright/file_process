# FROM python2.7
FROM daocloud.io/shuqiao/simrightcom_python27:20180319

MAINTAINER sunjingchao <sunjingchao@simright.com>

COPY .  /app/fem_utils
ENV PYTHONPATH="/app/fem_utils:${PYTHONPATH}"
WORKDIR /app/fem_utils

RUN pip install -r /app/fem_utils/srv/requirements.txt
