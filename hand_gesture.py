                                 # HAND GESTURE GAME CONTROLLER

import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

LEFT_LANE_BOUND = 0.38
RIGHT_LANE_BOUND = 0.62

DEAD_ZONE_LEFT = 0.43
DEAD_ZONE_RIGHT = 0.57

FRAME_THRESHOLD = 3

LEFT_FRAMES = 0
RIGHT_FRAMES = 0

pTime = 0
active_action = "Idle"

gesture_state = {
    'move_left': False,
    'move_right': False,
    'jump': False,
    'duck': False
}

def press_and_release(key):
    keyboard.press(key)
    keyboard.release(key)

def hold_key(key):
    keyboard.press(key)

def release_key(key):
    keyboard.release(key)

def fingers_extended(hand):
    extended = []
    extended.append(hand.landmark[4].y < hand.landmark[3].y)  
    for tip in [8, 12, 16, 20]:
        extended.append(hand.landmark[tip].y < hand.landmark[tip - 2].y)
    return extended

def is_jump(hand):
    extended = fingers_extended(hand)
    return not any(extended[1:])  

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    current_action = {
        'move_left': False,
        'move_right': False,
        'jump': False,
        'duck': False
    }

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        thumb = hand.landmark[4]
        index = hand.landmark[8]
        center_x = (thumb.x + index.x) / 2

        extended = fingers_extended(hand)
        finger_count = sum(extended)

        if center_x < LEFT_LANE_BOUND:
            LEFT_FRAMES += 1
            RIGHT_FRAMES = 0
        elif center_x > RIGHT_LANE_BOUND:
            RIGHT_FRAMES += 1
            LEFT_FRAMES = 0
        elif DEAD_ZONE_LEFT <= center_x <= DEAD_ZONE_RIGHT:
            LEFT_FRAMES = 0
            RIGHT_FRAMES = 0

        current_action['move_left'] = LEFT_FRAMES >= FRAME_THRESHOLD
        current_action['move_right'] = RIGHT_FRAMES >= FRAME_THRESHOLD

        if is_jump(hand):
            current_action['jump'] = True

        elif (finger_count == 2 and extended[0] and extended[4] and
              not extended[1] and not extended[2] and not extended[3]):
            current_action['duck'] = True

        if current_action['jump'] or current_action['duck']:
            LEFT_FRAMES = 0
            RIGHT_FRAMES = 0
            current_action['move_left'] = False
            current_action['move_right'] = False

    if current_action['move_left']:
        if not gesture_state['move_left']:
            hold_key(Key.left)
            gesture_state['move_left'] = True
        active_action = "LEFT"
    else:
        if gesture_state['move_left']:
            release_key(Key.left)
            gesture_state['move_left'] = False

    if current_action['move_right']:
        if not gesture_state['move_right']:
            hold_key(Key.right)
            gesture_state['move_right'] = True
        active_action = "RIGHT"
    else:
        if gesture_state['move_right']:
            release_key(Key.right)
            gesture_state['move_right'] = False

    if current_action['jump'] and not gesture_state['jump']:
        press_and_release(Key.up)
        gesture_state['jump'] = True
        active_action = "JUMP"
    elif not current_action['jump']:
        gesture_state['jump'] = False

  
    if current_action['duck'] and not gesture_state['duck']:
        press_and_release(Key.down)
        gesture_state['duck'] = True
        active_action = "DUCK"
    elif not current_action['duck']:
        gesture_state['duck'] = False

    if not any(current_action.values()):
        active_action = "Idle (Middle)"

    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime

    cv2.putText(image, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(image, f'Action: {active_action}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

