from epl import epl_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice","bob")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        
        # Create EPR Pair
        qubits = epr_socket.create(number=2)

        # Execute EPL Protocol
        result = epl_protocol_alice(qubits[0],qubits[1],alice,socket)
        print(result, "ALICE")

if __name__ == "__main__":
    main()
