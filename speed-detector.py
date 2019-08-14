#!/usr/bin/python3

import paho.mqtt.client as paho
import time

broker="broker.hivemq.com"
broker="iot.eclipse.org"

def get_bytes(t, iface='wlp5s0'):
    with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
        data = f.read();
    return int(data)

if __name__ == '__main__':
    (tx_prev, rx_prev) = (0, 0)

    client=paho.Client("ark-speed-detector")
    print("connecting to broker ",broker)
    client.connect(broker)#connect

    while(True):
        tx = get_bytes('tx')
        rx = get_bytes('rx')

        if tx_prev > 0:
            tx_speed = tx - tx_prev
            client.publish("ark/speed/tx",tx_speed)
            print('TX: ', tx_speed, 'bps')

        if rx_prev > 0:
            rx_speed = rx - rx_prev
            client.publish("ark/speed/rx",rx_speed)
            print('RX: ', rx_speed, 'bps')

        time.sleep(1)

        tx_prev = tx
        rx_prev = rx