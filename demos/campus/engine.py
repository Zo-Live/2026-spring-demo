from __future__ import annotations

from random import Random

from demos.campus.config import ACTION_BY_BUILDING, BUILDINGS, MAX_HOURS, TRAITS
from demos.campus.models import GameState, Student
from demos.campus.rules import (
    apply_effect,
    apply_energy_cost,
    can_execute_here,
    current_day_hour,
    distance_hours,
    is_open,
    team_score,
    update_debuffs_and_achievements,
)


class CampusGame:
    def __init__(self, rng: Random) -> None:
        students = [
            Student(name="S1", trait=rng.choice(TRAITS)),
            Student(name="S2", trait=rng.choice(TRAITS)),
            Student(name="S3", trait=rng.choice(TRAITS)),
        ]
        for student in students:
            if student.trait == "frail":
                student.max_energy = 80
                student.energy = 80
        self.state = GameState(students=students, max_hours=MAX_HOURS)

    def step(self, commands: dict[str, str]) -> None:
        if self.state.is_terminal:
            raise ValueError("game already finished")
        _, hour = current_day_hour(self.state.hour_index)
        occupied: dict[str, int] = {}
        step_log: list[str] = []
        for student in self.state.students:
            command = commands.get(student.name, "wait")
            if student.travel_remaining > 0:
                student.travel_remaining -= 1
                if student.travel_remaining == 0 and student.target is not None:
                    student.location = student.target
                    student.last_action = f"arrived:{student.location}"
                    student.target = None
                else:
                    student.last_action = f"moving:{student.target}:{student.travel_remaining}"
                update_debuffs_and_achievements(student)
                step_log.append(f"{student.name} {student.last_action}")
                continue

            if command == "wait":
                apply_effect(student, "wait", hour)
                student.last_action = "wait"
                update_debuffs_and_achievements(student)
                step_log.append(f"{student.name} waits at {student.location}")
                continue

            if command not in BUILDINGS:
                student.last_action = "invalid_command"
                update_debuffs_and_achievements(student)
                step_log.append(f"{student.name} invalid command {command}")
                continue

            target = command
            if student.location != target:
                travel = distance_hours(student.location, target, "fatigue" in student.debuffs)
                future_hour = (self.state.hour_index + travel) % 24
                if not is_open(target, future_hour):
                    student.last_action = "invalid_closed_on_arrival"
                    update_debuffs_and_achievements(student)
                    step_log.append(f"{student.name} could not start moving to {target}: closed on arrival")
                    continue
                student.energy -= apply_energy_cost(student, 2 * travel)
                student.satiety -= travel
                if travel <= 1:
                    student.location = target
                    student.target = None
                    student.travel_remaining = 0
                    student.last_action = f"arrived:{target}"
                else:
                    student.target = target
                    student.travel_remaining = travel - 1
                    student.last_action = f"moving:{target}:{student.travel_remaining}"
                update_debuffs_and_achievements(student)
                step_log.append(f"{student.name} starts moving to {target} ({travel}h)")
                continue

            allowed, reason = can_execute_here(student, target, hour, occupied)
            if not allowed:
                student.last_action = f"invalid:{reason}"
                apply_effect(student, "wait", hour)
                update_debuffs_and_achievements(student)
                step_log.append(f"{student.name} could not {ACTION_BY_BUILDING[target]}: {reason}")
                continue

            occupied[target] = occupied.get(target, 0) + 1
            action_name = ACTION_BY_BUILDING[target]
            was_hungry = "hunger" in student.debuffs
            apply_effect(student, action_name, hour)
            if was_hungry and action_name in {"study", "class"}:
                student.credits -= 8 if action_name == "class" else 5
            student.last_action = action_name
            update_debuffs_and_achievements(student)
            step_log.append(f"{student.name} performs {action_name} at {target}")

        self.state.log.extend(step_log)
        self.state.log.append(f"Team score: {team_score(self.state):.1f}")
        self.state.hour_index += 1
