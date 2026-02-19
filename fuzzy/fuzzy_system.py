import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzySystem:
    def __init__(self):
        # ===== INPUT =====
        self.distance = ctrl.Antecedent(np.arange(0, 301, 1), 'distance')
        self.speed = ctrl.Antecedent(np.arange(0, 31, 1), 'speed')

        # ===== OUTPUT =====
        self.risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

        # ===== MEMBERSHIP FUNCTION =====
        self._define_membership()
        self._define_rules()

        self.system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.system)

    def _define_membership(self):
        # Distance (px)
        self.distance['sangat_dekat'] = fuzz.trapmf(self.distance.universe, [0, 0, 30, 60])
        self.distance['dekat']        = fuzz.trimf(self.distance.universe, [40, 80, 120])
        self.distance['sedang']       = fuzz.trimf(self.distance.universe, [100, 160, 220])
        self.distance['jauh']         = fuzz.trapmf(self.distance.universe, [180, 240, 300, 300])

        # Speed (px/frame)
        self.speed['diam']    = fuzz.trapmf(self.speed.universe, [0, 0, 1, 3])
        self.speed['lambat']  = fuzz.trimf(self.speed.universe, [2, 6, 10])
        self.speed['sedang']  = fuzz.trimf(self.speed.universe, [8, 14, 20])
        self.speed['cepat']   = fuzz.trapmf(self.speed.universe, [18, 22, 30, 30])

        # Risk (0–100)
        self.risk['aman']              = fuzz.trimf(self.risk.universe, [0, 20, 40])
        self.risk['waspada']           = fuzz.trimf(self.risk.universe, [30, 50, 70])
        self.risk['berbahaya']         = fuzz.trimf(self.risk.universe, [60, 75, 90])
        self.risk['sangat_berbahaya']  = fuzz.trimf(self.risk.universe, [80, 100, 100])

    def _define_rules(self):
        self.rules = [
            ctrl.Rule(self.distance['jauh'] & self.speed['diam'], self.risk['aman']),
            ctrl.Rule(self.distance['jauh'] & self.speed['lambat'], self.risk['aman']),
            ctrl.Rule(self.distance['jauh'] & self.speed['sedang'], self.risk['waspada']),
            ctrl.Rule(self.distance['jauh'] & self.speed['cepat'], self.risk['waspada']),

            ctrl.Rule(self.distance['sedang'] & self.speed['diam'], self.risk['aman']),
            ctrl.Rule(self.distance['sedang'] & self.speed['lambat'], self.risk['waspada']),
            ctrl.Rule(self.distance['sedang'] & self.speed['sedang'], self.risk['berbahaya']),
            ctrl.Rule(self.distance['sedang'] & self.speed['cepat'], self.risk['berbahaya']),

            ctrl.Rule(self.distance['dekat'] & self.speed['diam'], self.risk['waspada']),
            ctrl.Rule(self.distance['dekat'] & self.speed['lambat'], self.risk['berbahaya']),
            ctrl.Rule(self.distance['dekat'] & self.speed['sedang'], self.risk['sangat_berbahaya']),
            ctrl.Rule(self.distance['dekat'] & self.speed['cepat'], self.risk['sangat_berbahaya']),

            ctrl.Rule(self.distance['sangat_dekat'] & self.speed['diam'], self.risk['berbahaya']),
            ctrl.Rule(self.distance['sangat_dekat'] & self.speed['lambat'], self.risk['sangat_berbahaya']),
            ctrl.Rule(self.distance['sangat_dekat'] & self.speed['sedang'], self.risk['sangat_berbahaya']),
            ctrl.Rule(self.distance['sangat_dekat'] & self.speed['cepat'], self.risk['sangat_berbahaya']),
        ]

    def evaluate(self, distance_value, speed_value):
        self.simulation.input['distance'] = distance_value
        self.simulation.input['speed'] = speed_value
        self.simulation.compute()
        return self.simulation.output['risk']
