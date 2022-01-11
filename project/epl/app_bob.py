from threading import BrokenBarrierError
from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

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
        q1 = epr_socket.recv()[0]
        q2 = epr_socket.recv()[0]

        result = epl_protocol_bob(q1,q2,bob,socket)
        print(result, "BOB")

if __name__ == "__main__":
    main()
