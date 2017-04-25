# Helper methods for observing what the camera is seeing
# If camera is not showing up, may need to hard-code a camera ID into the
# tracker code back in SpheroNav.

import cv2


# Video display
def display_tracking_window(tracker, traceable_object_list, exitKey="q"):
    """
        Given a list of traceable objects, track all objects in that list.
        Press exitKey to quit the window
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
        Display a single frame
    """
    image = tracker.get_video_frame()
    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_current_video(tracker):
    """
        Displays current video feed, press 'q' to escape
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
