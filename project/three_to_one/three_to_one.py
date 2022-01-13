import math
from netqasm.sdk.classical_communication.message import StructuredMessage

def three_to_one_protocol_alice(q1, q2, q3, alice, socket):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for 3->1 using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param q3: Alice's qubit from the third entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    outcome1, outcome2 = three_to_one_gates_and_measurement_alice(q1, q2, q3)
    print("flushing now")
    alice.flush()
    print("alice done")
    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    
    # Alice receives Bob's measurement
    outcome_bob1 = socket.recv_structured().payload
    outcome_bob2 = socket.recv_structured().payload
    print("received")
    # Alice sends measurement of 2A to Bob
    socket.send_structured(StructuredMessage("Measurement Alice 1",int(outcome1)))
    socket.send_structured(StructuredMessage("Measurement Alice 2",int(outcome2)))
    print("sent")
    return int(outcome1)==outcome_bob1 and int(outcome2) == outcome_bob2

def three_to_one_gates_and_measurement_alice(q1, q2, q3):
    """
    Performs the gates and measurements for Alice's side of the 3->1 protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param q3: Alice's qubit from the third entangled pair
    :return: A pair of integer 0/1 indicating Alice's measurement outcomes from measuring the qubits
    """
    # CNOT A3->A2 
    q3.cnot(q2)

    # CNOT A1->A3
    q1.cnot(q3)

    #Bell measurement A1 A2
    q1.cnot(q2)
    
    q1.H()
    
    m1 = q1.measure()
    m2 = q2.measure()
    
    return m1,m2


def three_to_one_protocol_bob(q1, q2, q3, bob, socket):
    """
    Implements Bob's side of the 3->1 distillation protocol.
    This function should perform the gates and measurements for 3->1 using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param q3: Bob's qubit from the third entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    outcome1, outcome2 = three_to_one_gates_and_measurement_bob(q1, q2, q3)
    print("flushing now")
    bob.flush()
    print("bob done")
    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    
    # Bob sends measurement of 2A to Alice
    socket.send_structured(StructuredMessage("Measurement Bob 1",int(outcome1)))
    socket.send_structured(StructuredMessage("Measurement Bob 2",int(outcome2)))
    print("sent")
    # Bob receives Alice's measurement
    outcome_alice1 = socket.recv_structured().payload
    outcome_alice2 = socket.recv_structured().payload
    print("received")

    return int(outcome1)==outcome_alice1 and int(outcome2) == outcome_alice2

def three_to_one_gates_and_measurement_bob(q1, q2, q3):
    """
    Performs the gates and measurements for Bob's side of the 3->1 protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param q3: Bob's qubit from the third entangled pair
    :return: A pair of integer 0/1 indicating Bob's measurement outcomes from measuring the qubits
    """
    # CNOT B3->B2 
    q3.cnot(q2)

    # CNOT B1->B3
    q1.cnot(q3)

    #Bell measurement B1 B2
    q1.cnot(q2)

    q1.H()
    
    m1 = q1.measure()
    m2 = q2.measure()
    
    return m1,m2

