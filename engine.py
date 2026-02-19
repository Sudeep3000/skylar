from sheets import read_sheet
from datetime import datetime



def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


def date_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1


def calculate_cost(pilot, mission):
    start = parse_date(mission["start_date"])
    end = parse_date(mission["end_date"])
    duration = (end - start).days + 1
    return duration * int(pilot["daily_rate"])




def check_pilot_conflict(pilot, mission, missions):
    for _, m in missions.iterrows():
        if m.get("assigned_pilot") == pilot["name"]:
            if date_overlap(
                parse_date(mission["start_date"]),
                parse_date(mission["end_date"]),
                parse_date(m["start_date"]),
                parse_date(m["end_date"]),
            ):
                return "Pilot is double-booked"
    return None


def check_skill(pilot, mission):
    if mission["required_skill"] not in pilot["skills"]:
        return "Skill mismatch"
    return None


def check_certification(pilot, mission):
    if mission["required_cert"] not in pilot["certifications"]:
        return "Certification mismatch"
    return None


def check_weather(drone, mission):
    if mission["weather"] == "Rainy" and drone["weather_rating"] == "Generic":
        return "Drone not waterproof"
    return None


# Core Logic
def match_pilot(mission, pilots, missions):
    best_candidate = None
    best_score = -1

    for _, pilot in pilots.iterrows():
        if pilot["status"] != "Available":
            continue

        score = 0

        if mission["required_skill"] in pilot["skills"]:
            score += 50

        if mission["required_cert"] in pilot["certifications"]:
            score += 30

        if mission["location"] == pilot["location"]:
            score += 10

        conflict = check_pilot_conflict(pilot, mission, missions)
        if conflict:
            continue

        if score > best_score:
            best_score = score
            best_candidate = pilot

    return best_candidate


def match_drone(mission, drones):
    for _, drone in drones.iterrows():
        if drone["status"] != "Available":
            continue

        if mission["location"] != drone["location"]:
            continue

        weather_issue = check_weather(drone, mission)
        if weather_issue:
            continue

        return drone

    return None



def assign_mission(project_id):
    pilots = read_sheet("Pilot_Roster")
    drones = read_sheet("Drone_Fleet")
    missions = read_sheet("Missions")

    mission = missions[missions["project_id"] == project_id].iloc[0]

    pilot = match_pilot(mission, pilots, missions)
    drone = match_drone(mission, drones)

    if pilot is None:
        return {"error": "No suitable pilot found"}

    if drone is None:
        return {"error": "No suitable drone found"}

    cost = calculate_cost(pilot, mission)

    warnings = []

    if cost > int(mission["budget"]):
        warnings.append("Budget exceeded")

    if mission["location"] != drone["location"]:
        warnings.append("Location mismatch")

    return {
        "recommended_pilot": pilot["name"],
        "recommended_drone": drone["drone_id"],
        "estimated_cost": cost,
        "warnings": warnings
    }


def urgent_reassignment(project_id):
    # simply re-run assignment logic
    return assign_mission(project_id)
