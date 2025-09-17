import json
import gates
import circuit
class QASM3_GENERATOR:
    def __init__(self):
        pass
    # parse function:
    #      If validate fails: returns a dict of 'message' and 'ok' of type boolean
    #      If validate successfully, returns circuit
    def validate_and_parse(self,input:str) -> dict:
        try:
            json_input = json.loads(input)
        except:
            return {
                "message" : "Invalid JSON",
                "ok" : False
            }
        try:
            number_of_qubits = int(json_input["number_of_qubits"])
            if number_of_qubits > 5 or number_of_qubits < 1:
                return {
                    "message" : "Number of qubits must be between 1 and 5",
                    "ok" : False
                }
        except:
            return {
                "message" : "Number of qubits must be a positive integer",
                "ok" : False
            }
        try:
            qubits_initial_values = json_input["qubits_initial_values"]
            if len(qubits_initial_values) != number_of_qubits:
                return {
                        "message" : "length of list not equal number of qubits",
                        "ok" : False
                    }
            for i in range(number_of_qubits):
                if qubits_initial_values[i] != 1 and qubits_initial_values[i] != 0:
                    return {
                        "message" : "Initial qubits value must be 1 or 0",
                        "ok" : False
                    }
        except:
            return {
                "message" : "qubits initial values not given",
                "ok" : False
            }
        try:
            operations_at_time = json_input["operations_at_time"]
            for i in range(len(operations_at_time)):
                try:
                    operation = operations_at_time[i]["operation"]
                    qubits_affected = operations_at_time[i]["qubits_affected"]
                except:
                    return {
                        "message" : f"operation or qubits affected not given at time {i}",
                        "ok" : False
                    }
                try:
                    angle = operations_at_time[i]["angle"]
                except:
                    angle = None

                msg = gates.Gate.is_valid_gate(operation,len(qubits_affected),angle)
                if not msg["ok"]:
                    return {
                        "message" : msg["message"],
                        "ok" : False
                    }
        except:
            return {
                "message" : "operations_at_time not given",
                "ok" : False
            }
        return {
            "message": json_input,
            "ok": True
        }

    def generate_qasm3_from_json(self, input: str):
        data = self.validate_and_parse(input)
        if not data["ok"]:
            raise RuntimeError(data["message"])
        
        data = data["message"]
        number_of_qubits = data["number_of_qubits"]
        qubits_initial_values = data["qubits_initial_values"]
        operations_at_time = data["operations_at_time"]
        lines = []

        lines.append("OPENQASM 3.0;")
        lines.append('include "stdgates.inc";')
        lines.append(f"qubit[{number_of_qubits}] q;")
        lines.append(f"bit[{number_of_qubits}] c;")
        
        for i in range(len(qubits_initial_values)):
            if qubits_initial_values[i] == 1:
                lines.append(f"x q[{i}];")
        
        for i in range(len(operations_at_time)):
            operation = operations_at_time[i]["operation"]
            qubits_affected = operations_at_time[i]["qubits_affected"]

            if gates.Gate.is_rotation_gate(operation):
                angle = operations_at_time[i]["angle"]
                lines.append(f"{operation}({angle}) q[{qubits_affected[0]}];")
            elif gates.Gate.is_controlled_gate(operation):
                lines.append(f"{operation} q[{qubits_affected[0]}], q[{qubits_affected[1]}];")
            else:
                lines.append(f"{operation} q[{qubits_affected[0]}];")

        for i in range(number_of_qubits):
            lines.append(f"measure q[{i}] -> c[{i}];")