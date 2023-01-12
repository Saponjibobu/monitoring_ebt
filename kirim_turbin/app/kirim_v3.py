import minimalmodbus
import json
import requests
import time
import csv
import datetime

url = "http://10.46.10.128:5000/dummy_komunikasi_data_v2"
headers = {
'Content-Type': 'application/json'
}

try:
    """PZEM 017 TURBIN ANGIN"""
    mb_address = 1 # Modbus address of sensor
    mb = minimalmodbus.Instrument('/dev/ttyUSB0',mb_address)	# Make an "instrument" object called mb (port name, slave address (in decimal))

    mb.serial.baudrate = 9600				# BaudRate
    mb.serial.bytesize = 8					# Number of data bits to be requested
    mb.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
    mb.serial.stopbits = 2					# Number of stop bits
    mb.serial.timeout  = 3					# Timeout time in seconds
    mb.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

    # Good practice to clean up before and after each execution
    mb.clear_buffers_before_each_transaction = True
    mb.close_port_after_each_call = True

except:
    """PZEM 017 TURBIN ANGIN"""
    mb_address = 1 # Modbus address of sensor
    mb = minimalmodbus.Instrument('/dev/ttyUSB1',mb_address)	# Make an "instrument" object called mb (port name, slave address (in decimal))

    mb.serial.baudrate = 9600				# BaudRate
    mb.serial.bytesize = 8					# Number of data bits to be requested
    mb.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
    mb.serial.stopbits = 2					# Number of stop bits
    mb.serial.timeout  = 3					# Timeout time in seconds
    mb.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

    # Good practice to clean up before and after each execution
    mb.clear_buffers_before_each_transaction = True
    mb.close_port_after_each_call = True

finally:
    header_added = False
    table_header = ['client_id', 'send_to_db_at', 'processing_time', 'voltage (V)', 'current (A)', 'power (W)', 'energy (Wh)']
    with open('logger_turbin_v3_new.csv','a', newline='') as f:
        writer = csv.writer(f)
        if not header_added:
            writer.writerow(i for i in table_header)
            header_added = True

    while True:
        try:
            """PZEM 017"""
            time_awal = time.time()
            client_id = 8

            data = mb.read_registers(0, 8, 4) 
            voltage = data[0]/100
            current = data[1]/100
            power = round(voltage*current,5)
            energy = round(power*5/60,5)

            time_akhir = time.time()
            processing_time = time_akhir-time_awal

            """DATA CREATED AT"""
            data_created_at = datetime.datetime.now()+datetime.timedelta(hours=7)

            """CSV"""
            data = [client_id, data_created_at, processing_time, voltage, current, power, energy]
            with open('logger_turbin_v3_new.csv','a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)

            """DATABASE"""
            send_to_db_at = datetime.datetime.now()+datetime.timedelta(hours=7)
            payload = json.dumps(
                {'client_id':client_id,
                'data':
                {
                'send_to_db_at': str(send_to_db_at),
                'processing_time': str(processing_time),
                'voltage': voltage,
                'current': current,
                'power': power,
                'energy': energy,
                'power_factor': 0,
                }   
                }
            )

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            print(payload)
            time.sleep(300)

        except:
            print('pass = data error\n')
            """PZEM 017"""
            time_awal = time.time()
            client_id = 8
 
            voltage = 999999
            current = 999999
            power = 999999
            energy = 999999

            time_akhir = time.time()
            processing_time = time_akhir-time_awal

            """DATA CREATED AT"""
            data_created_at = datetime.datetime.now()+datetime.timedelta(hours=7)

            """CSV"""
            data = [client_id, data_created_at, processing_time, voltage, current, power, energy]
            with open('logger_turbin_v3_new.csv','a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)

            """DATABASE"""
            send_to_db_at = datetime.datetime.now()+datetime.timedelta(hours=7)
            payload = json.dumps(
                {'client_id':client_id,
                'data':
                {
                'send_to_db_at': str(send_to_db_at),
                'processing_time': str(processing_time),
                'voltage': voltage,
                'current': current,
                'power': power,
                'energy': energy,
                'power_factor': 999999,
                }   
                }
            )

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            print(payload)
            time.sleep(300)

            
           
