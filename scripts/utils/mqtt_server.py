import json
import random
import time

from paho.mqtt import client as mqtt_client
src = "D:/mxz/mxz_back"
broker = 'p767a1ef.ala.cn-hangzhou.emqxsl.cn'
port = 8883
topic = 't/a'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# 如果 broker 需要鉴权，设置用户名密码
username = 'emqx'
password = 'emqx'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            subscribe(client)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # Set CA certificate
    client.tls_set(ca_certs=src + r'\scripts\writenote/emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def run_cmd( cmd_str='', echo_print=1):
    """
    执行cmd命令，不显示执行过程中弹出的黑框
    备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
    :param cmd_str: 执行的cmd命令
    :return:
    """
    from subprocess import run
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    d = run(cmd_str, shell=True, capture_output = True)
    print(d)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        run_cmd(data["cmd"])
    client.subscribe(topic)
    client.on_message = on_message


def run():
    i = 1
    while(True):
        if (i > 600):
            i = 600
        time.sleep(i*5)
        try:
            client = connect_mqtt()
            i = 1
            break
        except Exception as e:
            i = i + 1
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()