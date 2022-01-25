from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from numpy import array2string

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket("bob","alice")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Alice's NetQASM connection
    bob = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's EPL method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        
        # Receive half of epr pairs
        qubits = epr_socket.recv(number=2)
        bob.flush()

        # Save original qubit states
        original0 = get_qubit_state(qubits[0])
        original1 = get_qubit_state(qubits[1])
        
        # Execute EPL Protocol
        result = epl_protocol_bob(qubits[0],qubits[1],bob,socket)
        
        if result:
            # Send DMs to Alice to compute fidelities
            socket.send(array2string(original0, separator=', '))
            socket.send(array2string(original1, separator=', '))
            socket.send(array2string(get_qubit_state(qubits[0]), separator=', '))

        print(result, "BOB")
        return result

if __name__ == "__main__":
    main()
