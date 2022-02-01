import math
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import get_qubit_state

def epl_protocol_alice(q1, q2, alice, socket):
    """
    Implements Alice's side of the EPL distillation protocol.
    This function should perform the gates and measurements for EPL using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    ma = epl_gates_and_measurement_alice(q1, q2)
    alice.flush()

    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    
    # Alice sends measurement of 2A to Bob
    socket.send_structured(StructuredMessage("Measurement Alice",int(ma)))

    # Alice receives Bob's measurement
    mb_ = socket.recv_structured().payload

    # Protocol is succesful if 2A and 2B are 11
    return int(ma)==1 and int(mb_)==1


def epl_gates_and_measurement_alice(q1, q2):
    
    """
    Performs the gates and measurements for Alice's side of the EPL protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :return: Integer 0/1 indicating Alice's measurement outcome
    """
    # CNOT A1->A2 
    q1.cnot(q2)

    # Measure A2 in comp. basis
    m = q2.measure()
    return m


def epl_protocol_bob(q1, q2, bob, socket):
    """
    Implements Bob's side of the EPL distillation protocol.
    This function should perform the gates and measurements for EPL using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    
    # Perform operations on EPR pairs
    mb = epl_gates_and_measurement_bob(q1, q2)
    bob.flush()

    # Write below the code to send measurement result to Alice, receive measurement result from Alice and check if protocol was successful
    
    # Bob sends measurement of 2B to Alice
    ma_ = socket.recv_structured().payload
   
    # Bob receives Alice's measurement
    socket.send_structured(StructuredMessage("Measurement Bob!", int(mb)))

    # Protocol is succesful if 2A and 2B are 11
    return int(mb)==1 and int(ma_)==1

def epl_gates_and_measurement_bob(q1, q2):
    """
    Performs the gates and measurements for Bob's side of the EPL protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :return: Integer 0/1 indicating Bob's measurement outcome
    """
    # CNOT B1->B2 
    q1.cnot(q2)

    # Measure B2 in comp. basis
    m = q2.measure()
    return m

