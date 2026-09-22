import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyStudyEngine:
    def __init__(self):

        # =====================================================
        # INPUT VARIABLES - ANTECEDENTS
        # =====================================================

        # Student mastery percentage: 0 - 100
        self.mastery = ctrl.Antecedent(
            np.arange(0, 101, 1),
            "mastery"
        )

        # Topic difficulty: 1 - 10
        self.difficulty = ctrl.Antecedent(
            np.arange(1, 11, 1),
            "difficulty"
        )

        # Number of days remaining until the exam: 0 - 30
        self.exam_distance = ctrl.Antecedent(
            np.arange(0, 31, 1),
            "exam_distance"
        )

        # =====================================================
        # OUTPUT VARIABLE - CONSEQUENT
        # =====================================================

        # Final study priority: 0 - 100
        self.study_priority = ctrl.Consequent(
            np.arange(0, 101, 1),
            "study_priority"
        )

        # Create fuzzy membership functions and rules
        self._define_membership_functions()
        self._create_rules()

    # =========================================================
    # MEMBERSHIP FUNCTIONS
    # =========================================================

    def _define_membership_functions(self):

        # -----------------------------
        # MASTERY
        # -----------------------------

        self.mastery["low"] = fuzz.trapmf(
            self.mastery.universe,
            [0, 0, 30, 50]
        )

        self.mastery["medium"] = fuzz.trimf(
            self.mastery.universe,
            [30, 50, 70]
        )

        self.mastery["high"] = fuzz.trapmf(
            self.mastery.universe,
            [50, 70, 100, 100]
        )

        # -----------------------------
        # DIFFICULTY
        # -----------------------------

        self.difficulty["easy"] = fuzz.trapmf(
            self.difficulty.universe,
            [1, 1, 3, 5]
        )

        self.difficulty["moderate"] = fuzz.trimf(
            self.difficulty.universe,
            [3, 5, 8]
        )

        self.difficulty["hard"] = fuzz.trapmf(
            self.difficulty.universe,
            [6, 8, 10, 10]
        )

        # -----------------------------
        # EXAM DISTANCE
        # -----------------------------

        self.exam_distance["near"] = fuzz.trapmf(
            self.exam_distance.universe,
            [0, 0, 3, 7]
        )

        self.exam_distance["medium"] = fuzz.trimf(
            self.exam_distance.universe,
            [4, 10, 16]
        )

        self.exam_distance["far"] = fuzz.trapmf(
            self.exam_distance.universe,
            [12, 18, 30, 30]
        )

        # -----------------------------
        # STUDY PRIORITY
        # -----------------------------

        self.study_priority["low"] = fuzz.trapmf(
            self.study_priority.universe,
            [0, 0, 20, 40]
        )

        self.study_priority["medium"] = fuzz.trimf(
            self.study_priority.universe,
            [30, 50, 70]
        )

        self.study_priority["high"] = fuzz.trimf(
            self.study_priority.universe,
            [60, 75, 90]
        )

        self.study_priority["very_high"] = fuzz.trapmf(
            self.study_priority.universe,
            [80, 90, 100, 100]
        )

    # =========================================================
    # FUZZY RULES
    # =========================================================

    def _create_rules(self):

        rules = [

            # =================================================
            # LOW MASTERY RULES
            # =================================================

            # Weak student + exam very close
            ctrl.Rule(
                self.mastery["low"]
                & self.exam_distance["near"],
                self.study_priority["very_high"]
            ),

            # Weak student + exam moderately close
            ctrl.Rule(
                self.mastery["low"]
                & self.exam_distance["medium"],
                self.study_priority["high"]
            ),

            # Weak student even if exam is far away
            ctrl.Rule(
                self.mastery["low"]
                & self.exam_distance["far"],
                self.study_priority["high"]
            ),

            # =================================================
            # MEDIUM MASTERY RULES
            # =================================================

            ctrl.Rule(
                self.mastery["medium"]
                & self.exam_distance["near"],
                self.study_priority["high"]
            ),

            ctrl.Rule(
                self.mastery["medium"]
                & self.exam_distance["medium"],
                self.study_priority["medium"]
            ),

            ctrl.Rule(
                self.mastery["medium"]
                & self.exam_distance["far"],
                self.study_priority["medium"]
            ),

            # =================================================
            # HIGH MASTERY RULES
            # =================================================

            ctrl.Rule(
                self.mastery["high"]
                & self.exam_distance["near"],
                self.study_priority["medium"]
            ),

            ctrl.Rule(
                self.mastery["high"]
                & self.exam_distance["medium"],
                self.study_priority["low"]
            ),

            ctrl.Rule(
                self.mastery["high"]
                & self.exam_distance["far"],
                self.study_priority["low"]
            ),

            # =================================================
            # DIFFICULTY-BASED RULES
            # =================================================

            # Difficult topic + exam close
            ctrl.Rule(
                self.difficulty["hard"]
                & self.exam_distance["near"],
                self.study_priority["very_high"]
            ),

            # Difficult topic + medium mastery
            ctrl.Rule(
                self.difficulty["hard"]
                & self.mastery["medium"],
                self.study_priority["high"]
            ),

            # Easy topic + already high mastery
            ctrl.Rule(
                self.difficulty["easy"]
                & self.mastery["high"],
                self.study_priority["low"]
            ),

            # Moderate difficulty + low mastery
            ctrl.Rule(
                self.difficulty["moderate"]
                & self.mastery["low"],
                self.study_priority["high"]
            )
        ]

        # Create the fuzzy control system
        self.control_system = ctrl.ControlSystem(rules)

    # =========================================================
    # CALCULATE PRIORITY
    # =========================================================

    def calculate_priority(
        self,
        mastery,
        difficulty,
        days_to_exam
    ):
        """
        Calculate the fuzzy study priority.

        mastery:
            Student mastery percentage from 0 to 100.

        difficulty:
            Topic difficulty from 1 to 10.

        days_to_exam:
            Number of days until the exam.

        Returns:
            Study priority score between 0 and 100.
        """

        # Keep values inside fuzzy system ranges
        mastery = max(0, min(mastery, 100))
        difficulty = max(1, min(difficulty, 10))
        days_to_exam = max(0, min(days_to_exam, 30))

        # Create a new fuzzy simulation
        simulation = ctrl.ControlSystemSimulation(
            self.control_system
        )

        # Send sensor/percept values into the fuzzy system
        simulation.input["mastery"] = mastery
        simulation.input["difficulty"] = difficulty
        simulation.input["exam_distance"] = days_to_exam

        # Run fuzzy inference
        simulation.compute()

        # Get the defuzzified crisp priority score
        priority = simulation.output["study_priority"]

        return round(priority, 2)