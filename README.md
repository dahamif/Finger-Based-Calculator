# 🧮 Finger-Based Calculator Using OpenCV on Raspberry Pi

## 📌 Project Description

This is a touchless, interactive calculator built using **Python**, **OpenCV**, **MediaPipe**, and a **Raspberry Pi**. It uses a webcam to recognize **finger counting gestures** in real time to perform basic arithmetic operations. All inputs—both numbers and operators—are entered **solely through finger counting**, making it completely hands-free and intuitive.

The project uses **MediaPipe's real-time hand tracking solution** to detect hand landmarks and count fingers accurately. Numbers are recognized by detecting the **total number of fingers lifted across both hands**, and operations are mapped to **predefined finger-count gestures**.

Inspired by the way children engage with learning content like **Miss Rachel**, this project is designed to make math practice fun, visual, and physically engaging. 


📽️ **[Watch Demo Video](https://drive.google.com/file/d/178CVBzBMGe8PC25os6muF-VEIGARWwdc/view?usp=sharing)**

---


## 🕒 How it works

The calculator uses a timer-based gesture input system to ensure accurate recognition. Here's the step-by-step flow:

1. **Show First Number (0–10)**  
   Display the number using fingers on both hands.  
   A timer (e.g., 2–3 seconds) runs.  
   When the timer expires, the last stable gesture is taken as input.

2. **Show Operator**  
   Use a finger-count gesture to indicate the operation (e.g., 1 for addition).  
   Timer activates and records the operator.

3. **Show Second Number (0–10)**  
   Use both hands again to show the second number.  
   After the timer, the input is locked in.

4. **View Result**  
   The result is displayed visually on the screen along with the given inputs.

---

## ➗ Supported Math Operations

 ✋ Fingers Detected        | 🔣 Mapped Operation   |
|---------------------------|----------------------  |
| ✊ 0 fingers (closed fist) | ➕ Addition (+)      |
| 👎 1 finger (thumbs down) | ➖ Subtraction (−)    |
| ✌️ 2 fingers (peace sign) | ✖️ Multiplication (*) |
| 🖐️ 5 fingers (open palm)  | ➗ Division (/)       |

- **Numbers 0–10** are input using total finger count across both hands.
- **All input is based solely on visual finger counting.**

---

## 🛠️ Technologies Used

- Raspberry Pi (tested on Pi 3/4 with USB webcam)
- Python 3
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy

---


