from django.shortcuts import render
from django.conf import settings
from .models import UserRegistrationModel
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegister.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(
                loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})

def UserHome(request):
    return render(request, 'Users/UserHome.html', {})




import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ultralytics import YOLO
import cv2
import numpy as np

# Path to the YOLO model
MODEL_PATH = 'media/yolov8n.pt'  # Update this with the correct model path

def get_color_for_speed(speed):
    if speed >= 100:
        return (0, 0, 255)    # Red (BGR)
    elif speed >= 80:
        return (0, 255, 0)    # Green
    elif speed >= 40:
        return (0, 255, 255)  # Yellow
    else:
        return (255, 255, 255) # White

def upload_video(request):
    # Check if the method is POST and if a video file is uploaded
    if request.method == "POST" and request.FILES.get('video'):
        # Save the uploaded video
        uploaded_file = request.FILES['video']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploaded_videos'))
        file_path = fs.save(uploaded_file.name, uploaded_file)
        uploaded_video_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_videos', file_path)

        # Process the video
        output_video_path, car_data = process_video(uploaded_video_path)

        # Generate URL for the processed video (ensure it's relative to the MEDIA_URL)
        video_url = os.path.join(settings.MEDIA_URL, 'output_videos', os.path.basename(output_video_path))
        return render(request, 'Users/result.html', {'video_url': video_url, 'car_data': car_data})

    return render(request, 'Users/upload.html')


def process_video(video_path):
    """
    Processes the uploaded video and saves the processed output video.
    """
    # Define the output directory for processed videos
    output_dir = os.path.join(settings.MEDIA_ROOT, 'output_videos')
    os.makedirs(output_dir, exist_ok=True)
    
    # Set the output video path
    output_video_path = os.path.join(output_dir, 'output_video.mp4')

    # Load YOLO model
    model = YOLO(MODEL_PATH)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file.")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' or 'XVID'
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    scale_factor = 0.05
    prev_positions = {}
    car_speeds = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO inference
        results = model(frame)

        for result in results[0].boxes:
            x1, y1, x2, y2 = result.xyxy[0].cpu().numpy()
            class_id = int(result.cls.cpu().item())

            if class_id == 2:  # Class ID for cars in COCO dataset
                car_id = str(int(x1))  # Unique ID based on bounding box x1
                curr_bbox = (x1, y1, x2, y2)

                if car_id in prev_positions:
                    # Estimate speed
                    speed = estimate_speed(prev_positions[car_id], curr_bbox, fps, scale_factor)
                    
                    if car_id not in car_speeds:
                        car_speeds[car_id] = []
                    car_speeds[car_id].append(speed)

                    color = get_color_for_speed(speed)
                    cv2.putText(frame, f"Speed: {speed:.2f} km/h", (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                prev_positions[car_id] = curr_bbox

        # Write the processed frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    
    # Calculate average speed per car
    car_data = []
    for cid, speeds in car_speeds.items():
        if speeds:
            avg_speed = sum(speeds) / len(speeds)
            if avg_speed >= 100: status = 'Red (High Speed)'
            elif avg_speed >= 80: status = 'Green (Normal)'
            elif avg_speed >= 40: status = 'Yellow (Slow)'
            else: status = 'White (Very Slow)'
            
            car_data.append({
                'car_id': cid,
                'avg_speed': round(avg_speed, 2),
                'status': status
            })

    return output_video_path, car_data


def estimate_speed(prev_bbox, curr_bbox, fps, scale_factor):
    """
    Estimate the speed of the car based on the bounding box positions.
    """
    prev_center = ((prev_bbox[0] + prev_bbox[2]) / 2, (prev_bbox[1] + prev_bbox[3]) / 2)
    curr_center = ((curr_bbox[0] + curr_bbox[2]) / 2, (curr_bbox[1] + curr_bbox[3]) / 2)
    distance = np.sqrt((curr_center[0] - prev_center[0]) ** 2 +
                       (curr_center[1] - prev_center[1]) ** 2)
    return (distance * scale_factor) * fps * 3.6  # Convert m/s to km/h

def live_camera(request):
    """
    Opens the live camera, processes frames for car speed detection,
    and displays the result in an OpenCV window.
    """
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return render(request, 'Users/upload.html', {'message': 'Error: Could not open camera.'})

    scale_factor = 0.05
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 30
    prev_positions = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO inference
        results = model(frame)

        for result in results[0].boxes:
            x1, y1, x2, y2 = result.xyxy[0].cpu().numpy()
            class_id = int(result.cls.cpu().item())

            if class_id == 2:  # Class ID for cars in COCO dataset
                car_id = str(int(x1))  # Unique ID based on bounding box x1
                curr_bbox = (x1, y1, x2, y2)

                if car_id in prev_positions:
                    # Estimate speed
                    speed = estimate_speed(prev_positions[car_id], curr_bbox, fps, scale_factor)
                    color = get_color_for_speed(speed)
                    cv2.putText(frame, f"Speed: {speed:.2f} km/h", (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                prev_positions[car_id] = curr_bbox

        # Display the frame in an OpenCV window
        cv2.imshow('Live Camera - Press Q to Exit', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    return render(request, 'Users/upload.html', {'message': 'Live camera closed successfully.'})
