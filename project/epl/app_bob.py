from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket("bob","alice")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's EPL method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        
        # Receive half of epr pairs
        qubits = epr_socket.recv(number=2)
        bob.flush()

        # Execute EPL Protocol
        result = epl_protocol_bob(qubits[0],qubits[1],bob,socket)

        return result

if __name__ == "__main__":
    main()
