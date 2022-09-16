import cv2
import mediapipe as mp
import time
from socketIO_client import SocketIO

# IP Server (String number)
CONNECT_TO_SERVER = True # True / False
SERVER_IP = 'localhost' # localhost | i.p.ser.ver

MOTOR = 1
MIN_POS = 0
MAX_POS = 180
MASC = 0

# MOTOR = 2
# MIN_POS = 50
# MAX_POS = 180
# MASC = 1000

# MOTOR = 3
# MIN_POS = 0
# MAX_POS = 180
# MASC = 2000

# MOTOR = 4
# MIN_POS = 0
# MAX_POS = 180
# MASC = 3000

# MOTOR = 5
# MIN_POS = 80
# MAX_POS = 180
# MASC = 4000

INIT_POSITIONS = [90,90,50,120,100]

# Steps [Degrees]
STEP_MIN = 1 # For low velocity
STEP_MAX = 5   # For high velocity



mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
controlling = False
INFO_TEXT_X = 15
INFO_TEXT_Y = 35
both_hands = False
left_detected = False
right_detected = False
right_hand_landmarks = []
left_hand_landmarks = []
controlling_hand_message = ""
controlling_message = "Sin control"
controlling_message_color = (0,0,0)

LOW = False
HIGH = False

if CONNECT_TO_SERVER:
    # print("Conecando al servidor...")
    socketIO = SocketIO(SERVER_IP, 5001)
    # print("Conectado al servidor.")


# Camera index
cap = cv2.VideoCapture(0)
# with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

