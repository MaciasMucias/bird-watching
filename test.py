import cv2

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'FMP4')

video_out_conf = (fourcc, fps, size)
out = cv2.VideoWriter('better_test.mp4', fourcc, fps, size)


frame_count = 0
while True:
    _, frame = cap.read()
    out.write(frame)
    frame_count += 1
    cv2.waitKey(1)
    if frame_count > 30:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

