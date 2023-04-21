from sftp import Sftp

hostname = "192.168.0.227"
username = "karas"
password = "Skopioxv1"



remote_recordings_root = "/home/karas/Desktop/Sikorki/recordings"
local_recording_root = "D:/Informatyka/Sikorki/recordings"
local_log_path = "D:/Informatyka/Sikorki/Error.log"
while True:
    try:
        with Sftp(hostname=hostname, username=username, password=password) as server:
            for recording_name in server.listdir(remote_recordings_root):
                remote_path = remote_recordings_root + '/' + recording_name
                local_path = local_recording_root + '/' + recording_name
                server.download(remote_path, local_path)
                server.remove(remote_path)
    except Exception:
        with open(local_log_path, "a") as log:
            log.write(str(datetime.date.today()) + '\n')
            traceback.print_exc()
            traceback.print_exc(file=log)
            log.write("\n\n")
    finally:
        break
quit()