import datetime

def log(msg: str) -> None:
    today = datetime.datetime.today()
    date = today.strftime('%Y-%m-%d')
    time = today.strftime('%X')
    with open(f'./log/{date}', 'a') as log_file:
        log_file.write(f'[{time}] {msg}')