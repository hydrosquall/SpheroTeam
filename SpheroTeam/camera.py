# camera.py
# Cameron Yick
# 4/24/2017

# Helper methods for observing the state of the ColorTracker()'s camera
import cv2


# Video display
def display_tracking_window(tracker, traceable_object_list, exitKey="q"):
    """
        Given a list of traceable objects, track all objects in that list.
        Press exitKey to quit the window

        :param tracker: A SpheroNav ColorTracker() object
        :param exitKey: A single letter, which if pressed, closes window
        :type traceable_object_list: List of SpheroNav traceable objects
    """

    while(True):
        tracker.track_objects(traceable_object_list)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord(exitKey):
            break

    cv2.destroyAllWindows()


# For Debugging
def display_current_view(tracker):
    """
        Display a single video frame in ipython window

        :param tracker: A SpheroNav ColorTracker() object
    """
    image = tracker.get_video_frame()
    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_current_video(tracker):
    """
        Displays current video feed, press 'q' to escape

        :param tracker: A SpheroNav ColorTracker() object
    """
    cam = tracker.cam
    while(True):
        # Capture frame-by-frame
        ret, frame = cam.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
