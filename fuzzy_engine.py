import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyStudyEngine:
    def __init__(self):

        # =====================================================
        # INPUT VARIABLES
        # =====================================================

        self.mastery = ctrl.Antecedent(
            np.arange(0, 101, 1),
            "mastery"
        )

        self.difficulty = ctrl.Antecedent(
            np.arange(1, 11, 1),
            "difficulty"
        )

        self.exam_distance = ctrl.Antecedent(
            np.arange(0, 31, 1),
            "exam_distance"
        )

        # -1 = declining
        #  0 = stable
        #  1 = improving
        self.performance_trend = ctrl.Antecedent(
            np.arange(-1, 1.01, 0.01),
            "performance_trend"
        )

        # =====================================================
        # OUTPUT VARIABLE
        # =====================================================

        self.study_priority = ctrl.Consequent(
            np.arange(0, 101, 1),
            "study_priority"
        )

        self._define_membership_functions()
        self._create_rules()

    # =========================================================
    # MEMBERSHIP FUNCTIONS
    # =========================================================

    def _define_membership_functions(self):

        # MASTERY
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

        # DIFFICULTY
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

        # EXAM DISTANCE
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

        # PERFORMANCE TREND
        self.performance_trend["declining"] = fuzz.trapmf(
            self.performance_trend.universe,
            [-1, -1, -0.5, 0]
        )

        self.performance_trend["stable"] = fuzz.trimf(
            self.performance_trend.universe,
            [-0.5, 0, 0.5]
        )

        self.performance_trend["improving"] = fuzz.trapmf(
            self.performance_trend.universe,
            [0, 0.5, 1, 1]
        )

        # STUDY PRIORITY
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

            # LOW MASTERY
            ctrl.Rule(
                self.mastery["low"]
                & self.exam_distance["near"],
                self.study_priority["very_high"]
            ),

            ctrl.Rule(
                self.mastery["low"]
                & self.exam_distance["medium"],
                self.study_priority["high"]
            ),

            ctrl.Rule(
                self.mastery["low"]
                & self.exam_distance["far"],
                self.study_priority["high"]
            ),

            # MEDIUM MASTERY
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

            # HIGH MASTERY
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

            # DIFFICULTY
            ctrl.Rule(
                self.difficulty["hard"]
                & self.exam_distance["near"],
                self.study_priority["very_high"]
            ),

            ctrl.Rule(
                self.difficulty["hard"]
                & self.mastery["medium"],
                self.study_priority["high"]
            ),

            ctrl.Rule(
                self.difficulty["easy"]
                & self.mastery["high"],
                self.study_priority["low"]
            ),

            ctrl.Rule(
                self.difficulty["moderate"]
                & self.mastery["low"],
                self.study_priority["high"]
            ),

            # =================================================
            # PERFORMANCE TREND RULES
            # =================================================

            # Falling performance close to an exam needs attention
            ctrl.Rule(
                self.performance_trend["declining"]
                & self.exam_distance["near"],
                self.study_priority["very_high"]
            ),

            # Declining performance with medium mastery
            ctrl.Rule(
                self.performance_trend["declining"]
                & self.mastery["medium"],
                self.study_priority["high"]
            ),

            # Improvement can reduce urgency when the exam is not close
            ctrl.Rule(
                self.performance_trend["improving"]
                & self.mastery["medium"]
                & self.exam_distance["far"],
                self.study_priority["medium"]
            ),

            # High mastery and improving performance
            ctrl.Rule(
                self.performance_trend["improving"]
                & self.mastery["high"],
                self.study_priority["low"]
            )
        ]

        self.control_system = ctrl.ControlSystem(rules)

    # =========================================================
    # CALCULATE PRIORITY
    # =========================================================

    def calculate_priority(
        self,
        mastery,
        difficulty,
        days_to_exam,
        performance_trend="stable"
    ):

        mastery = max(0, min(mastery, 100))
        difficulty = max(1, min(difficulty, 10))
        days_to_exam = max(0, min(days_to_exam, 30))

        trend_values = {
            "declining": -1,
            "stable": 0,
            "improving": 1,
            "insufficient data": 0
        }

        trend_value = trend_values.get(
            performance_trend,
            0
        )

        simulation = ctrl.ControlSystemSimulation(
            self.control_system
        )

        simulation.input["mastery"] = mastery
        simulation.input["difficulty"] = difficulty
        simulation.input["exam_distance"] = days_to_exam
        simulation.input["performance_trend"] = trend_value

        simulation.compute()

        priority = simulation.output["study_priority"]

        return round(priority, 2)