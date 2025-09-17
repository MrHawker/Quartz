ONE_QUBIT_GATES = ["x","y","z","h","s","sdg","t","tdg","measure"]
TWO_QUBITS_GATES = ["cx","cz"]
ROTATION_GATES = ["rx","ry","rz"]
ALLOWED_GATES = ["x","y","z","h","s","sdg","t","tdg","rx",
                     "ry","rz","cx","cz","measure"]
#TO DO: ADD RADIAN ANGLE CHECK
class Gate:
    def __init__(self,type: str):
        self.is_valid_gate(type)
    
    @staticmethod
    def is_controlled_gate(self,type:str):
        return type in TWO_QUBITS_GATES

    @staticmethod
    def is_rotation_gate(self,type:str):
        return type in ROTATION_GATES

    @staticmethod    
    def is_valid_gate(type:str,number_of_qubits_affected:int,angle: float | None) -> dict:
        if type not in ALLOWED_GATES:
            return {
                "message": "Gate not recognized",
                "ok" : False
            }
        if (type in ONE_QUBIT_GATES or type in ROTATION_GATES) and number_of_qubits_affected != 1:
            return {
                "message": f"{type} gate only acts on 1 qubit",
                "ok" : False
            }
        
        if type in ROTATION_GATES and angle == None:
            return {
                "message": f"{type} gate require an 'angle'",
                "ok" : False
            }
        if type in TWO_QUBITS_GATES and number_of_qubits_affected != 2:
            return {
                "message": f"{type} gate acts on 2 qubits",
                "ok" : False
            }
        return {
                "message": "OK",
                "ok" : True
            }