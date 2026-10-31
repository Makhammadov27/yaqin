import asyncio
from pathlib import Path
out=Path(__file__).resolve().parent.parent / 'storage' / 'mailbox';out.mkdir(parents=True,exist_ok=True)
async def client(r,w):
    w.write(b'220 localhost test SMTP\r\n');await w.drain();data=False;lines=[]
    while line:=await r.readline():
        if data:
            if line==b'.\r\n':
                import time
                (out/f'{time.time_ns()}.eml').write_bytes(b''.join(lines));data=False;w.write(b'250 stored\r\n')
            else:lines.append(line)
        elif line.upper().startswith(b'EHLO'):w.write(b'250-localhost\r\n250 SIZE 1000000\r\n')
        elif line.upper().startswith(b'DATA'):data=True;lines=[];w.write(b'354 End with dot\r\n')
        elif line.upper().startswith(b'QUIT'):w.write(b'221 Bye\r\n');await w.drain();break
        else:w.write(b'250 OK\r\n')
        await w.drain()
    w.close()
async def main():
    srv=await asyncio.start_server(client,'127.0.0.1',1025)
    print('Test SMTP on 127.0.0.1:1025',flush=True)
    async with srv:await srv.serve_forever()
asyncio.run(main())

