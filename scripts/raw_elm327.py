import serial
import json

port = serial.serial_for_url('/dev/rfcomm0', parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=10)
port.baudrate = 38400
port.timeout = 1

def send_for_response(request):
    port.reset_input_buffer()
    port.write(request.encode() + b'\r')
    port.flush()
    response = port.read(len('NO DATA\r\r>'))
    if response != b'NO DATA\r\r>':
        response += port.read(256)
    return response

print(send_for_response("AT Z"))
print(send_for_response("ATI"))
print(send_for_response("AT D"))
print(send_for_response("AT E0"))
print(send_for_response("AT D1"))
print(send_for_response("AT SP5"))

print(send_for_response("00 00"))

for SID in range(256):
    responses = {}
    for PID in range(256):
        request = f"{SID:02X} {PID:02X}"
        response = send_for_response(request)
        print (f"{request} => {response}")
        responses[request] = response.decode()
    fpath = f'SID_{SID:02X}.json'
    with open(fpath, 'w') as f:
        json.dump(responses, f)
        print(f'Wrote {fpath}')
print(f'Done.')
