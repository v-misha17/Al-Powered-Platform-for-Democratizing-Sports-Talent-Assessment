import cv2
import numpy as np
from scipy.signal import find_peaks
import tempfile
import os
import json

def extract_frames(video_path, num_frames=8):
    """Extract frames from video using OpenCV"""
    frames = []
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate frame indices to extract
    if total_frames <= num_frames:
        frame_indices = range(total_frames)
    else:
        frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
    
    for i in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
    
    cap.release()
    return frames

def simulate_sport_prediction(frames):
    """Simulate sport prediction - but we won't use this for assessment"""
    sports = ['Javelin Throw', 'Table Tennis', 'Archery', 'Push-ups', 'Discus Throw', 'High Jump']
    return np.random.choice(sports)

def simulate_pose_estimation(frames):
    """Simulate pose estimation results"""
    keypoints = []
    for frame in frames:
        height, width = frame.shape[:2]
        # Simulate some random keypoints
        if np.random.random() > 0.2:  # 80% chance of detection
            kps = np.random.rand(10, 2) * [width, height]
            keypoints.append(kps)
        else:
            keypoints.append(None)
    return keypoints

def assess_javelin_metrics(keypoints_list, frames):
    """Simulate javelin metrics assessment"""
    coverage = sum(1 for kp in keypoints_list if kp is not None) / max(1, len(keypoints_list))
    return {
        "pose_coverage_ratio": round(coverage, 3),
        "release_angle_deg": round(np.random.uniform(25, 40), 1),
        "max_wrist_speed_px_per_frame": round(np.random.uniform(5, 20), 1)
    }

def assess_table_tennis_metrics(keypoints_list, frames):
    """Simulate table tennis metrics assessment"""
    coverage = sum(1 for kp in keypoints_list if kp is not None) / max(1, len(keypoints_list))
    return {
        "pose_coverage_ratio": round(coverage, 3),
        "rally_count": np.random.randint(1, 10),
        "avg_wrist_speed_px": round(np.random.uniform(2, 8), 1),
        "peak_wrist_speed_px": round(np.random.uniform(8, 15), 1)
    }

def assess_archery_metrics(keypoints_list, frames):
    """Simulate archery metrics assessment"""
    coverage = sum(1 for kp in keypoints_list if kp is not None) / max(1, len(keypoints_list))
    return {
        "pose_coverage_ratio": round(coverage, 3),
        "max_draw_ratio": round(np.random.uniform(0.8, 1.4), 2)
    }

def assess_pushups_metrics(keypoints_list, frames):
    """Simulate push-ups metrics assessment"""
    coverage = sum(1 for kp in keypoints_list if kp is not None) / max(1, len(keypoints_list))
    return {
        "pose_coverage_ratio": round(coverage, 3),
        "pushup_reps": np.random.randint(5, 20),
        "pushup_depth": round(np.random.uniform(0.3, 0.9), 2)
    }

def assess_discus_metrics(keypoints_list, frames):
    """Simulate discus metrics assessment"""
    coverage = sum(1 for kp in keypoints_list if kp is not None) / max(1, len(keypoints_list))
    return {
        "pose_coverage_ratio": round(coverage, 3),
        "max_wrist_speed_px_per_frame": round(np.random.uniform(5, 15), 1),
        "hip_rotation_range_px": round(np.random.uniform(30, 60), 1)
    }

def assess_highjump_metrics(keypoints_list, frames):
    """Simulate high jump metrics assessment"""
    coverage = sum(1 for kp in keypoints_list if kp is not None) / max(1, len(keypoints_list))
    return {
        "pose_coverage_ratio": round(coverage, 3),
        "hip_vertical_displacement": round(np.random.uniform(40, 80), 1),
        "takeoff_angle_deg": round(np.random.uniform(65, 85), 1)
    }

def generate_report(sport, metrics):
    """Generate assessment report and rating"""
    score = 0
    
    if sport == "Javelin Throw":
        if metrics.get("release_angle_deg") and 30 <= metrics["release_angle_deg"] <= 36:
            score += 4
        if metrics.get("max_wrist_speed_px_per_frame"):
            score += 3
        score += 3 * metrics.get("pose_coverage_ratio", 0)

    elif sport == "Table Tennis":
        score += min(4, metrics.get("rally_count", 0)/2)
        if metrics.get("peak_wrist_speed_px") and metrics.get("avg_wrist_speed_px") and metrics["peak_wrist_speed_px"] > metrics["avg_wrist_speed_px"]*1.5:
            score += 2
        score += 4 * metrics.get("pose_coverage_ratio", 0)

    elif sport == "Archery":
        if 0.9 <= metrics.get("max_draw_ratio", 0) <= 1.3:
            score += 5
        score += 5 * metrics.get("pose_coverage_ratio", 0)

    elif sport == "Push-ups":
        score += min(6, metrics.get("pushup_reps", 0) * 0.5)
        if metrics.get("pushup_depth") and metrics["pushup_depth"] > 0.5:
            score += 2
        score += 2 * metrics.get("pose_coverage_ratio", 0)

    elif sport == "Discus Throw":
        if metrics.get("max_wrist_speed_px_per_frame"):
            score += 5
        if metrics.get("hip_rotation_range_px"):
            score += 3
        score += 2 * metrics.get("pose_coverage_ratio", 0)

    elif sport == "High Jump":
        if metrics.get("hip_vertical_displacement"):
            score += min(6, metrics["hip_vertical_displacement"] / 50)
        if metrics.get("takeoff_angle_deg") and 70 <= metrics["takeoff_angle_deg"] <= 80:
            score += 3
        score += 1 * metrics.get("pose_coverage_ratio", 0)

    final_rating = round(score, 1)
    return final_rating

def process_video_assessment(assessment):
    """Process video and generate assessment results - ALWAYS use user-selected sport"""
    try:
        # Extract frames from video
        frames = extract_frames(assessment.video.path)
        
        # Simulate sport prediction (just for display, not used for assessment)
        assessment.predicted_sport = assessment.sport_type
        
        # ALWAYS use the sport selected by the user from dropdown
        sport = assessment.sport_type
        
        # Simulate pose estimation
        keypoints_list = simulate_pose_estimation(frames)
        
        # Run sport-specific assessment based on USER SELECTION
        sport_assessors = {
            "Javelin Throw": assess_javelin_metrics,
            "Table Tennis": assess_table_tennis_metrics,
            "Archery": assess_archery_metrics,
            "Push-ups": assess_pushups_metrics,
            "Discus Throw": assess_discus_metrics,
            "High Jump": assess_highjump_metrics,
        }
        
        if sport in sport_assessors:
            metrics = sport_assessors[sport](keypoints_list, frames)
            rating = generate_report(sport, metrics)
            
            # Use json.dumps for proper serialization
            assessment.metrics = json.dumps(metrics)
            assessment.rating = rating
            assessment.processed = True
            assessment.save()
            
            return assessment, None
        else:
            return None, f"Sport '{sport}' is not supported"
            
    except Exception as e:
        return None, f"Error processing video: {str(e)}"