while True:
    ok, frame = cap.read()
    if not ok:
        continue
    height, width, channels = frame.shape
    #frame = cv2.flip(frame,1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_handedness is not None: # is not pointer to null
        for index, hand_handedness in enumerate(results.multi_handedness):
            left_right = hand_handedness.classification[0].index # 0: Left, 1:Right
            if(left_right == 1): # is the right hand?
                right_detected = True
                right_hand_landmarks = results.multi_hand_landmarks[index]
            elif(left_right == 0): # is the left hand?
                left_detected = True
                left_hand_landmarks = results.multi_hand_landmarks[index]

        if right_detected and not left_detected:
            controlling_hand_message = "DERECHA"
            # mp_drawing.draw_landmarks(frame, right_hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
        elif right_detected and left_detected:
            controlling_hand_message = "DERECHA + IZQUIERDA"
            # mp_drawing.draw_landmarks(frame, right_hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # mp_drawing.draw_landmarks(frame, left_hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # calibration
            if not controlling:
                cv2.circle(frame, (100, 200),10,(0,0,255),11)
                LEFT_INDEX_FINGER_TIP_X = round(left_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                LEFT_INDEX_FINGER_TIP_Y = round(left_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                cv2.circle(frame, (LEFT_INDEX_FINGER_TIP_X,LEFT_INDEX_FINGER_TIP_Y),5,(0,0,255),6)

                if LEFT_INDEX_FINGER_TIP_X>89 and LEFT_INDEX_FINGER_TIP_X<111 and LEFT_INDEX_FINGER_TIP_Y>190 and LEFT_INDEX_FINGER_TIP_Y<211:
                    controlling = True
                    controlling_message = "SI"
                    controlling_message_color = (0,255,0)
                    # Picture of Wrist incial values
                    START_X = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                    START_Y = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                    # RIGHT_WRIST_START_Z = right_hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z

                    # Initialize controls positions
                    
                    GAPX = 100
                    GAPY = 70
                    R_W = 30

                    # M1L_X1 = START_X - round(GAPX/2)
                    # M1L_Y1 = START_Y - round(GAPY/3)
                    M1L_X1 = round(width/2-50)
                    M1L_Y1 = round(height-50)
                    
                    M1L_X2 = M1L_X1 + R_W
                    M1L_Y2 = M1L_Y1 + R_W

                    M1R_X1 = M1L_X1 + GAPX
                    M1R_Y1 = M1L_Y1
                    M1R_X2 = M1R_X1 + R_W
                    M1R_Y2 = M1R_Y1 + R_W

                    M1_TEXT_X =  M1L_X2
                    M1_TEXT_Y =  M1L_Y2 - GAPY

                    M1L_SIM_TEXT_X =  M1L_X1 + round(R_W/5)
                    M1L_SIM_TEXT_Y =  M1L_Y1 - round(R_W/2)

                    M1R_SIM_TEXT_X =  M1R_X1 + round(R_W/5)
                    M1R_SIM_TEXT_Y =  M1R_Y1 - round(R_W/2)


        elif left_detected and not right_detected:
            controlling_hand_message = "IZQUIERDA"
            # mp_drawing.draw_landmarks(frame, left_hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if controlling and right_detected:

            # TIP
            RIGHT_INDEX_FINGER_TIP_X = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
            RIGHT_INDEX_FINGER_TIP_Y = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
            RIGHT_PINKY_FINGER_TIP_X = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width)
            RIGHT_PINKY_FINGER_TIP_Y = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)

            # PIP
            RIGHT_INDEX_FINGER_PIP_X = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * width)
            RIGHT_INDEX_FINGER_PIP_Y = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * height)
            RIGHT_PINKY_FINGER_PIP_X = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x * width)
            RIGHT_PINKY_FINGER_PIP_Y = round(right_hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * height)

            # # TIP
            # cv2.circle(frame, (RIGHT_INDEX_FINGER_TIP_X,RIGHT_INDEX_FINGER_TIP_Y),5,(0,255,0),6)
            # cv2.circle(frame, (RIGHT_PINKY_FINGER_TIP_X,RIGHT_PINKY_FINGER_TIP_Y),5,(0,255,0),6)

            # # PIP
            # cv2.circle(frame, (RIGHT_INDEX_FINGER_PIP_X,RIGHT_INDEX_FINGER_PIP_Y),5,(0,0,0),6)
            # cv2.circle(frame, (RIGHT_PINKY_FINGER_PIP_X,RIGHT_PINKY_FINGER_PIP_Y),5,(0,0,0),6)
            # # PIP line
            # cv2.line(frame, (RIGHT_INDEX_FINGER_PIP_X,RIGHT_INDEX_FINGER_PIP_Y), (RIGHT_PINKY_FINGER_PIP_X,RIGHT_PINKY_FINGER_PIP_Y), (0,0,0), 2)

            # Drawing indicators -> cv2.rectangle(image, start_point, end_point, color, thickness)
            cv2.putText(frame, "-", (M1L_SIM_TEXT_X,M1L_SIM_TEXT_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.putText(frame, "+", (M1R_SIM_TEXT_X,M1R_SIM_TEXT_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.rectangle(frame, ( M1L_X1 , M1L_Y1 ) , ( M1L_X2 , M1L_Y2 ),(0,0,255), -1) 
            cv2.rectangle(frame, ( M1R_X1 , M1R_Y1 ) , ( M1R_X2 , M1R_Y2 ),(0,0,255), -1)

            # Check if TIP is Over or Under the PIP line
            # (slower)
            if RIGHT_INDEX_FINGER_TIP_Y <= RIGHT_INDEX_FINGER_PIP_Y and RIGHT_INDEX_FINGER_PIP_Y > height/2:
                if INIT_POSITIONS[MOTOR-1] >= MIN_POS:
                    INIT_POSITIONS[MOTOR-1] = INIT_POSITIONS[MOTOR-1]-STEP_MIN
                cv2.rectangle(frame, ( M1L_X1 , M1L_Y1 ) , ( M1L_X2 , M1L_Y2 ),(0,255,0), -1)
            elif RIGHT_PINKY_FINGER_TIP_Y <= RIGHT_PINKY_FINGER_PIP_Y and RIGHT_PINKY_FINGER_PIP_Y > height/2:
                if INIT_POSITIONS[MOTOR-1] <= MAX_POS:
                    INIT_POSITIONS[MOTOR-1] = INIT_POSITIONS[MOTOR-1]+STEP_MIN
                cv2.rectangle(frame, ( M1R_X1 , M1R_Y1 ) , ( M1R_X2 , M1R_Y2 ),(0,255,0), -1)
            
            # (faster)
            if RIGHT_INDEX_FINGER_TIP_Y <= RIGHT_INDEX_FINGER_PIP_Y and RIGHT_INDEX_FINGER_PIP_Y <= height/2:
                if INIT_POSITIONS[MOTOR-1] >= MIN_POS:
                    INIT_POSITIONS[MOTOR-1] = INIT_POSITIONS[MOTOR-1]-STEP_MAX
                cv2.rectangle(frame, ( M1L_X1 , M1L_Y1 ) , ( M1L_X2 , M1L_Y2 ),(0,255,0), -1)
            elif RIGHT_PINKY_FINGER_TIP_Y <= RIGHT_PINKY_FINGER_PIP_Y and RIGHT_PINKY_FINGER_PIP_Y <= height/2:
                if INIT_POSITIONS[MOTOR-1]+STEP_MAX <= MAX_POS:
                    INIT_POSITIONS[MOTOR-1] = INIT_POSITIONS[MOTOR-1]+STEP_MAX
                cv2.rectangle(frame, ( M1R_X1 , M1R_Y1 ) , ( M1R_X2 , M1R_Y2 ),(0,255,0), -1)
            

            # Change velocity label
            if RIGHT_INDEX_FINGER_PIP_Y > height/2 and RIGHT_PINKY_FINGER_PIP_Y > height/2 and LOW==False:
                velocity_message = "BAJA"
                velocity_message_color = (0,255,0)
                LOW = True
                HIGH = False

            elif RIGHT_INDEX_FINGER_PIP_Y <= height/2 and RIGHT_PINKY_FINGER_PIP_Y <= height/2 and HIGH==False:
                velocity_message = "ALTA"
                velocity_message_color = (0,0,255)
                HIGH = True
                LOW = False
            
            # Center line
            # cv2.line(frame, (0,round(height/2)), (width,round(height/2)), (0,0,0), 2)

            cv2.putText(frame, "POS = {}".format(round(INIT_POSITIONS[MOTOR-1])), (M1L_X1,M1_TEXT_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.putText(frame, "VELOCIDAD = "+velocity_message, (M1L_X1-50,M1_TEXT_Y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, velocity_message_color, 2)
        
        if controlling and left_detected:
            LEFT_INDEX_FINGER_TIP_X = round(left_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
            LEFT_INDEX_FINGER_TIP_Y = round(left_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
            cv2.circle(frame, (LEFT_INDEX_FINGER_TIP_X,LEFT_INDEX_FINGER_TIP_Y),5,(0,0,255),6)

            cv2.rectangle(frame, (50, INFO_TEXT_Y+200 ) , ( 75 , INFO_TEXT_Y+200+25 ),(0,0,255), -1)
            cv2.rectangle(frame, (50, INFO_TEXT_Y+250 ) , ( 75 , INFO_TEXT_Y+200+75 ),(0,0,255), -1)
            cv2.rectangle(frame, (50, INFO_TEXT_Y+300 ) , ( 75 , INFO_TEXT_Y+200+125 ),(0,0,255), -1)
            cv2.rectangle(frame, (50, INFO_TEXT_Y+350 ) , ( 75 , INFO_TEXT_Y+200+175 ),(0,0,255), -1)
            cv2.rectangle(frame, (50, INFO_TEXT_Y+400 ) , ( 75 , INFO_TEXT_Y+200+225 ),(0,0,255), -1)

            cv2.putText(frame, "M5", (5,INFO_TEXT_Y+220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1)
            cv2.putText(frame, "M4", (5,INFO_TEXT_Y+270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1)
            cv2.putText(frame, "M3", (5,INFO_TEXT_Y+320), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1)
            cv2.putText(frame, "M2", (5,INFO_TEXT_Y+370), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1)
            cv2.putText(frame, "M1", (5,INFO_TEXT_Y+420), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1)

            if LEFT_INDEX_FINGER_TIP_X > 50 and  LEFT_INDEX_FINGER_TIP_Y > INFO_TEXT_Y+200 and LEFT_INDEX_FINGER_TIP_X < 75 and LEFT_INDEX_FINGER_TIP_Y < INFO_TEXT_Y+200+25:
                MOTOR = 5
                MIN_POS = 80
                MAX_POS = 180
                MASC = 4000
                cv2.rectangle(frame, (50, INFO_TEXT_Y+200 ) , ( 75 , INFO_TEXT_Y+200+25 ),(0,255,0), -1)
            
            elif LEFT_INDEX_FINGER_TIP_X > 50 and  LEFT_INDEX_FINGER_TIP_Y > INFO_TEXT_Y+250 and LEFT_INDEX_FINGER_TIP_X < 75 and LEFT_INDEX_FINGER_TIP_Y < INFO_TEXT_Y+200+75:
                MOTOR = 4
                MIN_POS = 0
                MAX_POS = 180
                MASC = 3000
                cv2.rectangle(frame, (50, INFO_TEXT_Y+250 ) , ( 75 , INFO_TEXT_Y+200+75 ),(0,255,0), -1)
            elif LEFT_INDEX_FINGER_TIP_X > 50 and  LEFT_INDEX_FINGER_TIP_Y > INFO_TEXT_Y+300 and LEFT_INDEX_FINGER_TIP_X < 75 and LEFT_INDEX_FINGER_TIP_Y < INFO_TEXT_Y+200+125:
                MOTOR = 3
                MIN_POS = 0
                MAX_POS = 180
                MASC = 2000
                cv2.rectangle(frame, (50, INFO_TEXT_Y+300 ) , ( 75 , INFO_TEXT_Y+200+125 ),(0,255,0), -1)
            
            elif LEFT_INDEX_FINGER_TIP_X > 50 and  LEFT_INDEX_FINGER_TIP_Y > INFO_TEXT_Y+350 and LEFT_INDEX_FINGER_TIP_X < 75 and LEFT_INDEX_FINGER_TIP_Y < INFO_TEXT_Y+200+175:
                MOTOR = 2
                MIN_POS = 50
                MAX_POS = 180
                MASC = 1000
                cv2.rectangle(frame, (50, INFO_TEXT_Y+350 ) , ( 75 , INFO_TEXT_Y+200+175 ),(0,255,0), -1)
            
            elif LEFT_INDEX_FINGER_TIP_X > 50 and  LEFT_INDEX_FINGER_TIP_Y > INFO_TEXT_Y+400 and LEFT_INDEX_FINGER_TIP_X < 75 and LEFT_INDEX_FINGER_TIP_Y < INFO_TEXT_Y+200+225:
                MOTOR = 1
                MIN_POS = 0
                MAX_POS = 180
                MASC = 0
                cv2.rectangle(frame, (50, INFO_TEXT_Y+400 ) , ( 75 , INFO_TEXT_Y+200+225 ),(0,255,0), -1)
            
        if controlling and CONNECT_TO_SERVER:
            # Send angle to server
            socketIO.emit("nuevo_mensaje",str((INIT_POSITIONS[MOTOR-1]+MASC))+'\n')
            # print(str(M1))

        right_detected = False
        left_detected = False


    else:
        controlling_hand_message = "NINGUNA"
        controlling_message = "NO"
        controlling_message_color = (0,0,0)
        controlling = False
    
    cv2.putText(frame, "MANO DETECTADA: "+controlling_hand_message,(INFO_TEXT_X,INFO_TEXT_Y),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 0),2)
    cv2.putText(frame, "CONTROLANDO ROBOT: "+controlling_message,(INFO_TEXT_X,INFO_TEXT_Y+35),cv2.FONT_HERSHEY_SIMPLEX,0.8,controlling_message_color,2)
    cv2.putText(frame, "MOTOR: "+str(MOTOR)+" ["+str(MIN_POS)+","+str(MAX_POS)+"]",(INFO_TEXT_X,INFO_TEXT_Y+70),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 0),2)
        
    cv2.imshow("Frame", frame)
    time.sleep(0.005)
    if cv2.waitKey(5) & 0xFF == 27:
        break



cap.release()
cv2.destroyAllWindows()

        
